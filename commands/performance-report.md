---
description: Generate a marketing performance report with KPI tracking, trend analysis, anomaly detection, and recommendations
argument-hint: "<channels or period> [audience: executive|tactical]"
---

# Performance Report

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a structured marketing performance report that transforms raw data into actionable insights. Covers KPI tracking, period-over-period trends, anomaly detection, channel benchmarking, and prioritized optimization recommendations.

## Trigger

User runs `/performance-report` or asks for a marketing report, performance review, channel analysis, or campaign results summary.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Reporting period** — date range for the report (e.g., "last 30 days", "Q1 2026", "Feb 1-28")

2. **Channels to cover** — which marketing channels to include:
   - All channels (default)
   - Specific: organic search, paid search, social media, email, direct, referral

3. **Data source** — raw performance data in any of these forms:
   - Pasted directly into the conversation
   - CSV or spreadsheet file
   - Connected platform (if ~~analytics or ~~advertising are available)

4. **Comparison period** — previous period, year-over-year, or custom benchmark

5. **Report audience** — who will read this:
   - **Executive** — high-level summary with headline metrics and strategic recommendations
   - **Tactical** — detailed breakdown with granular data and specific optimizations

6. **KPIs of interest** (optional) — specific metrics to focus on, or use defaults:
   - Traffic: sessions, users, pageviews, bounce rate
   - Conversions: conversion rate, leads, revenue, ROAS
   - Engagement: time on site, pages per session, social engagement
   - Email: open rate, click rate, unsubscribe rate

## Process

1. **Load brand context** — apply brand goals, targets, and industry benchmarks from the active profile

2. **Ingest data** — validate and normalize the provided performance data

3. **Calculate core KPIs** — per channel: traffic, conversions, revenue, ROAS, CPA, engagement metrics, growth rates

4. **Trend analysis** — period-over-period changes, trajectory direction, seasonality adjustments

5. **Anomaly detection** — flag significant spikes or drops with likely root causes:
   - Traffic anomalies (algorithm update, viral content, technical issue)
   - Conversion anomalies (landing page change, pricing update, competitive action)
   - Cost anomalies (bid changes, new competition, quality score shifts)

6. **Benchmark comparison** — compare against industry averages and brand-specific targets

7. **Generate insights** — what worked, what underperformed, and hypotheses for why

8. **Produce recommendations** — prioritized optimizations for the next period, ranked by expected impact

## Output Format

### Executive Summary
- 3-5 headline metrics with period-over-period change and trend direction
- Overall assessment: on track, needs attention, or urgent action required
- Top win and top concern with context

### Channel Performance Dashboard

| Channel | Sessions | Conversions | Revenue | ROAS | vs. Prior | Trend |
|---------|----------|-------------|---------|------|-----------|-------|

### Trend Analysis
- Period-over-period comparison with percentage changes
- Trajectory indicators (accelerating, stable, decelerating)
- Seasonality context where relevant

### Anomaly Alerts

| Metric | Change | Likely Cause | Recommended Action |
|--------|--------|--------------|-------------------|

Flag any metric that moved more than 2 standard deviations from its trend.

### Top Wins
- 3-5 areas of strongest performance with context and contributing factors

### Areas Needing Attention
- 3-5 underperforming areas with root cause hypotheses and fix recommendations

### Recommendations

**Immediate Actions (this week):**
- Quick optimizations with expected impact

**Strategic Adjustments (this month):**
- Larger changes to channel mix, budget allocation, or content strategy

**Next Period Goals:**
- Recommended targets based on current trajectory and optimization potential

## After the Report

Ask: "Would you like me to:
- Dive deeper into any specific channel? (`/analytics-insights`)
- Investigate an anomaly in detail? (`/anomaly-scan`)
- Adjust budget allocation based on these results? (`/budget-optimizer`)
- Generate a client-ready version of this report? (`/client-report`)
- Create a live dashboard to track these KPIs? (`/live-dashboard`)
- Export this data to a spreadsheet? (`/data-export`)"
