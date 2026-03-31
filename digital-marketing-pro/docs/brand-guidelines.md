# Brand Guidelines, Guardrails & Agency SOPs

This guide covers how to import and use brand guidelines, restrictions, channel-specific styles, deliverable templates, and agency SOPs with Digital Marketing Pro.

## Why Import Guidelines?

Your brand profile captures the **what** — identity, voice scores (1-10), channels, goals. But real brands operate from detailed documents: voice & tone guides that say "never use exclamation marks in headlines," messaging playbooks with approved taglines, restriction lists banning specific words, and channel-specific style rules.

Brand guidelines capture the **how** — the detailed rules that make content authentically on-brand.

| Without Guidelines | With Guidelines |
|---|---|
| Voice: formality 7/10 | "Never use exclamation marks in headlines. Lead with data, then story. Max 20 words per sentence." |
| Avoid: cheap, discount | Full banned word list with 40+ terms, context for each, and suggested alternatives |
| Channel: LinkedIn | "LinkedIn: max 1300 chars, no emoji in first line, end with a question. Instagram: casual, emoji-friendly, hook in first line." |
| Industry: healthcare | "All health claims require citation. Never use 'cure' or 'guarantee'. Include disclaimer on wellness content." |

## Getting Started

### Import Your First Guidelines

```
/dm:import-guidelines
```

You can paste content from existing documents or describe rules conversationally:

**Example — pasting from a style guide:**

> You: Here's our brand voice guide. We're friendly but professional. Never use jargon — if a simpler word exists, use it. Use "you" not "customers." Sentences should be under 20 words.

The plugin extracts the rules, structures them into the right category (`voice-and-tone.md`), and saves them to your brand's guidelines directory.

**Example — describing restrictions:**

> You: We can never use the words "cheap," "guarantee," "best," or "revolutionary." Health claims need a disclaimer.

Saves to `restrictions.md` with alternatives suggested for each banned word.

### What Categories Exist?

| Category | What It Covers | Example Rules |
|----------|---------------|---------------|
| **Voice & Tone** | Writing style, tone, dos/don'ts beyond numeric scores | "Lead with empathy, follow with expertise" |
| **Messaging** | Approved key messages, value props, taglines, positioning | "Save 10 hours per week on reporting" |
| **Restrictions** | Banned words, restricted claims, mandatory disclaimers | "'cheap' → use 'affordable'" |
| **Channel Styles** | Per-channel tone and format rules | "LinkedIn: professional, no emoji; IG: casual, emoji OK" |
| **Visual Identity** | Colors, fonts, logo rules (text descriptions for briefs) | "Primary blue: #1a73e8, never on dark backgrounds" |
| **Custom** | Anything else (accessibility, legal triggers, seasonal) | "Holiday content requires Dec 1 approval" |

### Import Across Multiple Sessions

Guidelines persist — import them once, and they're applied in every future session. You can add to them over time:

> Session 1: /dm:import-guidelines → import voice & tone guide
> Session 2: /dm:import-guidelines → add restrictions
> Session 3: /dm:import-guidelines → add channel-specific styles

Each import asks whether to merge with or replace existing content.

## How Guidelines Are Enforced

### Automatic Application

Once imported, guidelines are enforced automatically across all plugin modules and commands:

1. **Session start**: The brand summary now shows guideline counts alongside voice scores and channel info
2. **Content creation**: Every module checks restrictions before generating content. Banned words are flagged, restricted claims get qualifications, mandatory disclaimers are appended
3. **Channel-specific output**: When creating content for a specific channel (LinkedIn post, Instagram caption, email), channel styles override the base voice settings
4. **Content review**: The Brand Guardian agent checks all content against guidelines before approval
5. **Violation tracking**: Guideline violations are logged for pattern analysis

### Priority Order

When guidelines and the brand profile conflict:

1. **Restrictions** — always enforced (highest priority)
2. **Channel styles** — override base voice for that specific channel
3. **Voice & tone guidelines** — override numeric voice scores with detailed rules
4. **Brand profile voice scores** — default when no guidelines exist
5. **SOPs** — add workflow steps, don't override content rules

### Example: Channel Styles Override

Your brand profile says formality = 7/10. But your channel styles say:

- LinkedIn: formality 8/10, no emoji, thought leadership tone
- Instagram: formality 4/10, emoji encouraged, casual and playful

When you ask "Write me a LinkedIn post," the plugin uses LinkedIn's formality 8 — not the base 7. When you ask "Write me an Instagram caption," it uses formality 4.

## Worked Example

### Before Guidelines

> You: Write me a blog post about our new feature.

The plugin uses your brand profile's voice scores (formality 7, energy 5, humor 3, authority 5) and your preferred/avoid word lists. The output is on-brand at a basic level.

### After Importing Guidelines

> You: /dm:import-guidelines
>
> You: Here's our style guide:
> - Always lead with the customer problem, not our solution
> - Use "you" and "your" — never "our customers" or "users"
> - Sentences max 20 words, paragraphs max 3 sentences
> - Every blog post starts with a question or surprising stat
> - Never use "synergy," "leverage," "paradigm," or "best-in-class"
> - Include a data point within the first 100 words
> - CTAs should ask a question, not give a command

Now when you ask "Write me a blog post," the plugin:
- Opens with a question or surprising stat (voice-and-tone rule)
- Leads with the customer problem (voice-and-tone rule)
- Uses "you/your" throughout (voice-and-tone rule)
- Keeps sentences under 20 words (voice-and-tone rule)
- Avoids "synergy," "leverage," etc. (restrictions)
- Includes early data point (voice-and-tone rule)
- Ends with a question CTA (voice-and-tone rule)

## Deliverable Templates

### What Templates Do

Templates define the output structure for plugin commands. Instead of getting the plugin's default report format, you get your agency's or brand's custom format.

### Importing a Template

```
/dm:import-template
```

**Example:**

> You: Our monthly performance reports should have: Executive Summary (3 bullets max), Channel Performance (table with MTD vs target), Campaign Highlights (top 3), Issues & Risks, Recommendations, Next Month Plan.

The plugin saves this as a template. Next time you run `/dm:performance-report`, it follows your custom structure.

### Which Commands Use Templates?

Any command can use a custom template. Name your template to match the command:

| Template Name | Used By |
|---|---|
| `performance-report` | `/dm:performance-report` |
| `proposal` | Campaign plan outputs |
| `content-brief` | `/dm:content-brief` |
| `campaign-plan` | `/dm:campaign-plan` |
| `pr-pitch` | `/dm:pr-pitch` |
| `competitor-analysis` | `/dm:competitor-analysis` |

Custom-named templates can be referenced by any module when relevant.

## Agency SOPs

### What SOPs Do

SOPs (Standard Operating Procedures) define **workflow steps** — approval processes, review chains, launch checklists. Unlike guidelines (which are per-brand), SOPs are agency-level and apply across all clients.

### Importing an SOP

```
/dm:import-sop
```

**Example:**

> You: Before publishing any content: 1. Writer creates draft, 2. Editor reviews quality, 3. Brand manager checks voice, 4. Legal reviews if claims present, 5. Client approves, 6. Publish.

The plugin saves this as a content approval workflow. When generating content, it adds notes about required approval steps.

### SOP Types

| Type | Example |
|---|---|
| **Content workflow** | Draft → edit → brand check → legal (conditional) → client approval → publish |
| **Campaign checklist** | Pre-launch verification, launch day checks, post-launch monitoring |
| **Escalation procedure** | Minor → account manager, major → director, critical → CEO within 1 hour |
| **Quality assurance** | Brand compliance check, accessibility review, competitor mention scan |
| **Client onboarding** | Brand setup → guidelines import → template import → first campaign |
| **Reporting workflow** | Data collection → analysis → presentation → client review → delivery |

### How SOPs Are Applied

When you use commands like `/dm:campaign-plan` or `/dm:content-brief`, the plugin checks for relevant SOPs and:

- Adds workflow steps to the output ("Submit to legal review before publishing")
- Flags when a step requires human approval
- Notes SOP compliance in the deliverable

## Storage Structure

Guidelines, templates, and SOPs are stored at:

```
~/.claude-marketing/
├── brands/
│   └── your-brand/
│       ├── profile.json                 # Brand identity (existing)
│       ├── guidelines/                  # NEW: Brand guidelines
│       │   ├── _manifest.json           # Index with counts and metadata
│       │   ├── voice-and-tone.md        # Detailed voice guide
│       │   ├── messaging.md             # Key messages and positioning
│       │   ├── restrictions.md          # Banned words and restricted claims
│       │   ├── channel-styles.md        # Per-channel rules
│       │   ├── visual-identity.md       # Colors, fonts, imagery style
│       │   └── custom/                  # Additional guideline files
│       └── templates/                   # NEW: Deliverable templates
│           ├── _manifest.json           # Template index
│           └── *.md                     # Custom templates
└── sops/                                # NEW: Agency-level SOPs
    ├── _manifest.json                   # SOP index
    └── *.md                             # Workflow definitions
```

All files are markdown — human-readable, easy to edit, and version-controllable.

## Multi-Brand / Agency Workflows

### Per-Brand Guidelines

Each brand has its own guidelines directory. When you switch brands (`/dm:switch-brand`), the active guidelines change too:

> You: /dm:switch-brand acme
> → Loads Acme Corp guidelines (restrictions, voice rules, channel styles)
>
> You: /dm:switch-brand globex
> → Loads Globex Corp guidelines (different restrictions, different voice)

### Shared SOPs

SOPs are agency-level — they apply regardless of which brand is active. Your content approval workflow or crisis escalation procedure works the same across all clients.

### Per-Brand Templates

Templates are brand-specific. Acme Corp may want a different report format than Globex Corp:

- Acme: Executive summary → channel table → recommendations
- Globex: KPI dashboard → deep dives → action items → budget impact

## Viewing and Managing Guidelines

### Check What's Configured

At session start, the brand summary shows:

```
Guidelines: 41 rules across 4 categories · 15 restrictions · 3 templates · 2 SOPs
```

### View Specific Guidelines

> You: Show me our brand restrictions.

The plugin loads and displays `restrictions.md` from the active brand's guidelines.

> You: What channel styles do we have?

Displays `channel-styles.md` with per-channel rules.

### Update Guidelines

> You: /dm:import-guidelines

Add new rules, update existing ones, or replace a category entirely. The plugin asks whether to merge or replace.

### Delete Guidelines

> You: Remove our visual identity guidelines.

Deletes the specific category file and updates the manifest.

## Tips

1. **Start with restrictions** — banned words and restricted claims are the highest-impact guidelines. Import these first.
2. **Add channel styles for your top 3 channels** — this immediately improves content quality for your most-used platforms.
3. **Import templates for your most common deliverables** — performance reports, proposals, and content briefs are good starting points.
4. **Review violations periodically** — the plugin tracks when guidelines are violated. Look for patterns to strengthen your guidelines.
5. **Guidelines evolve** — update them as your brand evolves. The merge feature makes it easy to add new rules without losing existing ones.
