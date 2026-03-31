---
description: Multi-dimensional competitive analysis — content, SEO, paid ads, social, AI visibility, pricing, and positioning
argument-hint: "<competitor names or URLs>"
---

# Competitor Analysis

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Deliver a comprehensive competitive intelligence report across all major marketing dimensions. Identify competitor strengths, weaknesses, strategies, and gaps the brand can exploit for competitive advantage.

## Trigger

User runs `/competitor-analysis` or asks to analyze competitors, benchmark against competition, find competitive gaps, or understand the competitive landscape.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Competitors** — 2-5 competitor names and/or URLs to analyze

2. **Analysis scope** — one of:
   - **Full analysis** — all dimensions below (default)
   - **SEO comparison** — keyword overlap, domain authority, content depth, link gaps
   - **Content analysis** — publishing strategy, content types, topics, quality, frequency
   - **Paid advertising** — ad copy, creative themes, platforms, estimated spend
   - **Social media** — platform presence, engagement, content mix, posting cadence
   - **Pricing and positioning** — pricing models, value props, messaging frameworks

3. **Key battleground keywords** — terms where the brand competes head-to-head

4. **Industry or category** — for contextual benchmarking

## Process

### 1. Content Strategy Analysis
- Content types produced (blog, video, podcast, newsletter, reports, tools)
- Publishing frequency and consistency
- Top-performing content (shares, backlinks, estimated traffic)
- Content themes and topic clusters
- Content gaps — topics you cover that they don't, and vice versa
- Quality assessment (depth, originality, E-E-A-T signals)

### 2. SEO Competitive Landscape

**If ~~SEO tools are connected (Ahrefs, Similarweb):**
- Pull domain metrics, keyword rankings, backlink profiles automatically
- Identify exact keyword overlap and gaps

**If tools are not connected:**
- Use web search to research the SEO landscape
- Note: "For detailed ranking data, connect Ahrefs or Similarweb via `/connect`."

Assess:
- Domain authority comparison
- Keyword overlap — terms both sites rank for, and who ranks higher
- Keyword gaps — terms competitors rank for that you don't
- Backlink profile comparison (referring domains, link quality)
- Content depth — average word count, topic breadth
- SERP feature ownership (featured snippets, People Also Ask, knowledge panels)

### 3. Paid Advertising Intelligence
- Platforms in use (Google, Meta, LinkedIn, TikTok, programmatic)
- Ad copy themes and messaging patterns
- Landing page strategies
- Estimated ad spend (if data available)
- Creative approaches (image, video, carousel, text)
- Targeting signals (audiences they appear to target)

### 4. Social Media Benchmarking
- Platform presence (which platforms, follower counts)
- Engagement rates by platform
- Content mix (text, image, video, stories, live)
- Posting frequency and consistency
- Community engagement (response rate, comment quality)
- Viral or standout content

### 5. AI Answer Engine Visibility
- How competitors appear in Google AI Overviews
- Presence in Perplexity, ChatGPT, and other AI answer engines
- Citation patterns — which competitor sites are cited most for key topics
- Structured content that makes competitors more "citeable"

### 6. Pricing and Positioning
- Pricing models (subscription, per-unit, freemium, enterprise)
- Price points relative to market
- Value proposition and messaging pillars
- Market positioning (premium, mid-market, budget, niche)
- Differentiation claims

## Output Format

### Competitive Overview Matrix

| Dimension | Your Brand | Competitor A | Competitor B | Competitor C |
|-----------|-----------|--------------|--------------|--------------|

Include rows for: content volume, SEO strength, social following, ad presence, pricing tier, AI visibility.

### Content Strategy Comparison

| Metric | Your Brand | Comp A | Comp B | Winner |
|--------|-----------|--------|--------|--------|

### SEO Landscape

| Keyword | Your Rank | Comp A | Comp B | Gap/Opportunity |
|---------|-----------|--------|--------|-----------------|

### SWOT per Competitor

For each competitor: Strengths, Weaknesses, Opportunities (for your brand), Threats.

### Strategic Recommendations

**Quick Wins:**
- Competitive gaps you can exploit immediately

**Strategic Opportunities:**
- Larger market positioning or content strategy moves

**Defensive Priorities:**
- Areas where competitors are gaining ground that need protection

## After the Analysis

Ask: "Would you like me to:
- Set up ongoing competitor monitoring? (`/competitor-monitor`)
- Create a counter-narrative strategy? (`/counter-narrative`)
- Draft content to fill the competitive gaps identified? (`/content-brief`)
- Build a share-of-voice tracking dashboard? (`/share-of-voice`)
- Analyze competitor ad creative in detail? (`/paid-advertising`)
- Map the full narrative landscape? (`/narrative-landscape`)"
