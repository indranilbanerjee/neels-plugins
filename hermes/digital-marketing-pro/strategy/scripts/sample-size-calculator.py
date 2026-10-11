#!/usr/bin/env python3
"""
sample-size-calculator.py
=========================
Calculate A/B test sample size requirements using the two-proportion Z-test
formula. Returns per-variant sample sizes, total sample needed, and optional
duration estimates based on daily traffic.

Dependencies: none (stdlib only)

MDE semantics (IMPORTANT): --mde is interpreted per --mde-type.
    absolute (default): mde is an absolute change in the rate.
        baseline 0.05 + --mde 0.005 → target 0.055.
    relative: mde is a fractional lift of the baseline.
        baseline 0.05 + --mde 0.10 (a 10% relative lift) → target 0.055.
    (The old script silently treated every --mde as absolute; a skill that
    documented --mde as a relative lift therefore under-sized tests by ~40×.
    --mde-type makes the interpretation explicit.)

Usage:
    python sample-size-calculator.py --baseline-rate 0.03 --mde 0.005
    python sample-size-calculator.py --baseline-rate 0.05 --mde 0.10 --mde-type relative
    python sample-size-calculator.py --baseline-rate 0.03 --mde 0.005 --daily-traffic 5000
    python sample-size-calculator.py --baseline-rate 0.10 --mde 0.02 --significance 0.99 --power 0.90 --variants 3
"""

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402


def inverse_normal_cdf(p):
    """Rational approximation for the inverse standard normal CDF.

    Uses the Abramowitz and Stegun formula 26.2.23.
    Accurate to approximately 4.5e-4.
    """
    if p <= 0 or p >= 1:
        raise ValueError("p must be between 0 and 1 exclusive")
    if p < 0.5:
        return -inverse_normal_cdf(1 - p)
    t = math.sqrt(-2.0 * math.log(1.0 - p))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308
    return t - (c0 + c1 * t + c2 * t * t) / (1.0 + d1 * t + d2 * t * t + d3 * t * t * t)


def calculate_sample_size(baseline_rate, mde, significance, power):
    """Calculate required sample size per variant using the two-proportion Z-test.

    Parameters:
        baseline_rate: current conversion rate (0 < x < 1)
        mde: minimum detectable effect as absolute change
        significance: confidence level (e.g. 0.95)
        power: statistical power (e.g. 0.80)

    Returns:
        sample size per variant (integer, rounded up)
    """
    alpha = 1.0 - significance
    z_alpha = inverse_normal_cdf(1.0 - alpha / 2.0)
    z_beta = inverse_normal_cdf(power)

    p1 = baseline_rate
    p2 = baseline_rate + mde

    numerator = (z_alpha + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p2 - p1) ** 2

    return math.ceil(numerator / denominator)


def build_recommendations(baseline_rate, mde, sample_per_variant, total_sample, daily_traffic, estimated_days, variants):
    """Generate actionable recommendations based on the calculation."""
    recs = []

    if daily_traffic and estimated_days:
        recs.append(
            f"With {daily_traffic:,} daily visitors split across {variants} variants, "
            f"expect the test to run approximately {estimated_days:,} days."
        )
        if estimated_days > 30:
            recs.append(
                "Test duration exceeds 30 days. Consider increasing the MDE threshold "
                "or focusing on higher-traffic pages to shorten the experiment."
            )
        if estimated_days > 90:
            recs.append(
                "Warning: tests running longer than 90 days risk seasonal bias and "
                "external confounders. Re-evaluate whether this test is feasible."
            )

    relative_lift = mde / baseline_rate * 100
    if relative_lift < 5:
        recs.append(
            f"A {relative_lift:.1f}% relative lift is very small. Detecting such a "
            "subtle change requires a large sample. Consider whether a larger effect "
            "size would be more practical to test."
        )

    if sample_per_variant > 100000:
        recs.append(
            "The required sample size is very large. Consider testing bolder changes "
            "with a higher expected impact to reduce the required sample."
        )

    if baseline_rate < 0.01:
        recs.append(
            "Low baseline conversion rates require significantly more traffic. "
            "Consider micro-conversion metrics (e.g., clicks, scroll depth) as "
            "proxy goals to detect changes faster."
        )

    if not recs:
        recs.append(
            "Sample size requirements look reasonable. Ensure even traffic "
            "splitting and avoid peeking at results before reaching the target."
        )

    return recs


def main():
    parser = argparse.ArgumentParser(
        description="Calculate A/B test sample size requirements"
    )
    parser.add_argument("--baseline-rate", type=float, required=True,
                        help="Current conversion rate (e.g. 0.03 for 3%%)")
    parser.add_argument("--mde", type=float, required=True,
                        help="Minimum detectable effect. Interpreted per --mde-type "
                             "(absolute change like 0.005, or relative lift like 0.10)")
    parser.add_argument("--mde-type", choices=["absolute", "relative"], default="absolute",
                        help="Whether --mde is an absolute rate change (default) or a "
                             "relative lift of the baseline (e.g. 0.10 = +10%% relative)")
    parser.add_argument("--significance", type=float, default=0.95,
                        help="Confidence level (default: 0.95)")
    parser.add_argument("--power", type=float, default=0.80,
                        help="Statistical power (default: 0.80)")
    parser.add_argument("--daily-traffic", type=int, default=None,
                        help="Daily visitors for duration estimate")
    parser.add_argument("--variants", type=int, default=2,
                        help="Number of variants including control (default: 2)")
    args = parser.parse_args()

    # --- Validation ---
    if not (0 < args.baseline_rate < 1):
        _common.finish({"error": "baseline-rate must be between 0 and 1 exclusive"})

    if args.mde <= 0:
        _common.finish({"error": "mde must be greater than 0"})

    # Resolve the MDE to an absolute rate change based on --mde-type. This is
    # the fix for the ~40x under-sizing bug: a relative lift of 0.10 on a 0.05
    # baseline is an absolute change of only 0.005, not 0.10.
    if args.mde_type == "relative":
        absolute_mde = args.baseline_rate * args.mde
    else:
        absolute_mde = args.mde

    if args.baseline_rate + absolute_mde >= 1:
        _common.finish({"error": "baseline-rate + resolved absolute mde must be less than 1"})

    if not (0.5 < args.significance < 0.999):
        _common.finish({"error": "significance must be between 0.5 and 0.999 exclusive"})

    if not (0.5 < args.power < 0.999):
        _common.finish({"error": "power must be between 0.5 and 0.999 exclusive"})

    if args.variants < 2:
        _common.finish({"error": "variants must be at least 2"})

    if args.daily_traffic is not None and args.daily_traffic <= 0:
        _common.finish({"error": "daily-traffic must be a positive integer"})

    # --- Calculation (always in absolute terms) ---
    sample_per_variant = calculate_sample_size(
        args.baseline_rate, absolute_mde, args.significance, args.power
    )
    total_sample = sample_per_variant * args.variants

    relative_lift = (absolute_mde / args.baseline_rate) * 100

    estimated_days = None
    if args.daily_traffic:
        visitors_per_variant_per_day = args.daily_traffic / args.variants
        estimated_days = math.ceil(sample_per_variant / visitors_per_variant_per_day)

    recommendations = build_recommendations(
        args.baseline_rate, absolute_mde, sample_per_variant, total_sample,
        args.daily_traffic, estimated_days, args.variants
    )

    # --- Output ---
    output = {
        "baseline_rate": args.baseline_rate,
        "mde_input": args.mde,
        "mde_type": args.mde_type,
        "absolute_mde": round(absolute_mde, 6),
        "minimum_detectable_effect": round(absolute_mde, 6),
        "target_rate": round(args.baseline_rate + absolute_mde, 6),
        "relative_lift": f"{relative_lift:.1f}%",
        "significance_level": args.significance,
        "statistical_power": args.power,
        "sample_size_per_variant": sample_per_variant,
        "total_sample_needed": total_sample,
        "variants": args.variants,
        "methodology": "Two-proportion Z-test",
        "recommendations": recommendations,
    }

    if args.daily_traffic:
        output["daily_traffic"] = args.daily_traffic
        output["estimated_days"] = estimated_days

    _common.finish(output)


if __name__ == "__main__":
    main()
