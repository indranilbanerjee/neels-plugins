#!/usr/bin/env python3
"""
benchmark_book.py — Market benchmarks with provenance, never bare numbers from memory.

WHY THIS EXISTS
---------------
DMP's skill docs carried hundreds of auction-priced figures — "LinkedIn CPMs
are high ($30–$60)", "Expect $30–$150 CPL", per-industry CPC tables — written
as current market fact with no date and no source. Auction prices drift
continuously; a range that was honest when written becomes a confident lie a
year later, and a media plan built on it inherits the lie with interest.
The suite already learned this lesson once with AI-provider pricing — numbers
enter with a source URL and stale quotes are refused — and this module applies
the same contract to *market* benchmarks: CPM, CPC, CPL, CPA, CPE, creator
rates, tool subscription fees.

THE CONTRACT
------------
1. A benchmark enters only via `record`, which REQUIRES a source URL and
   carries an as-of date (defaulting to the day of the lookup). No seed table
   ships in this file — every number was put here by a lookup that recorded
   where it came from.
2. `quote` returns a status, never a bare number. fresh (≤90 days) quotes
   cleanly; aging (≤365 days) quotes with an explicit warning the caller must
   surface; stale (>365 days) or absent REFUSES (exit 3) and names exactly
   what to look up. It will not guess and will not quietly reuse a dead figure.
3. A benchmark is a property of METRIC × CHANNEL × SEGMENT. LinkedIn CPM for
   B2B SaaS is not Meta CPM for DTC skincare; a single global "average CPM"
   is always wrong somewhere. Segment defaults to "all" when a metric is
   genuinely channel-wide.
4. Shipped doc figures are PLANNING PRIORS, not quotes. Skill docs that carry
   ranges are banner-stamped with their as-of month (enforced by
   tests/test_benchmark_provenance.py); anything entering a media plan, budget
   or client deliverable must come from this book or a live lookup.

HOW A BENCHMARK GETS IN
-----------------------
The agent looks it up — with the harness's own web tools, the user's already-
connected analytics/ads tools, or the brand's own platform exports (first-party
actuals beat published averages every time; record those with the dashboard URL
as source). Then:

    python benchmark_book.py --action record --metric cpm --channel linkedin \
        --segment b2b --low 30 --high 60 --source https://example.com/2026-benchmarks

    python benchmark_book.py --action quote --metric cpm --channel linkedin --segment b2b

Stdlib only. No network calls happen in here by design — the fetching layer is
the agent's, so numbers are as fresh as the lookup that found them and never as
stale as a table someone forgot to update.

Exit codes:
    0  recorded / quoted (fresh or aging) / listed
    2  bad input (missing source, malformed date, unknown action)
    3  quote refused — benchmark absent or stale; output names what to look up
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import ensure_utf8_stdout, workspace_root  # noqa: E402

BOOK_FILENAME = "benchmark-book.json"

FRESH_DAYS = 90    # quote cleanly
AGING_DAYS = 365   # quote with a warning the caller must surface; older = refuse

# Metrics this book understands, with the default unit each records in.
# This is a vocabulary, not a price list — there are no values here.
METRICS = {
    "cpm":  "usd_per_1000_impressions",
    "cpc":  "usd_per_click",
    "cpl":  "usd_per_lead",
    "cpa":  "usd_per_acquisition",
    "cpe":  "usd_per_engagement",
    "cpv":  "usd_per_view",
    "cpi":  "usd_per_install",
    "cpcv": "usd_per_completed_view",
    "creator-rate": "usd_per_post",
    "tool-subscription": "usd_per_month",
    "ctr":  "percent",
    "cvr":  "percent",
    "engagement-rate": "percent",
}


def book_path() -> Path:
    return workspace_root() / BOOK_FILENAME


def _load() -> dict:
    p = book_path()
    if not p.exists():
        return {"entries": {}}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # A corrupt book must never silently become an empty one — that would
        # erase provenance. Surface it and stop.
        raise ValueError(f"Corrupt benchmark book at {p}; fix or remove it explicitly.")


def _save(book: dict) -> None:
    p = book_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(book, indent=2, ensure_ascii=False), encoding="utf-8")


def _key(metric: str, channel: str, segment: str) -> str:
    return f"{metric}|{channel}|{segment}"


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9.+-]+", "-", s.strip().lower()).strip("-")


def _age_days(as_of: str) -> int:
    d = datetime.strptime(as_of, "%Y-%m-%d").date()
    return (date.today() - d).days


def _status_for_age(age: int) -> str:
    if age <= FRESH_DAYS:
        return "fresh"
    if age <= AGING_DAYS:
        return "aging"
    return "stale"


def record(metric: str, channel: str, segment: str, low: float, high: float,
           source: str, as_of: str | None = None, unit: str | None = None,
           note: str | None = None) -> dict:
    """Record a looked-up benchmark. Source URL is non-negotiable."""
    metric = _norm(metric)
    if metric not in METRICS:
        raise ValueError(
            f"Unknown metric {metric!r}. Known: {', '.join(sorted(METRICS))}")
    if not source or not re.match(r"^https?://", source):
        raise ValueError(
            "A benchmark cannot enter the book without a source URL "
            "(the page or dashboard the number was read from).")
    if low > high:
        raise ValueError(f"low ({low}) must not exceed high ({high}).")
    as_of = as_of or date.today().isoformat()
    _age_days(as_of)  # validates the format
    entry = {
        "metric": metric,
        "channel": _norm(channel),
        "segment": _norm(segment) or "all",
        "low": low,
        "high": high,
        "unit": unit or METRICS[metric],
        "source": source,
        "as_of": as_of,
        "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if note:
        entry["note"] = note
    book = _load()
    book["entries"][_key(entry["metric"], entry["channel"], entry["segment"])] = entry
    _save(book)
    return entry


def quote(metric: str, channel: str, segment: str = "all") -> tuple[dict, int]:
    """Return (payload, exit_code). Never a bare number: the payload always
    carries status + provenance, and refusal names the lookup to run."""
    metric, channel, segment = _norm(metric), _norm(channel), _norm(segment or "all")
    book = _load()
    entry = book["entries"].get(_key(metric, channel, segment))
    if entry is None and segment != "all":
        # Fall back to the channel-wide figure, saying so.
        entry = book["entries"].get(_key(metric, channel, "all"))
        if entry:
            entry = dict(entry, segment_fallback=f"no {segment!r} entry; channel-wide figure")
    lookup_hint = (
        f"No usable {metric.upper()} benchmark for {channel}"
        f"{'' if segment == 'all' else ' (' + segment + ')'}. Look it up live — "
        "current published benchmark reports, the platform's own planning tools, "
        "or the brand's dashboard actuals (best) — then record it with "
        "--action record (source URL required). Do not estimate from memory."
    )
    if entry is None:
        return ({"status": "absent", "metric": metric, "channel": channel,
                 "segment": segment, "action_required": lookup_hint}, 3)
    age = _age_days(entry["as_of"])
    status = _status_for_age(age)
    payload = dict(entry, age_days=age, status=status)
    if status == "stale":
        payload["action_required"] = (
            f"Benchmark is {age} days old (recorded {entry['as_of']}) — refusing to quote. "
            + lookup_hint)
        return (payload, 3)
    if status == "aging":
        payload["warning"] = (
            f"Benchmark is {age} days old (recorded {entry['as_of']}). Usable for rough "
            "planning; refresh before it enters a budget or client deliverable.")
    return (payload, 0)


def staleness() -> list[dict]:
    book = _load()
    out = []
    for entry in book["entries"].values():
        age = _age_days(entry["as_of"])
        out.append({"metric": entry["metric"], "channel": entry["channel"],
                    "segment": entry["segment"], "as_of": entry["as_of"],
                    "age_days": age, "status": _status_for_age(age),
                    "source": entry["source"]})
    return sorted(out, key=lambda e: -e["age_days"])


def main() -> int:
    ensure_utf8_stdout()
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--action", required=True,
                    choices=["record", "quote", "list", "staleness", "metrics"])
    ap.add_argument("--metric")
    ap.add_argument("--channel")
    ap.add_argument("--segment", default="all")
    ap.add_argument("--low", type=float)
    ap.add_argument("--high", type=float)
    ap.add_argument("--value", type=float,
                    help="Point estimate — records low == high == value")
    ap.add_argument("--unit")
    ap.add_argument("--source", help="URL the number was read from (required to record)")
    ap.add_argument("--as-of", dest="as_of", help="YYYY-MM-DD (default: today)")
    ap.add_argument("--note")
    args = ap.parse_args()

    try:
        if args.action == "metrics":
            print(json.dumps(METRICS, indent=2))
            return 0
        if args.action in ("list", "staleness"):
            print(json.dumps(staleness(), indent=2))
            return 0
        if not args.metric or not args.channel:
            print("ERROR: --metric and --channel are required.", file=sys.stderr)
            return 2
        if args.action == "record":
            if args.value is not None:
                low = high = args.value
            else:
                low, high = args.low, args.high
            if low is None or high is None:
                print("ERROR: provide --low and --high (or --value).", file=sys.stderr)
                return 2
            entry = record(args.metric, args.channel, args.segment, low, high,
                           args.source or "", args.as_of, args.unit, args.note)
            print(json.dumps({"recorded": entry}, indent=2))
            return 0
        if args.action == "quote":
            payload, code = quote(args.metric, args.channel, args.segment)
            print(json.dumps(payload, indent=2))
            return code
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
