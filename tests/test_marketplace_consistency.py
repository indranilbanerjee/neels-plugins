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

# Each platform reads a different file; all five describe the same three plugins.
MANIFESTS = {
    "claude": REPO / ".claude-plugin" / "marketplace.json",
    "cursor": REPO / ".cursor-plugin" / "marketplace.json",
    "codex": REPO / ".agents" / "plugins" / "marketplace.json",
    "copilot": REPO / ".github" / "plugin" / "marketplace.json",
    "grok": REPO / ".grok-plugin" / "marketplace.json",
}
# The Codex and Grok variants intentionally carry no top-level marketplace
# version (Grok's format, per the in-the-wild xAI examples, has no metadata block).
VERSIONED = ("claude", "cursor", "copilot")


def load(name):
    return json.loads(MANIFESTS[name].read_text(encoding="utf-8"))


def marketplace_version(doc):
    return (doc.get("metadata") or {}).get("version") or doc.get("version")


def plugins(doc):
    return {p["name"]: p for p in doc.get("plugins", [])}


class TestManifestsParse(unittest.TestCase):
    def test_all_five_parse(self):
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

    def test_plugin_versions_agree_across_all_five(self):
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

    def test_grok_variant_has_no_marketplace_version(self):
        """Deliberate: Grok's marketplace format (mirroring the in-the-wild xAI
        examples) carries only per-plugin versions."""
        self.assertIsNone(marketplace_version(load("grok")),
                          "the Grok manifest should not declare a marketplace version")


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
        """The exact regression that shipped: '21 skills' / '35-pattern' outliving the plugin.
        2026-08-17: '41-pattern' joined the list — it outlived the v3.20.0 catalog
        growth to 43 by four weeks, in all four manifests at once."""
        retired = ("35-pattern", "35 patterns", "21 skills", "29-pattern",
                   "41-pattern", "41 patterns")
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
                # Claude-family manifests use {"source": "github", "repo": ...};
                # the Grok format uses {"source": "url", "url": "...git"}.
                repo = (src.get("repo") or src.get("url")) if isinstance(src, dict) else src
                with self.subTest(manifest=name, plugin=pname):
                    self.assertIsNotNone(repo, f"{name}/{pname}: no source repo")
                    self.assertIn(expected[pname], str(repo),
                                  f"{name}/{pname} points at {repo}")


def _sibling(name):
    """Locate a sibling plugin repo checkout regardless of directory-name case.
    Returns None when the sibling is not checked out (e.g. marketplace-only CI)."""
    parent = REPO.parent
    for d in parent.iterdir():
        if d.is_dir() and d.name.lower() == name.lower():
            return d
    return None


class TestReadmeLiveness(unittest.TestCase):
    """The README rotted for six weeks while every manifest guard passed: the lede
    still announced the July 7 release, the suite badges said 196 skills / 502 tests
    against a 205-skill / 1,100+-test reality, and the plugin table advertised
    '21 skills · 35-pattern' — the exact regression TestListingDescriptions was
    built for, alive in the one file that test never read."""

    @classmethod
    def setUpClass(cls):
        cls.readme = (REPO / "README.md").read_text(encoding="utf-8")
        cls.canonical = marketplace_version(load("claude"))
        # Everything before "## What's new" is live listing surface; the entries
        # below it narrate past releases and keep their ship-time numbers.
        cls.live = cls.readme.split("## What's new")[0]

    def test_lede_names_the_current_release(self):
        m = re.search(r"^> 🆕.*$", self.readme, re.M)
        self.assertIsNotNone(m, "README lost its '> 🆕' lede line")
        self.assertIn(self.canonical, m.group(0),
                      "the lede announces an old release — it must name marketplace "
                      f"v{self.canonical} (the CHANGELOG top entry)")

    def test_no_retired_branding_in_live_sections(self):
        retired = ("35-pattern", "35 patterns", "29-pattern", "41-pattern", "21 skills",
                   "16 skills", "158 skills", "196%20across", "502%20across")
        for needle in retired:
            with self.subTest(needle=needle):
                self.assertNotIn(needle, self.live,
                                 f"README live section still says '{needle}'")

    def test_suite_skills_badge_matches_sibling_truth(self):
        sibs = [_sibling(n) for n in ("contentforge", "digital-marketing-pro", "socialforge")]
        if not all(sibs):
            self.skipTest("sibling repos not checked out beside the marketplace")
        truth = sum(len([d for d in (s / "skills").iterdir() if d.is_dir()]) for s in sibs)
        m = re.search(r"badge/skills-(\d+)%20across%20suite", self.readme)
        self.assertIsNotNone(m, "suite skills badge not found in README")
        self.assertEqual(int(m.group(1)), truth,
                         f"skills badge says {m.group(1)}, the three repos ship {truth}")

    def test_suite_tests_badge_matches_changelog(self):
        """The CHANGELOG top entries record 'Suite total N' at each release; the badge
        must agree with the most recent such record."""
        changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
        rec = re.search(r"Suite total ([\d,]+)", changelog)
        self.assertIsNotNone(rec, "CHANGELOG no longer records 'Suite total N'")
        recorded = int(rec.group(1).replace(",", ""))
        m = re.search(r"badge/tests-([\d,%C]+?)%20across%20suite", self.readme)
        self.assertIsNotNone(m, "suite tests badge not found in README")
        badge = int(re.sub(r"[^\d]", "", m.group(1)))
        self.assertEqual(badge, recorded,
                         f"tests badge says {badge}, CHANGELOG's latest record is {recorded}")

    def test_plugin_table_rows_match_sibling_truth(self):
        for repo_name, display in (("contentforge", "contentforge"),
                                   ("digital-marketing-pro", "digital-marketing-pro"),
                                   ("socialforge", "socialforge")):
            sib = _sibling(repo_name)
            if sib is None:
                self.skipTest("sibling repos not checked out beside the marketplace")
            truth = len([d for d in (sib / "skills").iterdir() if d.is_dir()])
            row = next((ln for ln in self.live.splitlines()
                        if display in ln and "skills" in ln and ln.strip().startswith("|")), None)
            self.assertIsNotNone(row, f"README table lost the {display} row")
            m = re.search(r"(\d+) skills", row)
            self.assertIsNotNone(m, f"{display} row states no skill count")
            with self.subTest(plugin=display):
                self.assertEqual(int(m.group(1)), truth,
                                 f"{display} row says {m.group(0)}, the repo ships {truth}")


class TestChangelogCoverage(unittest.TestCase):
    """The CHANGELOG silently stopped at 3.16.0 while the manifests marched to
    3.26.0 — ten unchronicled releases in the repo whose entire job is keeping
    listing metadata honest. This guard makes that impossible: the canonical
    manifest version must appear as a CHANGELOG heading before it can ship."""

    def test_manifest_version_has_a_changelog_entry(self):
        manifest = json.loads(MANIFESTS["claude"].read_text(encoding="utf-8"))
        canonical = manifest.get("metadata", {}).get("version") or manifest.get("version")
        changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
        headings = re.findall(r"^## \[([^\]]+)\]", changelog, re.M)
        self.assertIn(canonical, headings,
                      f"marketplace.json is v{canonical} but CHANGELOG.md has no "
                      f"'## [{canonical}]' entry — chronicle the release before shipping it.")


if __name__ == "__main__":
    unittest.main()
