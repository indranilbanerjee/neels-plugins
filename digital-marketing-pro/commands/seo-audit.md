---
description: Run a comprehensive SEO audit — technical health, on-page, content gaps, E-E-A-T, link profile, and competitor benchmarking
argument-hint: "<url or domain> [audit scope]"
---

# SEO Audit

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Audit a website's SEO health across all major ranking dimensions: technical infrastructure, on-page optimization, content quality, E-E-A-T signals, local SEO, link profile, and AI answer engine visibility. Produces a prioritized action plan with impact-to-effort scoring.

## Trigger

User runs `/seo-audit` or asks for an SEO audit, keyword research, content gap analysis, technical SEO check, or competitor SEO comparison.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **URL or domain** — the site to audit, or a topic/keyword if running in keyword research mode

2. **Audit scope** — one of:
   - **Full site audit** — end-to-end SEO review covering all dimensions below (default)
   - **Technical only** — crawlability, Core Web Vitals, structured data, infrastructure
   - **Content only** — thin content, gaps, freshness, E-E-A-T, keyword opportunities
   - **Local SEO** — Google Business Profile, NAP consistency, local schema, reviews
   - **Competitor comparison** — head-to-head benchmarking against specific competitors

3. **Target keywords** (optional) — specific keywords the site is targeting or wants to rank for

4. **Competitors** (optional) — 2-3 domains to benchmark against. If not provided and comparison is needed, identify likely competitors from the keyword space.

## Process

### 1. Keyword Research

**If ~~SEO tools are connected (Ahrefs, Similarweb):**
- Pull keyword data, search volume, difficulty scores, and current ranking positions automatically
- Identify keywords gaining or losing ground

**If tools are not connected:**
- Use web search to research the keyword landscape
- Note: "For precise volume and difficulty data, connect an SEO tool via `/connect ahrefs` or `/connect similarweb`."

For each keyword opportunity, assess:
- **Search volume signals** — relative demand (high, medium, low)
- **Keyword difficulty** — how competitive (easy, moderate, hard)
- **Intent classification** — informational, navigational, commercial, or transactional
- **Long-tail opportunities** — specific, lower-competition phrases with clear intent
- **Question-based keywords** — "how to", "what is" queries for People Also Ask

### 2. Technical SEO Audit

Evaluate infrastructure that affects crawlability and rankings:
- **Page speed** — slow-loading pages, likely causes (large images, render-blocking scripts, redirects)
- **Mobile-friendliness** — responsive design, tap targets, viewport configuration
- **Structured data** — schema markup opportunities (FAQ, HowTo, Product, Article, Organization, Breadcrumb)
- **Crawlability** — robots.txt, XML sitemap, canonical tags, noindex/nofollow usage
- **Broken links** — internal and external 404s, redirect chains
- **HTTPS** — secure connection, mixed content
- **Core Web Vitals** — LCP, INP, CLS indicators
- **Indexation** — pages that should be indexed but aren't, duplicate content risks

### 3. On-Page SEO Audit

For each key page (homepage, top landing pages, recent content):
- **Title tags** — present, unique, 50-60 characters, includes target keyword
- **Meta descriptions** — present, compelling, 150-160 characters, includes CTA
- **Heading hierarchy** — one H1, logical H2/H3 structure, keywords in subheadings
- **Keyword usage** — primary keyword in first 100 words, natural distribution, no stuffing
- **Internal linking** — pages link to related content, orphan pages identified, descriptive anchor text
- **Image optimization** — alt text on all images, compressed files, proper sizing
- **URL structure** — clean, readable, keyword-inclusive

### 4. Content Quality & E-E-A-T Assessment

- **Experience** — first-hand experience signals, original research, case studies
- **Expertise** — author credentials, depth of coverage, technical accuracy
- **Authoritativeness** — citation quality, industry recognition, backlink authority
- **Trustworthiness** — accuracy, transparency, editorial standards, secure site
- **Content freshness** — pages not updated in 12+ months, outdated statistics
- **Thin content** — pages with insufficient depth to rank
- **Content gaps** — topics competitors cover that the site doesn't

### 5. AI Answer Engine Visibility (AEO/GEO)

- **AI Overview presence** — does the site appear in Google AI Overviews?
- **Citation-worthiness** — are there "citeable moments" (definitions, data, structured answers)?
- **Snippet structuring** — content formatted for direct answer extraction
- **Entity consistency** — brand name, facts, and claims consistent across the web

### 6. Link Profile Analysis

- **Domain authority signals** — overall site strength based on backlink profile
- **Backlink quality** — proportion of high-quality vs. low-quality referring domains
- **Anchor text distribution** — natural vs. over-optimized
- **Link velocity** — trend in new links acquired
- **Competitor link gap** — sites linking to competitors but not to this domain
- **Toxic links** — potentially harmful backlinks to disavow

### 7. Local SEO (if applicable)

- **Google Business Profile** — completeness, accuracy, categories, photos, posts
- **NAP consistency** — name, address, phone matching across directories
- **Local schema markup** — LocalBusiness, opening hours, service area
- **Review profile** — volume, recency, rating, response rate
- **Local content** — city/service pages, local landing pages

## Output Format

### Executive Summary
- Overall SEO health score (1-10 per dimension)
- Top 3 strengths
- Top 3 priorities with estimated impact

### Keyword Opportunity Table

| Keyword | Volume Signal | Difficulty | Current Rank | Intent | Recommended Action |
|---------|--------------|------------|--------------|--------|--------------------|

Include 15-25 opportunities sorted by opportunity score.

### Issue Table

| Page/Area | Issue | Severity | Recommended Fix | Effort |
|-----------|-------|----------|-----------------|--------|

Severity: **Critical** (hurting rankings), **High** (significant impact), **Medium** (best practice), **Low** (minor optimization)

### Content Gap Recommendations

For each gap: topic, search demand, competitor coverage, recommended content type, priority, and estimated effort.

### Prioritized Action Plan

**Quick Wins (this week):**
- Actions under 2 hours with immediate impact
- Examples: fix title tags, add meta descriptions, fix broken links, add alt text

**Strategic Investments (this quarter):**
- Higher-effort actions driving long-term growth
- Examples: build topic clusters, pillar pages, link-building campaign, site structure overhaul

Each action includes: what to do, expected impact (high/medium/low), effort estimate, and dependencies.

## After the Audit

Ask: "Would you like me to:
- Draft content briefs for the top keyword opportunities? (`/content-brief`)
- Create optimized title tags and meta descriptions? (`/seo-implement`)
- Run a deeper technical audit? (`/tech-seo-audit`)
- Set up keyword ranking monitoring? (`/rank-monitor`)
- Check AI answer engine visibility? (`/aeo-audit`)
- Compare SEO performance against specific competitors? (`/competitor-analysis`)"
