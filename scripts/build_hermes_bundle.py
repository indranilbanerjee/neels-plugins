#!/usr/bin/env python3
"""Build the combined Hermes Agent listing: hermes/digital-marketing-pro/.

Hermes's plugin catalog allows one plugin per vendor (maintainer request, 2026-10-10), so the
Hermes listing folds ContentForge and SocialForge into the Digital Marketing Pro listing as
skill groups. This is Hermes-only: on every other platform the three plugins stay separate
products, and their repos stay self-contained. The folded copy lives here, in the marketplace
repo, because cross-plugin artefacts belong here and not in any one plugin.

What it writes (all of it generated, nothing hand-edited)::

    hermes/digital-marketing-pro/
      .gitattributes        # `* -text`: git stores these bytes exactly, so the sha256s hold
      plugin.yaml           # skills-only; capabilities = the union of the three plugins
      __init__.py           # stdlib-only adapter: registers every SKILL.md of the three groups
      README.md             # what the listing holds, versions, disclosures
      BUNDLE-MANIFEST.json  # per group: repo, version, full commit sha, file list with sha256
      strategy/             # Digital Marketing Pro, runtime files at its release commit
      content/              # ContentForge, runtime files at its release commit
      social/               # SocialForge, runtime files at its release commit

Each group is `git archive <sha>` of the sibling repo, so only tracked files at that commit
(no working-tree noise), minus what a Hermes install never reads: tests, evals, docs (except
the docs files a skill, script or agent points at), research notes, hooks, workflows, the other
platforms' manifests and the README translations. Skills keep their relative layout, so each
skill's "the scripts are in this plugin's `scripts/` folder, next to `skills/`" stays true
inside its group.

Run it from the marketplace repo::

    python scripts/build_hermes_bundle.py            # rebuild from the siblings' HEAD
    python scripts/build_hermes_bundle.py --check    # fail if the tree differs from a rebuild

It refuses to run unless each sibling (../digital-marketing-pro, ../ContentForge,
../SocialForge, or $DMP_DIR / $CF_DIR / $SF_DIR) has no modified tracked files, its HEAD is
contained in its upstream branch, and its plugin.json version equals its top CHANGELOG
version. Output is deterministic: running it twice leaves no diff.

Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUNDLE_DIR = REPO / "hermes" / "digital-marketing-pro"
SUITE_ROOT = REPO.parent

BUNDLE_NAME = "digital-marketing-pro"
GITHUB = "https://github.com/indranilbanerjee/"

# group folder -> (plugin, sibling folder names, env var, repo name, one-line role)
GROUPS = {
    "strategy": ("digital-marketing-pro", ("digital-marketing-pro",), "DMP_DIR", "digital-marketing-pro",
                 "marketing strategy, SEO/AEO/GEO, paid media, CRM and analytics"),
    "content": ("contentforge", ("ContentForge", "contentforge"), "CF_DIR", "contentforge",
                "long-form content: research, fact-check, draft, humanize, audit"),
    "social": ("socialforge", ("SocialForge", "socialforge"), "SF_DIR", "socialforge",
               "social creative: calendar to images, carousels, video and copy"),
}

# Top-level folders a Hermes install never reads.
DROP_DIRS = {"tests", "evals", "docs", "research", ".tmp", "hooks", "workflows", ".github",
             ".claude-plugin", ".codex-plugin", ".cursor-plugin", ".grok-plugin", ".agents"}
# Root files that are other platforms' manifests, repo furniture or maintenance docs.
DROP_ROOT = {"gemini-extension.json", "openclaw.plugin.json", "package.json", "plugin.json",
             "plugin.yaml", "__init__.py", ".gitignore", ".gitattributes", "CODE_OF_CONDUCT.md",
             "CONTRIBUTING.md", "SPONSORS.md", "SECURITY.md", "AGENTS.md", "SUBMISSION.md",
             "TESTING-GUIDE.md", "UPGRADE-GUIDE.md", "COWORK-GUIDE.md"}
DROP_ROOT_RE = re.compile(r"^(README\.[A-Za-z-]+\.md|.*(ENGINEERING-SPEC|PRD-Blueprint).*\.md)$")
# Folders whose files are scanned for references to a docs file (README and CHANGELOG are not:
# they point at every doc there is).
RUNTIME_DIRS = ("skills", "scripts", "agents", "commands", "references", "config", "templates",
                "utilities", "utils")
TEXT_SUFFIXES = (".md", ".py", ".json", ".yaml", ".yml", ".txt", ".js", ".html")
DOCS_REF = re.compile(r"(?<![\w./-])docs/[A-Za-z0-9_.\-]+\.(?:md|json|yaml|txt)")

ATTRIBUTES = "* -text\n"

# A variable two plugins read for different reasons gets one description in the union.
ENV_UNION_TEXT = {
    "GEMINI_API_KEY": "Gemini API key: image generation and asset indexing in the social group (an alternative "
                      "to Vertex AI), and the optional model-registry refresh (scripts/refresh_models.py) in every group",
}


# ── the three generated files that are not copies ─────────────────────────────

INIT_PY = r'''"""Hermes Agent adapter for the combined Digital Marketing Pro listing.

Read ONLY by Hermes Agent. The listing folds three plugins into one: Digital Marketing Pro
(strategy/), ContentForge (content/) and SocialForge (social/). Each group keeps the layout of its
own repo, with `skills/` next to `scripts/`, `references/` and the rest, so every skill's
"the scripts are in this plugin's `scripts/` folder, next to `skills/`" is true inside its group.

register(ctx) walks the three `skills/` folders and exposes every SKILL.md through
ctx.register_skill(name, path). Names are the skills' own names (a test keeps them unique across
the groups); Hermes namespaces them as `digital-marketing-pro:<skill>` and, while the plugin is
enabled, lists every one by name in the system prompt's <available_skills> (no description is passed).

This listing registers no tools, hooks or middleware, so there is nothing to switch on or off per
group. Standard library only; it never raises (a problem is logged and the rest still register).

Generated by scripts/build_hermes_bundle.py in the neels-plugins repo. Do not edit by hand.
"""
from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger("digital-marketing-pro")

PLUGIN_ROOT = Path(__file__).resolve().parent
PLUGIN_VERSION = "@@VERSION@@"
GROUPS = (@@GROUPS@@)


def _skill_name(skill_md: Path) -> str:
    """The `name:` in a SKILL.md's frontmatter, or the folder name when there is none."""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.debug("could not read %s: %s", skill_md, exc)
        return skill_md.parent.name
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if match:
        m = re.search(r'^name:\s*["\']?(.*?)["\']?\s*$', match.group(1), re.MULTILINE)
        if m and m.group(1).strip():
            return m.group(1).strip()
    return skill_md.parent.name


def _walk_skills() -> list[dict]:
    """Every group's skills/<name>/SKILL.md as {group, name, path}, in a stable order."""
    found: list[dict] = []
    for group in GROUPS:
        skills_dir = PLUGIN_ROOT / group / "skills"
        if not skills_dir.is_dir():
            logger.warning("digital-marketing-pro: %s/skills not found at %s", group, skills_dir)
            continue
        for entry in sorted(skills_dir.iterdir()):
            skill_md = entry / "SKILL.md"
            if entry.is_dir() and skill_md.is_file():
                found.append({"group": group, "name": _skill_name(skill_md), "path": skill_md})
    return found


def register(ctx) -> None:
    """Hermes plugin entry point. Called once at startup; never raises."""
    logger.info("digital-marketing-pro v%s registering with Hermes", PLUGIN_VERSION)
    skills = _walk_skills()
    if not skills:
        logger.warning("digital-marketing-pro found 0 skills under %s; the plugin will be inert. "
                       "Confirm it was installed with its strategy/, content/ and social/ folders.",
                       PLUGIN_ROOT)
        return
    if not hasattr(ctx, "register_skill"):
        logger.error("digital-marketing-pro: Hermes ctx has no register_skill(); %d skills could "
                     "not be registered.", len(skills))
        return
    registered, failed, seen = 0, 0, set()
    for skill in skills:
        if skill["name"] in seen:
            failed += 1
            logger.warning("digital-marketing-pro: skill name %r appears in more than one group; "
                           "skipping the copy in %s", skill["name"], skill["group"])
            continue
        try:
            ctx.register_skill(skill["name"], skill["path"])
            seen.add(skill["name"])
            registered += 1
        except Exception as exc:  # defensive: one bad skill must not block the rest
            failed += 1
            logger.warning("digital-marketing-pro: failed to register %r: %s", skill["name"], exc)
    logger.info("digital-marketing-pro v%s: registered %d skills (failed: %d) under 'digital-marketing-pro:'",
                PLUGIN_VERSION, registered, failed)


def audit() -> dict:
    """What register() would do, without Hermes: `python __init__.py` prints it."""
    skills = _walk_skills()
    per_group = {g: sum(1 for s in skills if s["group"] == g) for g in GROUPS}
    return {"plugin_root": str(PLUGIN_ROOT), "plugin_version": PLUGIN_VERSION,
            "skill_count": len(skills), "skills_per_group": per_group}


if __name__ == "__main__":
    import json
    print(json.dumps(audit(), indent=2))
'''


def plugin_yaml(version: str, groups: dict, optional_env: list[dict]) -> str:
    g = groups
    counts = {k: v["skills"] for k, v in g.items()}
    total = sum(counts.values())
    desc = (
        f"Three open-source marketing toolkits in one Hermes listing, {total} skills in all: "
        f"Digital Marketing Pro v{g['strategy']['version']} (strategy, SEO/AEO/GEO, paid media, CRM, "
        f"analytics; {counts['strategy']} skills), ContentForge v{g['content']['version']} (long-form "
        f"content, fact-check, humanize, audit; {counts['content']} skills) and SocialForge "
        f"v{g['social']['version']} (social creative from a content calendar; {counts['social']} skills). "
        "Skills only: no tools, hooks or background processes. Disclosure: optional scripts call "
        "third-party APIs with the user's own keys; packages and browsers install only when the user "
        "says yes; live writes need a typed yes and, for writes the plugin sends itself, a single-use "
        "approval record; see README.md and each group's PRIVACY.md."
    )
    lines = [
        "# Hermes Agent native plugin manifest for the combined Digital Marketing Pro listing.",
        "# Generated by scripts/build_hermes_bundle.py in the neels-plugins repo; do not edit by hand.",
        "# Only Hermes reads this file. On every other platform the three plugins are separate products",
        "# with their own repos and manifests.",
        "",
        f"name: {BUNDLE_NAME}",
        f"version: {version}",
        "description: >-",
    ]
    lines += ["  " + part for part in _wrap(desc, 96)]
    lines += [
        "author: Indranil Banerjee",
        "license: MIT",
        f"homepage: {GITHUB}neels-plugins",
        "",
        "provides_tools: []",
        "provides_hooks: []",
        "requires_env: []",
        "# Every credential below is OPTIONAL: nothing is required to install, and a script that needs one",
        "# says so and stops. They are listed (not in requires_env) so the catalog and `hermes plugins` can",
        "# show which environment variables the scripts read. This is the union of ContentForge's and",
        "# SocialForge's lists.",
        "optional_env:",
    ]
    for item in optional_env:
        lines += [f"  - name: {item['name']}",
                  f"    description: {json.dumps(item['description'], ensure_ascii=False)}",
                  f"    secret: {item['secret']}"]
    return "\n".join(lines) + "\n"


def _wrap(text: str, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def parse_optional_env(yaml_text: str) -> list[dict]:
    """The `optional_env:` list of a plugin.yaml in the exact shape these plugins write it."""
    items, cur, in_block = [], None, False
    for line in yaml_text.splitlines():
        if re.match(r"^optional_env:\s*$", line):
            in_block = True
            continue
        if in_block and re.match(r"^\S", line):
            break
        if not in_block:
            continue
        m = re.match(r"^  - name:\s*(\S+)\s*$", line)
        if m:
            cur = {"name": m.group(1), "description": "", "secret": "false"}
            items.append(cur)
            continue
        m = re.match(r"^    (description|secret):\s*(.*?)\s*$", line)
        if m and cur is not None:
            cur[m.group(1)] = m.group(2)
    return items


def listing_chars(names: list[str]) -> int:
    """Characters the registered skills add to Hermes's system-prompt index: one `    - <plugin>:<name>`
    row each (names only: the adapter registers no descriptions), counting the line break."""
    return sum(len(f"    - {BUNDLE_NAME}:{n}") + 1 for n in names)


def readme_md(version: str, groups: dict, listing_chars: int) -> str:
    g = groups
    total = sum(v["skills"] for v in g.values())
    rows = "\n".join(
        f"| `{k}/` | [{v['plugin']}]({v['repo']}) | {v['version']} | `{v['commit'][:12]}` | {v['skills']} | {GROUPS[k][4]} |"
        for k, v in g.items())
    return f"""# Digital Marketing Pro for Hermes Agent: three toolkits, one listing

This is the folder Hermes installs from the [neels-plugins marketplace]({GITHUB}neels-plugins) as
`digital-marketing-pro` (version {version}). Hermes allows one plugin per vendor, so the Hermes
listing holds three of our marketing plugins as skill groups. **{total} skills in all.** It is
generated, never hand-edited: `scripts/build_hermes_bundle.py` in the marketplace repo copies each
plugin's runtime files from its release commit and records the commit and a sha256 per file in
`BUNDLE-MANIFEST.json`.

| Folder | Plugin | Version | Commit | Skills | What it covers |
|---|---|---|---|---|---|
{rows}

On every other platform (Claude Code, Cowork, Codex, Cursor, Copilot CLI, Antigravity, OpenClaw,
Grok) the three plugins are separate products installed from their own repos, which stay
self-contained; nothing here changes them. Only Hermes gets the combined folder.

## How it loads

- `plugin.yaml` + `__init__.py` is a skills-only Hermes plugin: it registers every `SKILL.md` of the
  three groups with `ctx.register_skill`. The skills keep their own names and Hermes shows them as
  `digital-marketing-pro:<skill>`. A test keeps the names unique across the groups.
- **What it adds to the system prompt.** Hermes lists the skills of an enabled plugin in the system
  prompt's skills index. This listing registers its {total} skills by name only (the adapter passes no
  descriptions): {total} rows, about {listing_chars:,} characters (roughly {listing_chars // 4:,} tokens).
  Disable the plugin to remove them; a skill's full text loads with `skill_view` when it is asked for.
- It registers **no tools, hooks or middleware**, so `hermes tools` has nothing to switch on or off
  per group, and there is no group switch. Use the skills you want; ignore the rest.
- Each skill that runs a script says where it is when `${{CLAUDE_PLUGIN_ROOT}}` is not set (it is not set
  on Hermes): the group's `scripts/` folder, next to its `skills/`.

## What it never does

- **Install a package or a browser on its own.** A missing package prints its exact pinned install command;
  Playwright's browser and the optional packages install only when you say yes.
- **Send, publish or spend without your say-so.** Live writes wait for your typed `yes`; SocialForge
  shows a live price quote before any paid image or video generation and waits for "go".
- **Ask for an API key in the chat.** Keys come from environment variables.
- **Connect a service you did not set up.** No MCP server is configured by this listing and no hook runs.
- **Remove or hide AI watermarks.** AI involvement is disclosed, with C2PA provenance.

## Disclosures

These are the points a Hermes user should know before installing.

- **The agent creates and approves its own live-write records, and Hermes does not prompt before those
  script runs.** For writes the plugin sends itself (`/digital-marketing-pro:execute-action`), the script
  creates a single-use approval record at prepare, with a preview of the exact request. The skill approves
  that record after you type `yes`, and the request must match it byte for byte within 15 minutes. The
  record proves the approval step ran for this request, once; it cannot prove who typed `yes`, because
  the agent runs every command. Writes through MCP server tools are outside this check and rely on the
  skill's typed `yes` and your host's permission prompt. Keep script runs and MCP write tools out of
  your host's allowlist so it asks every time.
- **`refresh_models.py` reads your provider keys.** The optional model-registry refresh in each group
  reads `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` and `GEMINI_API_KEY` from the environment, and only when
  you run it; a provider without a key is skipped.
- **Keys and data live outside the Hermes profile.** SocialForge keeps its credentials and brand data in
  `~/socialforge-workspace` when no plugin-data folder is set; ContentForge and Digital Marketing Pro keep
  brand data under `~/.claude-marketing/`.
- **Installs run only when you say yes.** Nothing installs itself. SocialForge's setup lists what is
  missing and installs the pinned versions after an explicit `yes`.
- Network calls happen only when you, or a skill you invoked, run a script, and only to the endpoints each
  group lists in its `PRIVACY.md`.

Each group carries its own `README.md`, `PRIVACY.md` and `CHANGELOG.md` for the plugin it was copied from.

## What is left out

Tests, evals, most docs, research notes, hooks, workflows, the other platforms' manifests and the README
translations are not copied: a Hermes install never reads them. A `docs/` file stays when a skill, script
or agent points at it.

## Verifying

```bash
python __init__.py                       # what register() would do, without Hermes
python -c "import json;print(json.load(open('BUNDLE-MANIFEST.json'))['groups']['content']['commit'])"
```

`BUNDLE-MANIFEST.json` lists every copied file with its sha256. The marketplace's tests rebuild the folder
from those commits and fail on any difference, and Hermes's own `hermes plugins validate` runs on it.
"""


# ── git plumbing ──────────────────────────────────────────────────────────────

def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, check=check)


def sibling_dir(group: str) -> Path | None:
    _plugin, names, env, _repo, _role = GROUPS[group]
    if os.environ.get(env):
        p = Path(os.environ[env])
        return p if p.is_dir() else None
    for n in names:
        if (SUITE_ROOT / n / ".git").exists():
            return SUITE_ROOT / n
    return None


def release_problems(repo: Path) -> list[str]:
    """Why a sibling is not ready to be folded in (empty when it is)."""
    problems = []
    dirty = git(repo, "status", "--porcelain", "--untracked-files=no").stdout.decode().strip()
    if dirty:
        problems.append("has modified tracked files:\n      " + dirty.replace("\n", "\n      "))
    up = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}", check=False)
    if up.returncode != 0:
        problems.append("its branch has no upstream, so HEAD cannot be shown to be pushed")
    elif git(repo, "merge-base", "--is-ancestor", "HEAD", "@{u}", check=False).returncode != 0:
        problems.append("HEAD is not contained in its upstream branch (unpushed commits)")
    head = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    try:
        pj = json.loads(git(repo, "show", f"{head}:.claude-plugin/plugin.json").stdout.decode("utf-8"))
        cl = git(repo, "show", f"{head}:CHANGELOG.md").stdout.decode("utf-8")
        top = re.search(r"^## \[(\d+\.\d+\.\d+)\]", cl, re.M).group(1)
        if pj["version"] != top:
            problems.append(f"plugin.json says {pj['version']} but the top CHANGELOG entry is {top}")
    except Exception as exc:  # unreadable metadata is a reason to stop, not to guess
        problems.append(f"cannot read the plugin version/CHANGELOG at HEAD: {exc}")
    return problems


def archive_files(repo: Path, sha: str) -> dict[str, bytes]:
    """Every tracked regular file at `sha`: {path: bytes} (no working tree involved)."""
    # core.autocrlf=true (the Git for Windows default) makes `git archive` rewrite LF to CRLF; the bundle
    # must hold the commit's own bytes on every machine, so conversion is switched off for this call.
    tar = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "core.eol=lf", "archive", "--format=tar", sha],
                         cwd=repo, capture_output=True, check=True).stdout
    out: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
        for m in tf.getmembers():
            if m.isfile():
                out[m.name] = tf.extractfile(m).read()
    return out


# ── selection ─────────────────────────────────────────────────────────────────

def select(files: dict[str, bytes]) -> dict[str, bytes]:
    """The runtime files of one plugin: what a Hermes install can read."""
    referenced = set()
    for path, data in files.items():
        if path.split("/")[0] in RUNTIME_DIRS and path.endswith(TEXT_SUFFIXES):
            referenced.update(DOCS_REF.findall(data.decode("utf-8", errors="replace")))
    kept = {}
    for path, data in files.items():
        top = path.split("/")[0]
        if "/" not in path:
            if path in DROP_ROOT or DROP_ROOT_RE.match(path):
                continue
        elif top in DROP_DIRS:
            if not (top == "docs" and path in referenced):
                continue
        kept[path] = data
    return kept


def skill_names(files: dict[str, bytes]) -> list[str]:
    """Skill names as the adapter reads them: frontmatter `name:`, else the folder name."""
    names = []
    for path in sorted(files):
        m = re.fullmatch(r"skills/([^/]+)/SKILL\.md", path)
        if not m:
            continue
        text = files[path].decode("utf-8", errors="replace")
        fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        name = None
        if fm:
            nm = re.search(r'^name:\s*["\']?(.*?)["\']?\s*$', fm.group(1), re.MULTILINE)
            if nm and nm.group(1).strip():
                name = nm.group(1).strip()
        names.append(name or m.group(1))
    return names


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ── generation ────────────────────────────────────────────────────────────────

def market_version() -> str:
    doc = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    return doc["metadata"]["version"]


def generate(sources: dict[str, tuple[Path, str]], version: str) -> dict[str, bytes]:
    """The whole bundle as {relative path: bytes}. `sources` maps group -> (sibling repo, sha)."""
    tree: dict[str, bytes] = {}
    groups: dict[str, dict] = {}
    all_names: list[str] = []
    optional_env: dict[str, dict] = {}
    for group in GROUPS:
        repo, sha = sources[group]
        plugin, _names, _env, repo_name, _role = GROUPS[group]
        files = archive_files(repo, sha)
        pj = json.loads(files[".claude-plugin/plugin.json"].decode("utf-8"))
        kept = select(files)
        names = skill_names(kept)
        all_names += names
        for path, data in kept.items():
            tree[f"{group}/{path}"] = data
        for item in parse_optional_env(files.get("plugin.yaml", b"").decode("utf-8")):
            cur = optional_env.setdefault(item["name"], item)
            if cur is not item and cur["description"] != item["description"]:
                # the same variable described two ways: say what it is for in the union
                cur["description"] = ENV_UNION_TEXT.get(item["name"], cur["description"])
            if "true" in (cur["secret"], item["secret"]):
                cur["secret"] = "true"
        groups[group] = {"plugin": plugin, "repo": GITHUB + repo_name, "version": pj["version"],
                         "commit": sha, "skills": len(names),
                         "files": {p: sha256(d) for p, d in sorted(kept.items())}}
    group_list = ", ".join(f'"{g}"' for g in GROUPS) + ","
    generated = {
        ".gitattributes": ATTRIBUTES.encode(),
        "__init__.py": INIT_PY.replace("@@VERSION@@", version).replace("@@GROUPS@@", group_list).encode(),
        "plugin.yaml": plugin_yaml(version, groups, sorted(optional_env.values(), key=lambda i: i["name"])).encode(),
        "README.md": readme_md(version, groups, listing_chars(all_names)).encode(),
    }
    tree.update(generated)
    manifest = {
        "bundle": BUNDLE_NAME, "version": version,
        "generator": "scripts/build_hermes_bundle.py",
        "groups": groups,
        "generated_files": {p: sha256(d) for p, d in sorted(generated.items())},
    }
    tree["BUNDLE-MANIFEST.json"] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    return tree


def write_tree(tree: dict[str, bytes], out: Path) -> None:
    """Make `out` hold exactly `tree`. Files already right are left alone (so an editor or an
    indexer holding one open cannot fail the build), stale files are removed, empty folders pruned."""
    out.mkdir(parents=True, exist_ok=True)
    for rel, data in sorted(tree.items()):
        target = out / rel
        if target.is_file() and target.read_bytes() == data:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for rel in sorted(set(read_tree(out)) - set(tree)):
        (out / rel).unlink()
    for folder in sorted((p for p in out.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        if not any(folder.iterdir()):
            folder.rmdir()


def read_tree(root: Path) -> dict[str, bytes]:
    """Every file under root (bytecode caches are not part of a bundle and are ignored)."""
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def diff_trees(a: dict[str, bytes], b: dict[str, bytes]) -> list[str]:
    out = [f"only in the existing tree: {p}" for p in sorted(set(a) - set(b))]
    out += [f"missing from the existing tree: {p}" for p in sorted(set(b) - set(a))]
    out += [f"differs: {p}" for p in sorted(set(a) & set(b)) if a[p] != b[p]]
    return out


def manifest_sources(manifest: dict) -> dict[str, tuple[Path, str]] | None:
    """Siblings plus the commits a manifest records, or None when a sibling is absent."""
    out = {}
    for group in GROUPS:
        repo = sibling_dir(group)
        if repo is None:
            return None
        out[group] = (repo, manifest["groups"][group]["commit"])
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="rebuild into a temp folder and exit 1 if hermes/digital-marketing-pro differs")
    args = ap.parse_args(argv)

    sources, bad = {}, False
    for group in GROUPS:
        repo = sibling_dir(group)
        if repo is None:
            print(f"error: no checkout for {GROUPS[group][0]} (looked beside this repo and at ${GROUPS[group][2]})")
            return 2
        for p in release_problems(repo):
            print(f"error: {GROUPS[group][0]} {p}")
            bad = True
        sources[group] = (repo, git(repo, "rev-parse", "HEAD").stdout.decode().strip())
    if bad:
        print("refusing to build: each sibling must be clean, pushed, and consistent about its version")
        return 2

    tree = generate(sources, market_version())
    if args.check:
        existing = read_tree(BUNDLE_DIR) if BUNDLE_DIR.exists() else {}
        diffs = diff_trees(existing, tree)
        for d in diffs[:40]:
            print(d)
        print("hermes bundle is current" if not diffs else f"{len(diffs)} difference(s): run without --check")
        return 1 if diffs else 0
    write_tree(tree, BUNDLE_DIR)
    manifest = json.loads(tree["BUNDLE-MANIFEST.json"])
    for group, info in manifest["groups"].items():
        print(f"{group:9s} {info['plugin']:22s} {info['version']:8s} {info['commit'][:12]}  "
              f"{info['skills']:3d} skills  {len(info['files'])} files")
    print(f"wrote {BUNDLE_DIR.relative_to(REPO)} ({len(tree)} files, version {manifest['version']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
