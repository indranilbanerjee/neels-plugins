"""The marketplace manifests must agree with each other, with the README, and with
the plugin repositories they list.

This repo ships listing metadata, and that metadata is what someone reads *before*
they install anything. It has gone wrong twice in ways nothing caught:

  - the ContentForge listing advertised "21 skills, 35-pattern AI humanizer" for two
    releases after the plugin shipped 22 skills and a 41-pattern catalog, in all four
    manifests at once
  - the README version badge said 3.21.2 while the manifests said 3.21.3

Neither was detectable because this repo had no tests. These are the guards.

Stdlib only. Run with: python tests/run_all.py
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Each platform reads a different file; all four describe the same three plugins.
MANIFESTS = {
    "claude": REPO / ".claude-plugin" / "marketplace.json",
    "cursor": REPO / ".cursor-plugin" / "marketplace.json",
    "codex": REPO / ".agents" / "plugins" / "marketplace.json",
    "copilot": REPO / ".github" / "plugin" / "marketplace.json",
}
# The Codex variant intentionally carries no top-level marketplace version.
VERSIONED = ("claude", "cursor", "copilot")


def load(name):
    return json.loads(MANIFESTS[name].read_text(encoding="utf-8"))


def marketplace_version(doc):
    return (doc.get("metadata") or {}).get("version") or doc.get("version")


def plugins(doc):
    return {p["name"]: p for p in doc.get("plugins", [])}


class TestManifestsParse(unittest.TestCase):
    def test_all_four_parse(self):
        for name, path in MANIFESTS.items():
            with self.subTest(manifest=name):
                self.assertTrue(path.exists(), f"{path} is missing")
                json.loads(path.read_text(encoding="utf-8"))

    def test_hard_rules(self):
        """v2.8.0: `repository` must be a string URL; no top-level `$schema`."""
        for name in MANIFESTS:
            doc = load(name)
            with self.subTest(manifest=name):
                self.assertNotIn("$schema", doc, f"{name}: top-level $schema is forbidden")
                for pname, p in plugins(doc).items():
                    repo = p.get("repository")
                    if repo is not None:
                        self.assertIsInstance(
                            repo, str, f"{name}/{pname}: repository must be a string URL")


class TestCrossManifestAgreement(unittest.TestCase):
    def test_same_plugin_set(self):
        sets = {n: set(plugins(load(n))) for n in MANIFESTS}
        first = sets["claude"]
        for name, s in sets.items():
            self.assertEqual(s, first, f"{name} lists {s}, claude lists {first}")

    def test_plugin_versions_agree_across_all_four(self):
        by_plugin = {}
        for name in MANIFESTS:
            for pname, p in plugins(load(name)).items():
                by_plugin.setdefault(pname, {})[name] = p.get("version")
        for pname, versions in by_plugin.items():
            with self.subTest(plugin=pname):
                self.assertEqual(
                    len(set(versions.values())), 1,
                    f"{pname} version disagrees across manifests: {versions}")

    def test_marketplace_version_agrees(self):
        versions = {n: marketplace_version(load(n)) for n in VERSIONED}
        self.assertEqual(len(set(versions.values())), 1,
                         f"marketplace version disagrees: {versions}")

    def test_codex_variant_has_no_marketplace_version(self):
        """Deliberate: the .agents/ variant carries only per-plugin versions."""
        self.assertIsNone(marketplace_version(load("codex")),
                          "the Codex manifest should not declare a marketplace version")


class TestReadmeMatchesManifests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (REPO / "README.md").read_text(encoding="utf-8")
        cls.canonical = marketplace_version(load("claude"))

    def test_version_badge_matches(self):
        m = re.search(r"badge/version-(\d+\.\d+\.\d+)", self.readme)
        self.assertIsNotNone(m, "version badge not found in README")
        self.assertEqual(m.group(1), self.canonical,
                         f"README badge {m.group(1)} != manifest {self.canonical}")

    def test_every_listed_plugin_is_mentioned(self):
        for pname in plugins(load("claude")):
            self.assertIn(pname, self.readme, f"README never mentions {pname}")


class TestListingDescriptions(unittest.TestCase):
    """Descriptions are read at install time — the most-read text this repo owns."""

    def test_descriptions_present_and_identical_across_manifests(self):
        by_plugin = {}
        for name in MANIFESTS:
            for pname, p in plugins(load(name)).items():
                desc = p.get("description", "")
                self.assertTrue(desc.strip(), f"{name}/{pname}: empty description")
                by_plugin.setdefault(pname, {})[name] = desc
        for pname, descs in by_plugin.items():
            with self.subTest(plugin=pname):
                self.assertEqual(
                    len(set(descs.values())), 1,
                    f"{pname}: description differs between manifests, so different "
                    f"platforms show different install-time text")

    def test_no_retired_contentforge_branding(self):
        """The exact regression that shipped: '21 skills' / '35-pattern' outliving the plugin."""
        retired = ("35-pattern", "35 patterns", "21 skills", "29-pattern")
        for name in MANIFESTS:
            cf = plugins(load(name)).get("contentforge", {})
            desc = cf.get("description", "")
            for needle in retired:
                with self.subTest(manifest=name, needle=needle):
                    self.assertNotIn(needle, desc,
                                     f"{name}: ContentForge description still says '{needle}'")

    def test_source_repos_are_the_expected_ones(self):
        expected = {
            "digital-marketing-pro": "indranilbanerjee/digital-marketing-pro",
            "contentforge": "indranilbanerjee/contentforge",
            "socialforge": "indranilbanerjee/socialforge",
        }
        for name in MANIFESTS:
            for pname, p in plugins(load(name)).items():
                src = p.get("source")
                repo = src.get("repo") if isinstance(src, dict) else src
                with self.subTest(manifest=name, plugin=pname):
                    self.assertIsNotNone(repo, f"{name}/{pname}: no source repo")
                    self.assertIn(expected[pname], str(repo),
                                  f"{name}/{pname} points at {repo}")


if __name__ == "__main__":
    unittest.main()
