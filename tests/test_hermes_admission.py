"""Every suite plugin passes Hermes Agent's own admission validator.

Hermes runs an install-time security scan and refuses a plugin it rates
"dangerous"; its plugin catalog runs the same scan plus manifest, loadability
and capability checks (`hermes plugins validate`). On 2026-10-04 all three
suite plugins rated dangerous on harmless lines written like attacks, so a
Hermes user could not install any of them. Each plugin now carries a stdlib
guard for those patterns; this test runs the real validator, which only this
repo can do without making a plugin depend on Hermes.

It needs a Hermes source checkout and a Python environment with Hermes's
dependencies, given as HERMES_SRC (the checkout's root, with hermes_cli/,
agent/, tools/ and pm/) and HERMES_PYTHON (that environment's interpreter).
Without both it skips. The plugins are validated as installs see them: the
files git tracks at HEAD.
"""
from __future__ import annotations

import os
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent.parent
PLUGINS = {"digital-marketing-pro": ("digital-marketing-pro",),
           "contentforge": ("ContentForge", "contentforge"),
           "socialforge": ("SocialForge", "socialforge")}

PROBE = """
import json, sys
from pathlib import Path
from hermes_cli.plugin_validate import validate_plugin_dir
out = {}
for name in sys.argv[2:]:
    r = validate_plugin_dir(Path(sys.argv[1]) / name)
    out[name] = [f"{c}: {d}" for c, ok, d in r.checks if not ok]
print(json.dumps(out))
"""


def _checkout(names):
    for n in names:
        if (SUITE_ROOT / n / ".git").exists():
            return SUITE_ROOT / n
    return None


@unittest.skipUnless(os.environ.get("HERMES_SRC") and os.environ.get("HERMES_PYTHON"),
                     "set HERMES_SRC and HERMES_PYTHON to run Hermes's own validator")
class TestHermesAdmission(unittest.TestCase):
    def test_every_plugin_passes_hermes_validate(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            present = []
            for name, dirs in PLUGINS.items():
                repo = _checkout(dirs)
                if repo is None:
                    continue
                archive = Path(tmp) / f"{name}.tar"
                subprocess.run(["git", "archive", "-o", str(archive), "HEAD"], cwd=repo, check=True)
                with tarfile.open(archive) as tf:
                    tf.extractall(Path(tmp) / name)
                present.append(name)
            if not present:
                self.skipTest("no plugin repo is checked out beside the marketplace")
            env = dict(os.environ, PYTHONPATH=os.environ["HERMES_SRC"], PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run([os.environ["HERMES_PYTHON"], "-c", PROBE, tmp, *present],
                                  capture_output=True, text=True, env=env, timeout=900)
            self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
            failures = {k: v for k, v in json.loads(proc.stdout.strip().splitlines()[-1]).items() if v}
            self.assertEqual(failures, {}, f"Hermes would refuse these: {failures}")


if __name__ == "__main__":
    unittest.main()
