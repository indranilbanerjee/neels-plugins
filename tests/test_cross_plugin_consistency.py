"""Independent copies drift. This is the only repo allowed to notice.

The self-containment rule forbids a plugin from importing a sibling, so
ContentForge and Digital Marketing Pro each carry their OWN copy of the
structural-tell scan and the authorship matcher. That rule is right — a plugin
must work standalone — but it has a cost: two implementations of one
specification, maintained by hand, with nothing comparing them.

Neither plugin's test suite can catch that drift without violating the rule it
is meant to protect. The marketplace repo can: its whole job is the three
plugins together. So the drift guard lives here.

A failure means the two copies now answer differently for the same document.
Fix by porting the change across, not by loosening this test.

Skips cleanly when the sibling repos are not checked out beside this one.
"""
from __future__ import annotations

import importlib.util

import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent.parent
CF = SUITE_ROOT / "contentforge"
DMP = SUITE_ROOT / "digital-marketing-pro"

# Findings both copies must produce, with identical numbers.
SHARED_FINDINGS = ("moralizing", "section_symmetry", "parallel_headings",
                   "specificity", "stance", "paragraph_evenness",
                   "entity_development")

NUMERIC_KEYS = ("per_1000_words", "coefficient_of_variation", "mentions_per_entity",
                "distinct_entities", "max_identical_pattern_share",
                "single_mention_share", "distinct_per_1000_words")

DOCUMENTS = {
    "ai_shaped": (
        "# The Guide\n\n## Understanding The Basics\n\n"
        "In today's landscape, businesses must delve into the intricate tapestry of "
        "modern marketing. It is important to remember that success typically requires "
        "planning. Ultimately, this matters because preparation wins.\n\n"
        "## Building The Foundation\n\n"
        "Organizations may generally benefit from best practices that can usually "
        "improve outcomes. In conclusion, the key takeaway is that preparation wins.\n"),
    "human_shaped": (
        "# What 14 months of cold email taught us\n\n"
        "## The $4,300 mistake\n\n"
        "I spent Q3 2025 sending 11,000 cold emails for Acme Robotics. Open rate: 61%. "
        "Meetings booked: 4.\n\nFour.\n\n"
        "Our consultant, Priya Sharma, put it bluntly: \"You optimized the wrong stage.\"\n\n"
        "## Why the 61% was a trap\n\n"
        "Opens measure subject lines. Meetings measure the offer. HubSpot's 2026 report "
        "puts reply-to-meeting near 9% for B2B SaaS; we were at 2.1%.\n"),
    "adversarial_empty": "",
    "adversarial_unicode": "# 🎯 Résumé\n\nLe café naïve 日本語 Ελληνικά مرحبا 31 days.\n",
    "adversarial_fence": "# D\n\n```py\nprint(1)\n\nAfter the fence.\n",
    # Long enough (>=600 words) and entity-dense enough (>=12 distinct) that the
    # entity_development band is LIVE rather than suppressed by the measurability
    # floor. Without a document in this shape a threshold change on one side
    # produces no visible difference and the drift guard silently passes.
    "entity_churn_measurable": "# Report\n\n## Findings\n\n" + " ".join(
        f"The {n} team logged a shift that quarter and staff there noted the change soon afterwards. "
        f"Analysts called the pattern broadly consistent with the prior period across that whole region. "
        f"Nobody involved disputed the summary that was circulated to the group later that same month. "
        for n in ("Fraunhofer", "Siemens", "Duisburg", "Stuttgart", "Hoffmann", "Weber",
                  "Leipzig", "Kessler", "Hannover", "Baumann", "Dortmund", "Vogel",
                  "Essen", "Bremen", "Aachen", "Kiel", "Rostock", "Ulm", "Trier", "Jena")),
    # Same length, but the specifics recur — lands on the other side of the band.
    "entity_dwell_measurable": "# Report\n\n## Findings\n\n" + (
        "The Fraunhofer report tracked review delays across Bavaria and Saxony through 2024. "
        "Fraunhofer found the Bavaria median rose from 14 days to 31 days while Saxony held near 18. "
        "Kessler Partners audited the same Bavaria cohort and reached the 31-day figure independently. "
        "Reviewers at Bavaria described the backlog to Kessler Partners during 2024. "
        "By 2025 the Bavaria median settled at 28 days, still double the Fraunhofer baseline of 14. "
    ) * 8,
}


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless((CF / "scripts" / "text-metrics.py").is_file()
                     and (DMP / "scripts" / "structural-tell-scan.py").is_file(),
                     "sibling plugin repos not checked out beside this one")
class TestStructuralScanCopiesAgree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cf = _load("cf_text_metrics", CF / "scripts" / "text-metrics.py")
        cls.dmp = _load("dmp_structural", DMP / "scripts" / "structural-tell-scan.py")

    def test_same_findings_present_in_both(self):
        for name, doc in DOCUMENTS.items():
            with self.subTest(doc=name):
                a = set(self.cf.structure_scan(doc)["findings"])
                b = set(self.dmp.structure_scan(doc)["findings"])
                self.assertEqual(a, b, f"finding sets diverged: CF-only={a-b}, DMP-only={b-a}")
                self.assertTrue(set(SHARED_FINDINGS) <= a,
                                f"a documented finding vanished: {set(SHARED_FINDINGS) - a}")

    def test_identical_numbers_and_bands(self):
        for name, doc in DOCUMENTS.items():
            a, b = self.cf.structure_scan(doc), self.dmp.structure_scan(doc)
            with self.subTest(doc=name):
                self.assertEqual(a["words_analyzed"], b["words_analyzed"])
                self.assertEqual(a["overall"], b["overall"])
                for key in SHARED_FINDINGS:
                    fa, fb = a["findings"][key], b["findings"][key]
                    self.assertEqual(fa["band"], fb["band"], f"{key}: band drift")
                    for num in NUMERIC_KEYS:
                        if num in fa or num in fb:
                            self.assertEqual(fa.get(num), fb.get(num),
                                             f"{key}.{num}: value drift")

    def test_entity_development_measurability_rule_matches(self):
        """Both copies must stay silent on the same short documents."""
        for name, doc in DOCUMENTS.items():
            with self.subTest(doc=name):
                a = self.cf.structure_scan(doc)["findings"]["entity_development"]
                b = self.dmp.structure_scan(doc)["findings"]["entity_development"]
                self.assertEqual(a["measurable"], b["measurable"])

    def test_the_corpus_actually_exercises_every_band(self):
        """Guard on the guard. A drift check whose documents never reach a live
        band cannot detect a threshold change — the first version of this file
        passed a planted threshold drift for exactly that reason. Assert the
        corpus spans the bands it claims to police."""
        seen = {}
        for doc in DOCUMENTS.values():
            for key, f in self.cf.structure_scan(doc)["findings"].items():
                seen.setdefault(key, set()).add(f["band"])
        self.assertTrue(seen["entity_development"] & {"NOTE", "ATTENTION"},
                        "no document drives entity_development off OK — a threshold "
                        "change there would slip past this suite")
        measurable = [self.cf.structure_scan(d)["findings"]["entity_development"]["measurable"]
                      for d in DOCUMENTS.values()]
        self.assertIn(True, measurable, "no document is long/dense enough to be measurable")
        self.assertIn(False, measurable, "no document exercises the measurability floor")

    def test_band_threshold_tables_are_identical(self):
        """The most direct drift check available: compare the tables themselves,
        not only their effect on a sample. Catches a threshold edit even where
        no test document happens to straddle it."""
        self.assertEqual(self.cf._BANDS, self.dmp._BANDS,
                         "structural band thresholds drifted between the two copies")
        self.assertEqual(set(self.cf._LOWER_IS_WORSE), set(self.dmp._LOWER_IS_WORSE),
                         "band direction drifted between the two copies")


@unittest.skipUnless((CF / "scripts" / "authorship.py").is_file()
                     and (DMP / "scripts" / "authorship.py").is_file(),
                     "sibling plugin repos not checked out beside this one")
class TestAuthorshipCopiesAgree(unittest.TestCase):
    SRC = ("ok so the thing that killed us was the 14 day estimate. we quoted it for two years.\n"
           "i found out in march when the bavaria client missed their launch window.\n"
           "we lost about 40k in rework on that one account alone.\n")
    PRESERVED = ("# T\n\nok so the thing that killed us was the 14 day estimate. we quoted it for two years.\n\n"
                 "A researched sentence was added between theirs for context.\n\n"
                 "i found out in march when the bavaria client missed their launch window.\n\n"
                 "we lost about 40k in rework on that one account alone.\n")
    LAUNDERED = ("# T\n\nThe critical issue was the 14-day estimate. We quoted it for two years.\n\n"
                 "I discovered this in March, when the Bavaria client missed their launch window.\n")

    @classmethod
    def setUpClass(cls):
        cls.cf = _load("cf_authorship", CF / "scripts" / "authorship.py")
        cls.dmp = _load("dmp_authorship", DMP / "scripts" / "authorship.py")

    def test_thresholds_match(self):
        for const in ("NEAR_MATCH", "VERBATIM", "AUTHORED_WORD_SHARE_FLOOR"):
            self.assertEqual(getattr(self.cf, const), getattr(self.dmp, const),
                             f"{const} drifted between the two copies")

    def test_verdicts_match(self):
        for label, draft in (("preserved", self.PRESERVED), ("laundered", self.LAUNDERED)):
            a = self.cf.classify(self.SRC, draft)
            b = self.dmp.classify(self.SRC, draft)
            with self.subTest(case=label):
                self.assertEqual(a["counts"], b["counts"])
                self.assertEqual(a["violations"], b["violations"])
                self.assertEqual(a["author_word_share"], b["author_word_share"])
                self.assertEqual(a["may_claim_authored"], b["may_claim_authored"])

    def test_both_refuse_to_overclaim_on_a_violated_draft(self):
        for mod in (self.cf, self.dmp):
            self.assertFalse(mod.classify(self.SRC, self.LAUNDERED)["may_claim_authored"])


if __name__ == "__main__":
    unittest.main()
