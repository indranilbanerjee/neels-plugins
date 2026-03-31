---
description: Generate a full multi-channel campaign plan with objectives, audience, channel mix, budget, timeline, and KPIs
argument-hint: "<campaign objective or product>"
---

# Campaign Plan

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate a comprehensive multi-channel marketing campaign plan ready for execution. Covers strategic objectives, audience segmentation, channel selection, budget distribution, phased timeline, content calendar, and measurable KPIs.

## Trigger

User runs `/campaign-plan` or asks to plan, design, build, or launch a marketing campaign.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Campaign goal** — the primary objective (drive signups, increase awareness, launch a product, generate leads, re-engage churned users, drive event registrations)

2. **Product or service** — what is being promoted

3. **Target audience** — who the campaign is aimed at (demographics, roles, industries, pain points, buying stage). If a brand profile exists, reference existing personas.

4. **Timeline** — campaign duration and any fixed dates (launch date, event, seasonal deadline)

5. **Budget range** — approximate budget or budget tier (optional; if not provided, generate a channel-agnostic plan and note where budget allocation would matter)

6. **Additional context** (optional):
   - Key differentiators or value propositions
   - Previous campaign performance or learnings
   - Geographic focus or market
   - Channel constraints or preferences
   - Compliance requirements

## Brand Context

If a brand profile exists at `~/.claude-marketing/brands/`, load it automatically:
- Apply brand voice settings to all messaging recommendations
- Reference existing audience personas instead of asking for them again
- Check for guidelines, restrictions, and compliance rules
- Load custom templates if available
- Check agency SOPs for campaign planning standards

If no brand exists, ask: "Set up a brand first (`/brand-setup`)?" — or proceed with general best practices.

## Campaign Brief Structure

### 1. Campaign Overview
- Campaign name suggestion
- One-sentence campaign summary
- Primary objective with a specific, measurable goal (SMART format)
- Secondary objectives (if applicable)

### 2. Target Audience
- Primary audience segment with targeting parameters
- Secondary segment (if applicable)
- Pain points, motivations, and buying triggers
- Channel affinity — where this audience spends time
- Buying stage alignment (awareness, consideration, decision)

### 3. Key Messages
- Core campaign message (one sentence)
- 3-4 supporting messages aligned to audience pain points
- Message variations by channel (if different tones needed)
- Proof points or evidence supporting each message

### 4. Channel Strategy

Recommend channels based on audience behavior, budget, and objective. For each channel:
- Why this channel fits the audience and objective
- Content format recommendations
- Estimated effort level (low, medium, high)
- Expected performance benchmarks for the industry
- Budget allocation (if budget provided)

Channel categories to evaluate:
- **Owned**: blog, email, website, social profiles, newsletter
- **Earned**: PR, influencer partnerships, guest posts, community
- **Paid**: search ads, social ads, display, sponsored content, retail media

If ~~analytics or ~~advertising connectors are available, reference historical performance data to inform channel recommendations.

### 5. Content Calendar

Week-by-week (or day-by-day for short campaigns) content plan:

| Week | Content Piece | Channel | Format | Owner/Notes | Dependencies |
|------|--------------|---------|--------|-------------|--------------|

Include key milestones, launch dependencies, and approval checkpoints.

### 6. Content Assets Required

List every content asset needed:
- Asset name and type (blog, email, social, ad creative, landing page, video, etc.)
- Brief description
- Priority (must-have vs. nice-to-have)
- Production timeline

### 7. Budget Allocation (if budget provided)
- Channel-by-channel breakdown
- Production costs vs. distribution/ad spend
- Contingency recommendation (10-15%)

### 8. Success Metrics

| KPI | Target | Measurement Method | Reporting Cadence |
|-----|--------|--------------------|-------------------|

- Primary KPI with target number
- 3-5 secondary KPIs
- Attribution approach
- Reporting frequency

### 9. Risks and Mitigations
- 2-3 potential risks (timeline, audience mismatch, channel underperformance)
- Mitigation strategy for each

### 10. Next Steps
- Immediate action items to kick off
- Stakeholder approvals needed
- Key decision points

## After Planning

Ask: "Would you like me to:
- Draft specific content pieces from the calendar? (`/content-engine`)
- Create the email sequences? (`/email-sequence`)
- Build the media plan with budget pacing? (`/media-plan`)
- Set up competitor monitoring for the campaign period? (`/competitor-monitor`)
- Design the landing page copy? (`/content-engine`)"
