"""Each standalone hero skill still matches the plugin it was extracted from.

The hero repos (contentforge-humanizer, digital-marketing-pro-agent-readiness,
socialforge-copy-adapter) each copy a script out of a suite plugin so the skill
runs with nothing around it. Each hero's own tests carry parity tests against
its source plugin, but those run only when someone runs that hero's suite with
the plugin checked out beside it. Nothing ran them when the plugin changed.

This repo is the one place that tests the family together, so it runs every
hero's suite against the current plugin checkout and fails if the suite fails
or if any parity test was skipped (a skipped parity test proves nothing).

Skips cleanly when a hero or its plugin is not checked out beside this repo.
"""
from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent.parent
HEROES_ROOT = SUITE_ROOT / "heroes"


def _first_existing(*names: str) -> Path | None:
    for n in names:
        p = SUITE_ROOT / n
        if p.is_dir():
            return p
    return None


# hero folder -> (env var its parity tests read, candidate plugin folder names)
HEROES = {
    "contentforge-humanizer": ("CONTENTFORGE_DIR", ("ContentForge", "contentforge")),
    "digital-marketing-pro-agent-readiness": ("DMP_DIR", ("digital-marketing-pro",)),
    "socialforge-copy-adapter": ("SOCIALFORGE_DIR", ("SocialForge", "socialforge")),
}

HAS_PYTEST = importlib.util.find_spec("pytest") is not None


def run_hero_suite(hero: Path, env_var: str, plugin: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, **{env_var: str(plugin)}, PYTHONDONTWRITEBYTECODE="1")
    if HAS_PYTEST:
        cmd = [sys.executable, "-B", "-m", "pytest", "tests", "-q", "-rs", "-p", "no:cacheprovider"]
    else:
        cmd = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"]
    return subprocess.run(cmd, cwd=hero, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=900)


def skipped_count(output: str) -> int:
    m = re.search(r"(\d+) skipped", output)
    if m:
        return int(m.group(1))
    m = re.search(r"OK \(skipped=(\d+)\)", output)
    return int(m.group(1)) if m else 0


class TestHeroParity(unittest.TestCase):
    def _check(self, name: str):
        env_var, plugin_names = HEROES[name]
        hero = HEROES_ROOT / name
        plugin = _first_existing(*plugin_names)
        if not (hero / "tests").is_dir() or plugin is None:
            self.skipTest(f"{name} or its plugin is not checked out beside the marketplace")
        proc = run_hero_suite(hero, env_var, plugin)
        out = proc.stdout + proc.stderr
        self.assertEqual(proc.returncode, 0, f"{name}'s suite fails against {plugin.name}:\n{out[-3000:]}")
        self.assertEqual(skipped_count(out), 0,
                         f"{name}: tests were skipped although {plugin.name} is present, "
                         f"so parity was not proven:\n{out[-2000:]}")

    def test_contentforge_humanizer(self):
        self._check("contentforge-humanizer")

    def test_digital_marketing_pro_agent_readiness(self):
        self._check("digital-marketing-pro-agent-readiness")

    def test_socialforge_copy_adapter(self):
        self._check("socialforge-copy-adapter")

    def test_skip_counter_reads_both_runners(self):
        self.assertEqual(skipped_count("34 passed, 2 skipped in 3.1s"), 2)
        self.assertEqual(skipped_count("Ran 9 tests\n\nOK (skipped=3)"), 3)
        self.assertEqual(skipped_count("96 passed in 10.7s"), 0)


if __name__ == "__main__":
    unittest.main()
