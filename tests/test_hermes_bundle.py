"""The combined Hermes listing (hermes/digital-marketing-pro/) says what it is and is what it says.

Hermes's plugin catalog allows one plugin per vendor, so the Hermes listing folds ContentForge and
SocialForge into the Digital Marketing Pro listing as skill groups (strategy/, content/, social/).
That folder is a generated copy of three other repos, which makes four ways for it to go wrong:

  - someone edits a copied file by hand, or the copy goes stale after a plugin release
  - the manifest, the plugin.yaml and the marketplace disagree about a version
  - two groups define a skill with the same name, and one silently shadows the other
  - a skill points at a script that did not make it into the group

Every check below is a pure function over an in-memory tree, so each one is also run on a
planted failure and must flag it. The rebuild check needs the three sibling repos (it skips,
loudly, without them); everything else runs anywhere.

Stdlib only. Run with: python tests/run_all.py
"""
from __future__ import annotations

import ast
import importlib.util
import json
import re
import subprocess
import sys
import types
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUNDLE = REPO / "hermes" / "digital-marketing-pro"
SCRIPT = REPO / "scripts" / "build_hermes_bundle.py"

_spec = importlib.util.spec_from_file_location("build_hermes_bundle", SCRIPT)
gen = importlib.util.module_from_spec(_spec)
sys.modules["build_hermes_bundle"] = gen
_spec.loader.exec_module(gen)

GROUPS = tuple(gen.GROUPS)


def read_bundle() -> dict[str, bytes]:
    return gen.read_tree(BUNDLE)


def manifest_of(tree: dict[str, bytes]) -> dict:
    return json.loads(tree["BUNDLE-MANIFEST.json"].decode("utf-8"))


# ── checks (each takes a tree, returns a list of problems) ────────────────────

def manifest_problems(tree: dict[str, bytes]) -> list[str]:
    """Every file is listed with its sha256, and nothing is listed that is not there."""
    m = manifest_of(tree)
    expected = {}
    for group, info in m["groups"].items():
        for path, digest in info["files"].items():
            expected[f"{group}/{path}"] = digest
    expected.update(m["generated_files"])
    actual = {p: gen.sha256(d) for p, d in tree.items() if p != "BUNDLE-MANIFEST.json"}
    out = [f"not in the manifest: {p}" for p in sorted(set(actual) - set(expected))]
    out += [f"in the manifest but missing: {p}" for p in sorted(set(expected) - set(actual))]
    out += [f"edited since the manifest was written: {p}"
            for p in sorted(set(actual) & set(expected)) if actual[p] != expected[p]]
    return out


def skills_by_group(tree: dict[str, bytes]) -> dict[str, list[str]]:
    out = {}
    for group in GROUPS:
        sub = {p[len(group) + 1:]: d for p, d in tree.items() if p.startswith(group + "/")}
        out[group] = gen.skill_names(sub)
    return out


def collision_problems(tree: dict[str, bytes]) -> list[str]:
    seen, out = {}, []
    for group, names in skills_by_group(tree).items():
        for name in names:
            if name in seen:
                out.append(f"skill {name!r} is in both {seen[name]} and {group}")
            seen.setdefault(name, group)
    return out


def missing_script_problems(tree: dict[str, bytes]) -> list[str]:
    """Every scripts/<x>.py a group's SKILL.md names exists in that group."""
    out = []
    for path, data in tree.items():
        m = re.fullmatch(r"(strategy|content|social)/skills/[^/]+/SKILL\.md", path)
        if not m:
            continue
        group = m.group(1)
        for script in sorted(set(re.findall(r"(?<![\w/.-])scripts/([A-Za-z0-9_.\-]+\.py)", data.decode("utf-8", "replace")))):
            if f"{group}/scripts/{script}" not in tree:
                out.append(f"{path} names scripts/{script}, which is not in {group}/")
    return out


def init_problems(tree: dict[str, bytes]) -> list[str]:
    """__init__.py imports only the standard library."""
    out = []
    mod = ast.parse(tree["__init__.py"].decode("utf-8"))
    for node in ast.walk(mod):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        for n in names:
            if n.split(".")[0] not in sys.stdlib_module_names and n != "__future__":
                out.append(f"__init__.py imports {n}, which is not in the standard library")
    return out


def load_init(tree_root: Path):
    spec = importlib.util.spec_from_file_location("dmp_bundle_init", tree_root / "__init__.py")
    mod = importlib.util.module_from_spec(spec)
    keep, sys.dont_write_bytecode = sys.dont_write_bytecode, True   # leave no __pycache__ in the bundle
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.dont_write_bytecode = keep
    return mod


class FakeCtx:
    def __init__(self):
        self.skills = []

    def register_skill(self, name, path):
        self.skills.append((name, Path(path)))


# ── tests ─────────────────────────────────────────────────────────────────────

class TestBundleIsWhatItSays(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert BUNDLE.is_dir(), "hermes/digital-marketing-pro/ is missing: run scripts/build_hermes_bundle.py"
        cls.tree = read_bundle()
        cls.manifest = manifest_of(cls.tree)

    def test_every_file_matches_the_manifest(self):
        self.assertEqual(manifest_problems(self.tree), [])

    def test_the_bundle_is_stored_byte_for_byte(self):
        """`* -text` keeps git from converting line endings, so the sha256s are what is served."""
        self.assertEqual(self.tree[".gitattributes"], b"* -text\n")

    def test_the_bundle_rebuilds_identically_from_the_recorded_commits(self):
        sources = gen.manifest_sources(self.manifest)
        if sources is None:
            self.skipTest("a plugin repo is not checked out beside the marketplace, so the bundle "
                          "cannot be rebuilt here (the manifest check above still ran)")
        for group, (repo, sha) in sources.items():
            if gen.git(repo, "cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode != 0:
                self.skipTest(f"{repo.name} does not have commit {sha[:12]}; fetch it to rebuild")
        fresh = gen.generate(sources, self.manifest["version"])
        self.assertEqual(gen.diff_trees(self.tree, fresh), [],
                         "the bundle is stale or hand-edited: run scripts/build_hermes_bundle.py")

    def test_versions_agree_with_the_marketplace(self):
        market = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        listed = {p["name"]: p["version"] for p in market["plugins"]}
        for group, info in self.manifest["groups"].items():
            with self.subTest(group=group):
                self.assertEqual(info["version"], listed[info["plugin"]],
                                 f"{info['plugin']} is {listed[info['plugin']]} in the marketplace "
                                 f"but the bundle holds {info['version']}: rebuild it")
                self.assertRegex(info["commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(self.manifest["version"], market["metadata"]["version"])
        self.assertIn(f"\nversion: {self.manifest['version']}\n", self.tree["plugin.yaml"].decode("utf-8"))
        self.assertIn(f'PLUGIN_VERSION = "{self.manifest["version"]}"', self.tree["__init__.py"].decode("utf-8"))

    def test_skill_names_are_unique_across_groups(self):
        self.assertEqual(collision_problems(self.tree), [])

    def test_skill_counts_match_the_manifest_and_the_description(self):
        per = skills_by_group(self.tree)
        total = sum(len(v) for v in per.values())
        for group, names in per.items():
            self.assertEqual(len(names), self.manifest["groups"][group]["skills"], group)
        self.assertIn(f"{total} skills in all", self.tree["plugin.yaml"].decode("utf-8").replace("\n  ", " "))
        self.assertIn(f"**{total} skills in all.**", self.tree["README.md"].decode("utf-8").replace("\n", " "))

    def test_every_script_a_skill_names_is_in_its_group(self):
        self.assertEqual(missing_script_problems(self.tree), [])

    def test_init_is_stdlib_only(self):
        self.assertEqual(init_problems(self.tree), [])

    def test_init_registers_exactly_every_skill(self):
        mod = load_init(BUNDLE)
        ctx = FakeCtx()
        mod.register(ctx)
        total = sum(v["skills"] for v in self.manifest["groups"].values())
        self.assertEqual(len(ctx.skills), total)
        self.assertEqual(len({n for n, _ in ctx.skills}), total, "a skill name was registered twice")
        for name, path in ctx.skills:
            self.assertTrue(path.is_file(), f"{name} points at {path}, which is not a file")
        self.assertEqual(mod.audit()["skill_count"], total)

    def test_init_never_raises(self):
        mod = load_init(BUNDLE)
        mod.register(types.SimpleNamespace())          # a ctx with no register_skill

        class Boom(FakeCtx):
            def register_skill(self, name, path):
                raise RuntimeError("boom")
        mod.register(Boom())                            # every registration fails

    def test_nothing_the_other_platforms_read_is_copied(self):
        banned = (".claude-plugin/", ".codex-plugin/", ".cursor-plugin/", ".grok-plugin/", ".github/",
                  "gemini-extension.json", "openclaw.plugin.json", "package.json", "plugin.json",
                  "plugin.yaml", "tests/", "evals/")
        for path in self.tree:
            if path.split("/")[0] in GROUPS:
                inner = path.split("/", 1)[1]
                with self.subTest(path=path):
                    self.assertFalse(any(inner == b or inner.startswith(b) for b in banned),
                                     f"{path} is another platform's file or a test")
                    self.assertFalse(re.fullmatch(r"README\.[A-Za-z-]+\.md", inner), path)


class TestPlantedFailuresAreFlagged(unittest.TestCase):
    """Each check on a tree that has exactly the failure it exists to catch."""

    @classmethod
    def setUpClass(cls):
        cls.tree = read_bundle()

    def planted(self):
        return dict(self.tree)

    def test_a_clean_tree_has_no_problems(self):
        t = self.planted()
        self.assertEqual(manifest_problems(t) + collision_problems(t) + missing_script_problems(t) + init_problems(t), [])

    def test_a_stale_group_file_is_flagged(self):
        t = self.planted()
        victim = next(p for p in t if p.startswith("content/skills/") and p.endswith("SKILL.md"))
        t[victim] = t[victim] + b"\nstale edit\n"
        self.assertEqual(manifest_problems(t), [f"edited since the manifest was written: {victim}"])

    def test_an_unlisted_and_a_missing_file_are_flagged(self):
        t = self.planted()
        t["social/scripts/extra.py"] = b"x = 1\n"
        gone = next(p for p in t if p.startswith("strategy/scripts/") and p.endswith(".py"))
        del t[gone]
        problems = manifest_problems(t)
        self.assertIn("not in the manifest: social/scripts/extra.py", problems)
        self.assertIn(f"in the manifest but missing: {gone}", problems)

    def test_a_skill_name_collision_is_flagged(self):
        t = self.planted()
        name = skills_by_group(t)["content"][0]
        src = next(p for p in t if p.startswith("content/skills/") and p.endswith("/SKILL.md")
                   and gen.skill_names({p.split("/", 1)[1]: t[p]}) == [name])
        t["social/skills/shadow/SKILL.md"] = t[src]
        problems = collision_problems(t)
        self.assertEqual(len(problems), 1)
        self.assertIn(repr(name), problems[0])

    def test_a_missing_script_is_flagged(self):
        t = self.planted()
        skill = next(p for p in t if re.fullmatch(r"content/skills/[^/]+/SKILL\.md", p)
                     and re.search(rb"(?<![\w/.-])scripts/[A-Za-z0-9_.\-]+\.py", t[p]))
        script = re.search(rb"(?<![\w/.-])scripts/([A-Za-z0-9_.\-]+\.py)", t[skill]).group(1).decode()
        del t[f"content/scripts/{script}"]
        self.assertTrue(any(skill in p and script in p for p in missing_script_problems(t)))

    def test_a_non_stdlib_import_in_init_is_flagged(self):
        t = self.planted()
        t["__init__.py"] = t["__init__.py"] + b"\nimport requests\n"
        self.assertEqual(init_problems(t), ["__init__.py imports requests, which is not in the standard library"])


if __name__ == "__main__":
    unittest.main()
