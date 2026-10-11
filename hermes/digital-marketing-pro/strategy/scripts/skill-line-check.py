#!/usr/bin/env python3
"""
skill-line-check.py
===================
CI guard for the Claude Code "Keep SKILL.md under 500 lines" guideline.

Walks every skills/*/SKILL.md and prints a report. Exits non-zero if any
SKILL.md exceeds the configured threshold (default 500 lines).

Used by:
- pre-commit-style CI on push
- /digital-marketing-pro:doctor extended diagnostic
- ad-hoc local sanity check before bumping a release

Usage:
    python scripts/skill-line-check.py              # default threshold 500
    python scripts/skill-line-check.py --max 400    # tighter limit
    python scripts/skill-line-check.py --json       # machine-readable
    python scripts/skill-line-check.py --warn-at 400 --error-at 500

Why this matters: SKILL.md content stays in context across turns once
loaded. Auto-compaction re-attaches the most-recent invocation but only
the first 5,000 tokens of it. A skill that grows past ~500 lines (roughly
4,000-6,000 tokens depending on density) starts losing its tail content
after the first compaction.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PLUGIN_ROOT / "skills"


def collect_skill_sizes() -> list[dict]:
    out = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            text = skill_md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
        out.append({
            "skill": skill_dir.name,
            "path": str(skill_md.relative_to(PLUGIN_ROOT)),
            "lines": lines,
            "bytes": len(text.encode("utf-8")),
        })
    out.sort(key=lambda r: r["lines"], reverse=True)
    return out


def report(rows: list[dict], warn_at: int, error_at: int, as_json: bool) -> int:
    warn_rows = [r for r in rows if warn_at <= r["lines"] < error_at]
    error_rows = [r for r in rows if r["lines"] >= error_at]

    if as_json:
        print(json.dumps({
            "total_skills": len(rows),
            "warn_threshold": warn_at,
            "error_threshold": error_at,
            "warnings": warn_rows,
            "errors": error_rows,
            "top_10": rows[:10],
        }, indent=2))
        return 1 if error_rows else 0

    print(f"Scanned {len(rows)} skills.")
    print(f"  warn at >= {warn_at} lines,  error at >= {error_at} lines")
    print()
    print("Top 10 heaviest SKILL.md files:")
    print(f"  {'LINES':>6}  {'BYTES':>7}  SKILL")
    for r in rows[:10]:
        status = "  "
        if r["lines"] >= error_at:
            status = "EE"
        elif r["lines"] >= warn_at:
            status = "WW"
        print(f"  {r['lines']:>6}  {r['bytes']:>7}  {status} {r['skill']}")
    print()
    if warn_rows:
        print(f"WARNINGS ({len(warn_rows)}):")
        for r in warn_rows:
            print(f"  {r['skill']}: {r['lines']} lines (approaching threshold)")
        print()
    if error_rows:
        print(f"ERRORS ({len(error_rows)}):")
        for r in error_rows:
            print(f"  {r['skill']}: {r['lines']} lines (over threshold; split into references/)")
        print()
        print("Fix: move detailed reference material to separate files under the skill's")
        print("directory and reference them from SKILL.md so they only load when needed.")
        return 1
    print("All skills under threshold. Good.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--warn-at", type=int, default=400,
                        help="Lines at which to warn (default: 400)")
    parser.add_argument("--error-at", type=int, default=500,
                        help="Lines at which to fail (default: 500)")
    parser.add_argument("--max", type=int, default=None,
                        help="Shorthand: sets both warn-at and error-at to this value")
    parser.add_argument("--json", action="store_true",
                        help="Machine-readable JSON output")
    args = parser.parse_args()

    warn_at = args.warn_at
    error_at = args.error_at
    if args.max is not None:
        warn_at = args.max
        error_at = args.max

    rows = collect_skill_sizes()
    return report(rows, warn_at, error_at, args.json)


if __name__ == "__main__":
    sys.exit(main())
