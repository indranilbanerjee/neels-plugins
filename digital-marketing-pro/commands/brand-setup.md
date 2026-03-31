---
description: Set up a new brand profile with voice, audience, competitors, guidelines, and compliance rules
argument-hint: "<brand name>"
---

# Brand Setup

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Create or update a brand marketing profile that powers every skill in the plugin. The profile captures brand identity, voice settings, target audiences, competitor landscape, compliance requirements, and channel strategy — then stores it for automatic use across all marketing operations.

## Trigger

User runs `/brand-setup` or asks to set up a new brand, onboard a new client, create a brand profile, or switch between brands.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Brand name** — the company, product, or client name

2. **What the brand does** — one-sentence elevator pitch (used to infer industry, business model, and USP)

3. **Target audience** — who the brand serves (B2B/B2C, demographics, job titles, pain points)

4. **Brand voice** — 3 descriptive words (e.g., "bold, witty, professional") mapped to formality, energy, humor, and authority scales (1-10)

5. **Primary marketing channels** — where the brand focuses efforts (social, email, SEO, paid ads, etc.)

6. **Additional context** (optional):
   - Competitors to track
   - Compliance or regulatory requirements (HIPAA, GDPR, financial services, etc.)
   - Existing style guide document or URL to import
   - Brand guidelines, approved messaging, restricted terms
   - Geographic markets and languages

## Setup Modes

### Quick Setup (5 questions — get started in 2 minutes)

Ask only the 5 essential questions above. From these, intelligently populate the full profile:
- Infer industry, business model, and compliance requirements from the elevator pitch
- Map voice descriptors to 1-10 scales (e.g., "professional" = formality: 8, "fun" = humor: 7)
- Set sensible defaults for everything else
- Tell the user: "Quick profile created! Refine anytime with `/brand-setup --full`"

### Full Setup (17 questions — comprehensive profiling)

Walk through detailed profiling across 5 sections:

#### Brand Identity
1. Brand name
2. Elevator pitch
3. Unique selling proposition
4. Mission and values

#### Business Model
5. B2B, B2C, or hybrid
6. Industry and sub-category
7. Revenue model
8. Sales cycle length

#### Target Audience
9. Primary persona (demographics, role, pain points, goals)
10. Secondary persona (optional)
11. Buying triggers and objections

#### Brand Voice & Messaging
12. Voice attributes (3 words mapped to 4 scales)
13. Messaging pillars (3-5 core messages)
14. Restricted language (terms to avoid, compliance constraints)

#### Marketing Context
15. Active channels with goals per channel
16. Top 3-5 competitors
17. Geographic markets and languages

## Profile Storage

Profiles are saved to `~/.claude-marketing/brands/{slug}/profile.json` and automatically loaded by every skill:
- `profile.json` — full brand context
- `guidelines/` — imported style guides, restrictions, approved messaging
- `templates/` — custom deliverable templates

## Brand Switching (Agency Use)

For agencies managing multiple brands:
- Switch active brand: `/switch-brand AcmeMed`
- List all brands: `/switch-brand --list`
- Each brand gets isolated context — no cross-contamination

## After Setup

After creating the profile, ask:

"Brand profile for [name] is ready. Would you like to:
- Import an existing style guide? (`/import-guidelines`)
- Run a competitive analysis? (`/competitor-analysis`)
- Plan your first campaign? (`/campaign-plan`)
- Audit your SEO? (`/seo-audit`)
- Check which connectors are active? (`/integrations`)"
