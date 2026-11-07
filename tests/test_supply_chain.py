"""Installs take a released, pinned commit, never the plugin's default branch.

The 2026-11-05 security review (finding 11): every marketplace entry was
`{"source": "github", "repo": "indranilbanerjee/<plugin>"}` with no tag or commit, so an install or
update took whatever was on the default branch, and a push from a compromised account reached every
user at their next update. The Hermes bundle in this repo was already pinned by commit and sha256.

Since 3.60.0:
  * Claude Code and Copilot entries carry `ref: "v<version>"` and the tag's full 40-character `sha`;
  * Codex entries carry `ref: "v<version>"` (its format documents `ref`);
  * the Hermes bundle's recorded commit for each folded plugin is the commit the marketplace pins;
  * with network access, each tag exists in its repository and points at the pinned commit.
Cursor and Grok document no pin field, so their entries are left as plain repository sources.

Stdlib only. The tag check uses `git ls-remote` and skips when the network is unavailable.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFESTS = {
    "claude": REPO / ".claude-plugin" / "marketplace.json",
    "copilot": REPO / ".github" / "plugin" / "marketplace.json",
    "codex": REPO / ".agents" / "plugins" / "marketplace.json",
}
SHA_PINNED = ("claude", "copilot")
BUNDLE = REPO / "hermes" / "digital-marketing-pro" / "BUNDLE-MANIFEST.json"
BUNDLE_GROUPS = {"strategy": "digital-marketing-pro", "content": "contentforge", "social": "socialforge"}
SHA = re.compile(r"^[0-9a-f]{40}$")


def entries(name: str) -> dict:
    doc = json.loads(MANIFESTS[name].read_text(encoding="utf-8"))
    return {p["name"]: p for p in doc["plugins"]}


def pin_problems(entry: dict, need_sha: bool) -> list[str]:
    src = entry.get("source")
    if not isinstance(src, dict):
        return [f"{entry.get('name')}: source is not an object, so it cannot be pinned"]
    out = []
    want = "v" + str(entry.get("version"))
    if src.get("ref") != want:
        out.append(f"{entry['name']}: ref is {src.get('ref')!r}, expected {want!r}")
    if need_sha and not SHA.match(str(src.get("sha", ""))):
        out.append(f"{entry['name']}: sha is {src.get('sha')!r}, expected a full 40-character commit")
    return out


def remote_tag_commit(repo: str, tag: str):
    """The commit a tag names on GitHub (peeled for annotated tags), or None when it cannot be checked."""
    try:
        out = subprocess.run(["git", "ls-remote", f"https://github.com/{repo}.git", f"refs/tags/{tag}",
                              f"refs/tags/{tag}^{{}}"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    lines = dict(reversed(line.split("\t")) for line in out.stdout.splitlines() if "\t" in line)
    return lines.get(f"refs/tags/{tag}^{{}}") or lines.get(f"refs/tags/{tag}") or ""


class TestEntriesArePinned(unittest.TestCase):
    def test_every_entry_is_pinned_to_its_release(self):
        bad = {}
        for name in MANIFESTS:
            for pname, entry in entries(name).items():
                if p := pin_problems(entry, need_sha=name in SHA_PINNED):
                    bad[f"{name}/{pname}"] = p
        self.assertEqual(bad, {})

    def test_hosts_pin_the_same_commit(self):
        claude, copilot, codex = entries("claude"), entries("copilot"), entries("codex")
        for pname, entry in claude.items():
            with self.subTest(plugin=pname):
                self.assertEqual(entry["source"]["sha"], copilot[pname]["source"]["sha"])
                self.assertEqual(entry["source"]["ref"], copilot[pname]["source"]["ref"])
                self.assertEqual(entry["source"]["ref"], codex[pname]["source"]["ref"])

    def test_hermes_bundle_folds_the_pinned_commits(self):
        groups = json.loads(BUNDLE.read_text(encoding="utf-8"))["groups"]
        claude = entries("claude")
        for group, plugin in BUNDLE_GROUPS.items():
            with self.subTest(group=group):
                self.assertEqual(groups[group]["commit"], claude[plugin]["source"]["sha"],
                                 f"the Hermes bundle's {group} group is not the release the marketplace pins")

    def test_tags_exist_and_point_at_the_pinned_commit(self):
        for pname, entry in entries("claude").items():
            src = entry["source"]
            got = remote_tag_commit(src["repo"], src["ref"])
            if got is None:
                self.skipTest("GitHub is not reachable from here; the tag check needs the network")
            with self.subTest(plugin=pname):
                self.assertTrue(got, f"{src['repo']} has no tag {src['ref']}")
                self.assertEqual(got, src["sha"], f"{src['repo']} {src['ref']} points elsewhere")

    def test_guard_can_fail(self):
        good = {"name": "x", "version": "1.2.3",
                "source": {"source": "github", "repo": "o/x", "ref": "v1.2.3", "sha": "a" * 40}}
        self.assertEqual(pin_problems(good, True), [])
        self.assertTrue(pin_problems({**good, "source": {"source": "github", "repo": "o/x"}}, False))
        self.assertTrue(pin_problems({**good, "version": "1.2.4"}, False))
        self.assertTrue(pin_problems({**good, "source": {**good["source"], "sha": "abc"}}, True))
        self.assertTrue(pin_problems({**good, "source": "https://github.com/o/x"}, False))


if __name__ == "__main__":
    unittest.main()
