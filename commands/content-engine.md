---
description: Draft blog posts, ad copy, emails, social media, landing pages, and video scripts with brand voice and SEO
argument-hint: "<content type and topic>"
---

# Content Engine

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../CONNECTORS.md).

Generate marketing content drafts tailored to a specific content type, audience, and brand voice. Covers blog posts, ad copy, email campaigns, social media, landing pages, video scripts, press releases, and case studies — with built-in SEO optimization, brand compliance, and quality evaluation.

## Trigger

User runs `/content-engine` or asks to draft, write, create, or optimize marketing content.

## Inputs

Gather the following from the user. If not provided, ask before proceeding:

1. **Content type** — one of:
   - Blog post or article
   - Ad copy (specify platform: Google, Meta, LinkedIn, TikTok)
   - Email (single email, newsletter, or sequence)
   - Social media post (specify platform: LinkedIn, Twitter/X, Instagram, Facebook, Threads)
   - Landing page copy
   - Video script (YouTube, TikTok, Instagram Reels, explainer)
   - Press release
   - Case study
   - Content calendar

2. **Topic** — the subject or theme of the content

3. **Target audience** — who this content is for (role, industry, pain points, buying stage)

4. **Key messages** — 2-4 main points or takeaways to communicate

5. **Additional context** (optional):
   - Tone override (if different from brand default)
   - Length target or format constraints
   - Primary keyword for SEO
   - Call to action
   - Campaign context or related content

## Brand Voice

- If a brand profile exists at `~/.claude-marketing/brands/`, apply voice settings automatically (formality, energy, humor, authority scales)
- Load guidelines, restrictions, approved messaging, and channel-specific tone overrides
- If no brand profile exists, ask: "Do you have brand voice guidelines? If not, I'll use a professional tone."

## Content Generation by Type

### Blog Post / Article
- 2-3 headline options with SEO keyword in the primary
- Hook introduction (question, statistic, bold statement, or story)
- 3-5 sections with descriptive subheadings using related keywords
- Supporting evidence, examples, and data references
- Conclusion with clear call to action
- SEO: meta title, meta description, internal linking suggestions, keyword placement

### Ad Copy
- Platform-specific format and constraints (character limits, headline count, description count)
- 3-5 headline variations
- 2-3 description variations
- Display URL suggestions
- Call-to-action options
- Ad extensions recommendations
- Compliance notes for regulated industries

### Email
- 2-3 subject line options with open-rate considerations
- Preview text
- Body copy with clear hierarchy and scannable formatting
- Primary CTA with button text
- Personalization token recommendations
- Deliverability notes (spam trigger words, link density, image-to-text ratio)

### Social Media Post
- Platform-native format and length
- Hook in the first line (scroll-stopping opener)
- Hashtag strategy (platform-appropriate count)
- Call to action or engagement prompt
- Image/video specifications and recommendations
- Optimal posting time suggestions

### Landing Page
- Headline and subheadline
- Hero section copy
- 3-4 benefit-driven value propositions
- Social proof placement (testimonials, logos, statistics)
- Primary and secondary CTAs
- FAQ section
- SEO: meta title, meta description

### Video Script
- Platform-specific structure (YouTube: 3-10 min, TikTok: 30-60s, Reels: 15-90s)
- Hook within first 3 seconds
- Scene descriptions with timestamps
- Dialogue and on-screen text
- B-roll suggestions
- Music and tone recommendations
- End card with CTA

### Press Release
- Headline following press release conventions
- Dateline and lead paragraph (who, what, when, where, why)
- Supporting quotes (placeholder guidance)
- Boilerplate and media contact placeholders

### Case Study
- Result-focused title
- Customer overview (industry, size, challenge)
- Challenge → Solution → Results structure
- Metrics and data points (prompt user for specifics)
- Customer quote placeholders
- Call to action

## Quality Checks

After drafting, automatically evaluate:
- Brand voice consistency (matches profile settings)
- Compliance (restricted terms, required disclaimers, regulatory language)
- Legal flags (unsubstantiated claims, superlatives without evidence, comparative claims)
- SEO alignment (keyword usage, meta tags, heading structure)
- Readability score appropriate for target audience

## After Drafting

Ask: "Would you like me to:
- Revise any section or adjust the tone?
- Create variations for A/B testing? (`/prompt-test`)
- Evaluate quality with the full scoring framework? (`/eval-content`)
- Adapt this content for other channels? (`/content-repurpose`)
- Create an email sequence from this content? (`/email-sequence`)
- Generate social media posts to promote this? (`/social-strategy`)"
