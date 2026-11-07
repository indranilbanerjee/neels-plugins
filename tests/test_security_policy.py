"""SECURITY.md describes this repository as it is.

The 2026-11-05 security review (finding 13): the policy said the repo "ships listing metadata, not
plugin code" while it ships the Hermes bundle (Python scripts included); its version table said 3.12.x
at 3.59.0; its scope and the `[CF Security]` subject were copied from ContentForge; the advisory link
labelled "the Neelverse marketplace" pointed at ContentForge; it named `~/.claude-marketing/<brand-slug>/`
for every plugin's data; and it called every connector the provider's official endpoint.

These checks keep it honest: the supported row names the current major.minor, the stale phrases stay
out, each advisory link points at the repository its label names, the Hermes bundle is in scope, and
SocialForge's key storage is described.

Stdlib only.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POLICY = REPO / "SECURITY.md"
STALE = ("not plugin code", "[CF Security]", "ships listing metadata", "the Neelverse marketplace](",
         "~/.claude-marketing/<brand-slug>/", "via the provider's official endpoint", "The CF plugin itself")
LINK_REPOS = {"Digital Marketing Pro": "digital-marketing-pro", "ContentForge": "contentforge",
              "SocialForge": "socialforge", "CutForge": "cutforge"}


def marketplace_version() -> str:
    doc = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    return (doc.get("metadata") or {}).get("version") or doc["version"]


def policy_problems(text: str, version: str) -> list[str]:
    out = []
    major_minor = ".".join(version.split(".")[:2])
    if not re.search(r"\|\s*" + re.escape(major_minor) + r"\.x\s*\|\s*✅", text):
        out.append(f"the supported row does not name {major_minor}.x")
    out += [f"stale text: {s!r}" for s in STALE if s in text]
    for label, repo in LINK_REPOS.items():
        for target in re.findall(r"\[" + re.escape(label) + r"\]\((https://[^)]+)\)", text):
            if f"/indranilbanerjee/{repo}/" not in target:
                out.append(f"the {label} link points at {target}")
    for needle in ("hermes/digital-marketing-pro", "socialforge-workspace", "keychain", "icacls", "_operator"):
        if needle not in text:
            out.append(f"does not mention {needle}")
    return out


class TestSecurityPolicy(unittest.TestCase):
    def test_policy_matches_the_repository(self):
        self.assertEqual(policy_problems(POLICY.read_text(encoding="utf-8"), marketplace_version()), [])

    def test_guard_can_fail(self):
        good = POLICY.read_text(encoding="utf-8")
        version = marketplace_version()
        self.assertTrue(policy_problems(good.replace(".x | ✅", ".y | ✅", 1), version))
        self.assertTrue(policy_problems(good + "\nThis repo ships listing metadata, not plugin code.", version))
        self.assertTrue(policy_problems(good.replace("/indranilbanerjee/socialforge/security",
                                                     "/indranilbanerjee/contentforge/security"), version))
        bumped = version.split(".")
        bumped[1] = str(int(bumped[1]) + 1)
        self.assertTrue(policy_problems(good, ".".join(bumped)), "a new minor must fail until the table moves")


if __name__ == "__main__":
    unittest.main()
