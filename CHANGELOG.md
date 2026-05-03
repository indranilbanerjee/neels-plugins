# Changelog

All notable changes to the neels-plugins marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.5.0] - 2026-05-03

### Added — Compliance, Hygiene, Cowork-Compatible Aggregators

Audit of the marketplace surfaced documentation drift and missing compliance-friendly metadata. This release brings everything in sync with the actual plugin states and the Anthropic Software Directory Policy.

#### contentforge updated to v3.9.1

ContentForge v3.9.1 ships Cowork-compatible aggregator MCPs for services that have no first-party HTTP MCP — specifically Google Sheets and Google Drive. The new connector reference catalog includes:
- Pipedream MCPs (Google Sheets, Google Drive, plus a generic 1000+ service template)
- Composio MCPs (Google Sheets + 500+ generic apps)
- Zapier MCP (single endpoint, 8000+ integrations)
- Make.com MCP (template URL with zone + token substitution)

Plus full `_auth` notes on every catalog entry and explicit Cowork compatibility statements. ContentForge's plugin.json now carries `$schema`, `homepage`, `repository`, `license`, `keywords`, and `author.url` fields that were previously missing.

#### Marketplace metadata hardening

- Added LICENSE file (MIT) — the README already claimed MIT but no LICENSE existed.
- README rewrites: badges updated from stale v1.23.0 to current v2.5.0; plugin table updated from stale v2.7.0/v3.8.0/v1.3.0 to current v3.1.0/v3.9.1/v1.5.0; added a Platform Compatibility section explicitly mapping which features work in Claude Code CLI vs Anthropic Cowork; added a Compliance section documenting alignment with the Anthropic Software Directory Policy; added a Plugin Coexistence Pattern section documenting the zero-global-hooks + opt-in-MCPs convention all three plugins follow.
- marketplace.json gained `$schema`, `metadata.homepage`, `metadata.license`, `metadata.keywords`, and `owner.url` fields; each plugin entry gained per-plugin `homepage` and `license` fields.

#### Compliance posture (Anthropic Software Directory Policy)

All three plugins reviewed against the policy:
- No financial transaction processing ✓
- No advertising or ad-serving ✓
- No circumvention of safety guardrails ✓
- AI-generated images (where supported) require explicit user approval and are produced in a clear marketing-content context ✓
- All MCP connectors use OAuth 2.0 or API-key auth via the connector provider's official endpoint ✓

### Updated
- Marketplace metadata version bumped to 2.5.0
- contentforge bumped to v3.9.1

---

## [2.4.0] - 2026-05-03

### Changed — Multi-Plugin Coexistence Sweep

The same global-hook issue that prompted contentforge v3.9.0 earlier today affected the other two marketing plugins. Both fixed in matching releases.

- **digital-marketing-pro** updated from v2.7.0 to v3.1.0 — combines the v3.0.0 release (12-Part Engagement Methodology, Four Core Documents, Two-Views Model, Decision Matrix, Living Project Instruction File on top of 25 agents + 141 skills) with v3.1.0 hook hygiene (removed the `PreToolUse mcp_.*` matcher that was gating every MCP call from every installed plugin through DMP's brand-compliance prompt — the most acute multi-plugin-coexistence issue in the marketing suite).
- **socialforge** updated from v1.4.0 to v1.5.0 — removed all 4 global hooks (SessionStart credential banner, PreToolUse Write/Edit compliance check, SubagentStart brand-context injection, Stop image-approval verification). Credential status now via `/sf:status` on demand instead of every-Claude-Code-launch banner.

### Background

Audit confirmed via current Claude Code docs (May 2026) that plugin hooks fire globally on every operation regardless of working directory. There is no per-directory or per-project scoping. Plugins that registered SessionStart/PreToolUse/Stop hooks were imposing latency, token cost, and noise on every Claude Code session in every project — even unrelated ones — until removed. All three marketing plugins now ship with empty `hooks/hooks.json` and preserve their prior config in `hooks/hooks-reference.example.json` for users who specifically want a behavior back.

### Updated
- Marketplace metadata version bumped to 2.4.0

---

## [2.3.0] - 2026-05-03

### Changed
- **contentforge** updated from v3.8.0 to v3.9.0 — world-class humanizer + multi-plugin coexistence fixes
  - **Humanizer (Phase 6.5):** new 29-pattern AI-detection catalog organized into 5 buckets (content, language/grammar, style, communication, filler/hedging) adapted from Wikipedia: Signs of AI writing (CC BY-SA, WikiProject AI Cleanup) and structured after blader/humanizer (MIT). Adds copula avoidance, em dash overuse, rule of three, false ranges, signposting, persuasive authority tropes, fragmented headers, and ~15 other patterns the prior catalog was missing.
  - **New Step 7.5 self-critique meta-pass:** the model asks itself "what makes this still obviously AI?", lists tells, makes surgical edits, optionally injects soul (opinions, mixed feelings, first-person, intentional rhythm). Single highest-leverage technique adopted from blader.
  - **New Step 0.1 voice calibration:** when brand profile includes a `writing_sample` field, analyzes sentence length pattern, word choice level, punctuation habits, and verbal tics, then matches them. Replaces generic personality archetype with real human fingerprint.
  - **Em dash advice corrected** from 2-3 per 500 words (recommended) to 1-2 per 500 words MAX (em dash overuse is a documented AI tell).
  - **Multi-plugin coexistence:** removed all 4 global hooks (SessionStart, PreToolUse Write/Edit, SubagentStart, Stop) that previously fired on EVERY operation in EVERY project regardless of working directory. Their work already lives at the right architectural layer (Phase 7 reviewer agent + per-agent rules + Quality Gate). Prior config preserved as reference.
  - **MCP servers now opt-in:** `.mcp.json` ships empty; the 9-server catalog (Notion, Canva, Webflow, Slack, Gmail, GCal, Figma, fal-ai, Replicate) lives in `.mcp.json.connectors-reference`. Activate via existing `cf-connect` skill or `/contentforge:cf-add-integration`.

### Updated
- Marketplace metadata version bumped to 2.3.0

---

## [1.22.0] - 2026-03-31

### Changed
- **socialforge** updated from v1.2.0 to v1.3.0
  - Persistent storage via ${CLAUDE_PLUGIN_DATA} across all 11 scripts
  - Google Drive asset source support (Cowork platform integration + Claude Code local)
  - Cloudinary HTTP MCP (10th connector, professional DAM)
  - 10 HTTP connectors total, all Cowork+Claude Code compatible

### Updated
- Marketplace metadata version bumped to 1.22.0

---

## [1.21.0] - 2026-03-31

### Changed
- **socialforge** updated from v1.1.0 to v1.2.0 — 100% spec coverage achieved
  - Video: Veo 3.1 + routing + SRT subtitles
  - Compositing: edge feathering + color temp matching + reflection
  - Copy: Instagram first-comment + bilingual + campaign hashtags
  - Compliance: forbidden content types
  - Carousel: PDF assembly
  - Matching: same-week freshness penalty

### Updated
- Marketplace metadata version bumped to 1.21.0

---

## [1.20.0] - 2026-03-31

### Changed
- **socialforge** updated from v1.0.1 to v1.1.0
  - Gemini model fixes + ref image limit raised to 14
  - Brand manager expanded (languages, hashtags, illustration style, image rules)
  - Compositing: drop shadow generation
  - LinkedIn fold_at awareness, compliance disclaimers + image rules

### Updated
- Marketplace metadata version bumped to 1.20.0

---

## [1.19.0] - 2026-03-31

### Changed
- **socialforge** updated from v1.0.0 to v1.0.1
  - Complete documentation suite: USER-GUIDE, TESTING-GUIDE, CONNECTORS, CONTRIBUTING, LICENSE, .mcp.json.example
  - README fixed with correct version and documentation links

### Updated
- Marketplace metadata version bumped to 1.19.0

---

## [1.18.0] - 2026-03-31

### Added
- **socialforge** v1.0.0 — NEW PLUGIN: Agency-grade social media calendar automation with asset-first compositing. 14 skills, 17 scripts, 5 agents, 18 commands, 8 carousel templates, 9 HTTP connectors, 11 reference docs. 4 creative modes, multi-brand, multi-tier approval, compliance checking.

### Updated
- Marketplace now has 3 plugins (was 2)
- Marketplace metadata version bumped to 1.18.0

---

## [1.17.0] - 2026-03-31

### Changed
- **digital-marketing-pro** updated from v2.6.0 to v2.7.0
  - All 141 skill descriptions trimmed to <130 chars (skill discovery budget optimization)
  - maxTurns added to all 25 agents (runaway execution prevention)
  - launch-plan protected with disable-model-invocation (18 total)
  - SessionStart timeout wrapper on setup.py
  - 169 files changed, zero feature changes

### Updated
- Marketplace metadata version bumped to 1.17.0

---

## [1.16.0] - 2026-03-31

### Changed
- **contentforge** updated from v3.7.1 to v3.8.0
  - Agent compression: 11,503 → 4,957 lines (-57%). ALL quality gates and logic preserved.
  - maxTurns on all 13 agents (prevents runaway execution)
  - Skill descriptions trimmed to <130 chars (fits discovery budget)
  - 4 more execution skills protected with disable-model-invocation
  - 31 files changed, 7,620 lines removed, ~20,000 tokens saved per pipeline run

### Updated
- Marketplace metadata version bumped to 1.16.0

---

## [1.15.0] - 2026-03-31

### Changed
- **contentforge** updated from v3.7.0 to v3.7.1
  - User guidance overhaul: Quick Start in SessionStart, progressive brand setup, expanded troubleshooting
  - Phase progress indicators in agents 01, 03, 07 with ETAs and conditional post-decision updates
  - Token tracking reframed as Pipeline Complexity metrics (words, sources, loops — not token estimates)

### Updated
- Marketplace metadata version bumped to 1.15.0

---

## [1.14.0] - 2026-03-31

### Changed
- **contentforge** updated from v3.6.0 to v3.7.0
  - Title curation overhaul: SERP reconnaissance, content-type-specific angles, brand personality adaptation, guardrails validation, 60-char SERP limit, anti-clickbait
  - Pre-flight brand validation: completeness check before pipeline, regulated industry guardrails enforcement
  - Phase 3 + Phase 5: empty guardrails now report "SKIPPED" with scoring penalty instead of false "zero violations"
  - Scoring fixes: GEO as SEO sub-score, industry threshold overrides, dimension minimums, rounding precision
  - Tracking: per-phase timing columns, token estimates, guardrails status, pipeline performance in output
  - Brand template: visual_identity, content_pillars, competitor_analysis fields
  - Brand setup: 4 new steps (audience personas, competitors, pillars, visual identity)
  - 3 new evals (6 total), 16 files changed, 31 audit findings addressed

### Updated
- Marketplace metadata version bumped to 1.14.0

---

## [1.13.0] - 2026-03-31

### Changed
- **contentforge** updated from v3.5.1 to v3.6.0
  - Optional AI image generation via fal.ai (HTTP) and Replicate (HTTP) — works in both Cowork and Claude Code
  - 3 additional npx image gen servers: Stability AI, nanobanana (Gemini), mcp-imagenate (multi-provider)
  - Phase 3.5 Visual Asset Annotator: user opt-in, feature/contextual/diagram generation, approval flow
  - Phase 6 SEO: feature image og:image meta tag awareness
  - Phase 8 Output: AI image embedding with attribution
  - Phase 10 Social: Canva MCP social graphics generation
  - effort frontmatter on all 16 skills
  - SubagentStart hook (brand injection) and Stop hook (quality gate)
  - ${CLAUDE_PLUGIN_DATA} persistent storage with legacy fallback
  - 29 files changed, 9 HTTP connectors (was 7), 4 hooks (was 2)

### Updated
- Marketplace metadata version bumped to 1.13.0

---

## [1.12.0] - 2026-03-30

### Changed
- **contentforge** updated from v3.5.0 to v3.5.1
  - Mandatory title curation step before pipeline starts — generates 4-5 SEO-optimized title options, user selects before Phase 1 Research begins
  - Pipeline no longer auto-selects titles from topics
  - Updated: create-content command, contentforge skill, Phase 1 agent, README pipeline diagram

### Updated
- Marketplace metadata version bumped to 1.12.0

---

## [1.11.0] - 2026-03-30

### Changed
- **digital-marketing-pro** updated from v2.5.1 to v2.6.0
  - 6 new SEO sub-skills: programmatic-seo, competitor-pages, image-seo-audit, page-seo-analysis, sitemap-manager, seo-plan
  - schema-generator.py expanded from 9 to 18 types with deprecation warnings (HowTo, FAQPage)
  - 2 new reference files: schema-templates.json (12 JSON-LD templates), google-seo-reference.md (E-E-A-T, CWV, spam policies)
  - seo-specialist agent updated with all new skills and reference files
  - DataForSEO MCP integration added (live SERP data, keyword research, backlinks, 9 API modules)
  - All new skills include user-invocable: true and argument-hint per convention
  - Counts: 141 skills, 148 reference files, 68 npx integrations

### Updated
- Marketplace metadata version bumped to 1.11.0

---

## [1.8.0] - 2026-03-04

### Changed
- **contentforge** updated from v3.3.0 to v3.4.0
  - 10 industry knowledge packs for subject matter expertise (pharma, BFSI, healthcare, technology, B2B SaaS, legal, eCommerce, consumer goods, real estate, education)
  - Brand-setup Step F: auto-generated brand key files from website analysis
  - Phase 3 SME Calibration via industry knowledge packs
  - Phase 4 domain-specific validation (terminology, regulatory, evidence standards)
  - Pipeline documentation corrected to 10-phase (Phase 3.5 Visual Asset Annotator)
  - Version alignment across all files (plugin.json, hooks.json, README)

### Updated
- Marketplace metadata version bumped to 1.8.0

---

## [1.7.0] - 2026-03-03

### Changed

- Updated contentforge to v3.3.0:
  - **v3.2.0**: New Phase 3.5 Visual Asset Annotator agent (13 agents total) — auto-generates matplotlib data charts from verified statistics, creates structured `<!-- VISUAL: ... -->` and `<!-- INTERNAL-LINK: ... -->` markers, embeds charts in .docx with TODO boxes for human-action visuals
  - **v3.3.0**: Google Sheets tracking + Google Drive delivery via Python scripts with service account — `sheets-tracker.py` (init, add-row, get-pending, update-row, mark-complete) and `drive-uploader.py` (upload, ensure-folders, upload-assets with Brand/Type/Year/Month hierarchy)
  - **Audit fixes**: requirement_id collision prevention, query injection fix for apostrophe brand names, priority validation, error checking between script calls
- Updated marketplace.json and README.md with current plugin versions and descriptions

---

## [1.6.0] - 2026-02-26

### Changed

- Updated digital-marketing-pro to v2.5.0 — adds 7 command files visible in Customize panel (brand-setup, campaign-plan, seo-audit, content-engine, performance-report, competitor-analysis, email-sequence)
- Updated contentforge to v3.1.0 — adds 7 command files visible in Customize panel (create-content, content-brief, social-adapt, publish, translate, brand-setup, audit-content), new `/cf:help` and `/cf:add-integration` skills
- Updated marketplace.json and README.md with current plugin versions and descriptions

---

## [1.5.0] - 2026-02-25

### Changed

- Updated contentforge to v3.0.0 — Complete modernization: 14 new skills, 2 new agents (Social Adapter, Translator), 4 agent upgrades (Output Manager, SEO Optimizer, Humanizer, Reviewer), connector infrastructure, comprehensive user guide
- Updated marketplace descriptions and version references in README.md

---

## [1.4.0] - 2026-02-25

### Changed

- Updated digital-marketing-pro to v2.4.0 — adds connector discovery and onboarding skills (`/dm:integrations`, `/dm:connect`)

## [1.3.0] - 2026-02-25

### Fixed — SSH Host Key Verification Failure in Cowork VM

**Root cause found in Claude debug logs** (`C:\Users\indra\AppData\Roaming\Claude\logs\main.log`):

```
✘ Failed to install plugin "digital-marketing-pro@neels-plugins":
  Failed to clone repository: Host key verification failed.
  fatal: Could not read from remote repository.
```

The Cowork VM doesn't have GitHub's SSH host key in `known_hosts`. When plugins use `"source": "github"`, the VM tries to `git clone` via SSH and fails because it can't verify GitHub's identity.

Anthropic's Marketing plugin installs fine because it uses relative path sources within the same marketplace repo — no git clone needed.

**Fix:** Changed both plugin sources from `"source": "github"` to `"source": "url"` with explicit HTTPS URLs. This forces HTTPS cloning which doesn't require SSH host key verification.

```json
// Before (fails — uses SSH)
"source": { "source": "github", "repo": "indranilbanerjee/digital-marketing-pro" }

// After (works — uses HTTPS)
"source": { "source": "url", "url": "https://github.com/indranilbanerjee/digital-marketing-pro.git" }
```

## [1.2.0] - 2026-02-25

### Fixed — Marketplace Schema & Agent Registration

**Root cause investigation of persistent installation failures:**

Three separate issues identified:

1. **marketplace.json structure wrong** — `version` and `description` were at top level instead of under documented `metadata` object. `$schema` referenced a non-existent URL (returns 404). Undocumented top-level fields may cause silent validation failure in Claude Code's strict schema validator.

2. **2 DM Pro agents missing YAML frontmatter** — `localization-specialist.md` and `quality-assurance.md` had no `---` frontmatter block. Without frontmatter, agent registration fails, potentially causing installation rollback.

3. **Cowork VM EXDEV bug (platform-level)** — [Issue #25444](https://github.com/anthropics/claude-code/issues/25444): Cowork's VM tries `fs.rename()` across different filesystem mounts during plugin installation, failing with EXDEV. Affects ALL third-party marketplace plugins. Not fixable from plugin side.

**Fixes applied:**
- Restructured marketplace.json: moved `version`/`description` into `metadata` object, removed `$schema`, removed `email` from owner
- digital-marketing-pro 2.3.0 → 2.3.1: added YAML frontmatter to 2 agents
- Marketplace version 1.1.0 → 1.2.0

## [1.1.0] - 2026-02-25

### Changed — HTTP Connector Architecture

Both plugins rebuilt to follow Anthropic's official plugin pattern with HTTP-only MCP connectors.

**digital-marketing-pro 2.2.1 → 2.3.0:**
- New `.mcp.json` with 14 HTTP connectors (Slack, Canva, Figma, HubSpot, Amplitude, Notion, Ahrefs, Similarweb, Klaviyo, Google Calendar, Gmail, Stripe, Asana, Webflow)
- New `CONNECTORS.md` with 12 connector categories
- Minimal `plugin.json` (4 fields, matching Anthropic's format)
- Script path resolution: setup.py now outputs plugin root at session start
- `.mcp.json.example` preserved for Claude Code users wanting full 67-server npx config

**contentforge 2.0.2 → 2.1.0:**
- New `.mcp.json` with 6 HTTP connectors (Notion, Canva, Webflow, Slack, Gmail, Google Calendar)
- New `CONNECTORS.md` with connector categories
- Minimal `plugin.json` (4 fields)
- Agent names normalized to kebab-case for proper Cowork routing
- Removed non-standard `skill_type` field from skill frontmatter
- `.mcp.json.example` preserved for Google Sheets/Drive (npx only)

### Marketplace

- Simplified plugin descriptions to match Anthropic's concise style
- Removed `homepage`, `repository`, `email` from plugin entries
- Marketplace version 1.0.4 → 1.1.0

## [1.0.4] - 2026-02-24

### Updated

**Plugin version bumps reflecting bug fix releases:**
- digital-marketing-pro: 2.2.0 → **2.2.1** — Fixed CLI argument mismatches in 8 SKILL.md files, removed undefined `${CLAUDE_PLUGIN_ROOT}` from 53 files, fixed content-scorer.py and hallucination-detector.py bugs, simplified hooks.json
- contentforge: 2.0.1 → **2.0.2** — Added YAML frontmatter to all 10 agents for Cowork routing, replaced 5 invented MCP tool names in Output Manager with adaptive approach

### Fixed
- ContentForge description: "9-phase autonomous pipeline" → "10-agent autonomous pipeline" (was undercounting Agent 06.5 Humanizer)

---

## [1.0.3] - 2026-02-17

### 🐛 Fixed

**CRITICAL: Actually prevented MCP auto-loading (v1.0.2's approach didn't work)**

v1.0.2's marketplace-level `"mcpServers": []` approach **FAILED** — users still saw "24 MCP servers failed" errors because the `.mcp.json` files in plugin repos were being auto-discovered regardless of marketplace configuration.

**Root cause identified:**
- `.mcp.json` at plugin root is auto-discovered by Claude Code's plugin loader
- Marketplace `"mcpServers": []` only **adds** to what the plugin declares, it **cannot suppress** files already in the repo
- The only way to prevent auto-loading is to **rename the file** so it's not discovered

**Fix implemented:**
- **Renamed `.mcp.json` → `.mcp.json.example`** in both plugin repos (digital-marketing-pro v2.2.1, contentforge v2.0.2)
- Updated plugin READMEs with copy instructions: `cp .mcp.json.example .mcp.json`
- Removed useless `"mcpServers": []` declarations from marketplace.json (they never worked)
- MCP integrations now **truly opt-in** — file must be manually copied and configured

### ✅ Expected Outcome

- ✅ **NO MCP servers auto-load** on plugin installation (file doesn't exist with discoverable name)
- ✅ **NO "X MCP servers failed" errors** on startup
- ✅ Plugins install cleanly without any MCP-related failures
- ✅ "Manage Plugin" shows all 115 skills + 25 agents (digital-marketing-pro) and 3 skills (contentforge)
- ✅ Users who want MCP integrations copy `.mcp.json.example` to `.mcp.json` and configure credentials

### 📝 Technical Notes

The marketplace `"mcpServers"` field is a **component path field** that specifies **additional** MCP configs to load on top of what the plugin repo already declares. An empty array `[]` means "add no additional servers" — it does **NOT** mean "suppress the servers declared by the plugin repo itself."

The only reliable way to prevent `.mcp.json` auto-discovery is to not have the file at that exact location. Renaming it to `.mcp.json.example` prevents auto-discovery.

**Plugin versions updated:**
- digital-marketing-pro: 2.2.0 → 2.2.1 (`.mcp.json` renamed)
- contentforge: 2.0.1 → 2.0.2 (`.mcp.json` renamed)

---

## [1.0.2] - 2026-02-17

### ⚠️ Known Issue

This version's marketplace-level `"mcpServers": []` approach **did not work** — MCP servers were still being auto-loaded from plugin repos. **Upgrade to v1.0.3 immediately.**

### 🐛 Fixed

**CRITICAL: Resolved "Manage Plugin shows nothing" regression from v1.0.1**

v1.0.1 introduced a critical regression where plugins would install without crashing, but "Manage Plugin" would show nothing and redirect back to the platform. The root cause was a misunderstanding of how `"strict": false` works in marketplace.json.

**What `"strict": false` actually does:**
- The marketplace entry becomes the **ENTIRE definition** of the plugin
- The plugin's own `plugin.json` is completely ignored
- Only components explicitly declared in marketplace.json are loaded

By setting `"strict": false` with only `"mcpServers": []` declared, we told Claude Code to install the plugin with **zero components** (no skills, agents, or hooks), which caused the empty plugin management UI.

**Fix implemented:**
- **Removed `"strict": false`** from both plugin entries (digital-marketing-pro and contentforge)
- Kept `"mcpServers": []` to suppress MCP auto-loading
- With default `strict: true`, the plugin's own plugin.json is the authority, and the marketplace entry supplements it
- Skills, agents, and hooks now auto-discover correctly from the plugin repos

### ✅ Expected Outcome

- ✅ Plugins install without Claude Desktop crashing (MCP still suppressed)
- ✅ **"Manage Plugin" now shows all 115 skills + 25 agents** (digital-marketing-pro)
- ✅ **"Manage Plugin" now shows all 3 skills** (contentforge)
- ✅ All plugin functionality works immediately after installation
- ✅ MCP integrations remain opt-in (no auto-loading of unconfigured servers)

### 📝 Technical Notes

The correct marketplace.json configuration uses default `strict: true` (implicit):
```json
{
  "name": "digital-marketing-pro",
  "source": { "source": "github", "repo": "indranilbanerjee/digital-marketing-pro" },
  "mcpServers": [],
  ...
}
```

**No `"strict": false` declaration.** The `mcpServers: []` field in the marketplace entry supplements/overrides the plugin's MCP configuration while allowing skills, agents, and hooks to auto-discover from the plugin repo's default locations.

---

## [1.0.1] - 2026-02-17

### ⚠️ Known Issue

This version introduced a regression where "Manage Plugin" shows nothing after installation. **Upgrade to v1.0.2 immediately.**

### 🐛 Fixed

**CRITICAL: Resolved "Couldn't connect to Claude" error on plugin installation**

The root cause was identified: when users installed plugins from the neels-plugins marketplace, Claude Desktop attempted to start **all 67 MCP servers** (from digital-marketing-pro) or 2 MCP servers (from contentforge) simultaneously on startup. Most MCP servers failed immediately due to missing API keys, environment variables, and credentials, causing a cascade of MCP startup failures that crashed Claude Desktop with "Couldn't connect to Claude" error.

**Fixes implemented:**
- Added `"strict": false` and explicit `"mcpServers": []` to all plugin entries in marketplace.json to suppress MCP auto-loading on installation
- MCP integrations are now opt-in and require manual configuration after plugin installation
- This prevents Claude Desktop from attempting to start unconfigured MCP server processes

### ✨ Changed

- **Added official `$schema` reference** — Marketplace now includes `https://anthropic.com/claude-code/marketplace.schema.json` for proper validation and clearer error messages
- **Aligned structure with official Anthropic format** — Moved `version` and `description` from nested `metadata` object to top level to match the official marketplace.json schema used by Anthropic
- **Improved documentation** — Added MCP setup warnings to both plugin READMEs (digital-marketing-pro and contentforge) to clearly communicate that MCP integrations require manual configuration

### 📝 Technical Notes

**What users will notice:**
- ✅ Plugins install without Claude Desktop crashing
- ✅ "Manage Plugin" button opens the management UI correctly (no more redirects)
- ✅ Plugins don't ask to reinstall after already being installed
- ✅ Claude Desktop starts successfully with plugins installed
- ✅ All skills and agents work immediately

**What changed for MCP integrations:**
- MCP servers are no longer auto-registered during plugin installation
- Users who want MCP integrations (social publishing, CRM sync, ad campaign creation, etc.) must configure them manually following the integration guides
- All plugin functionality works without MCP — MCP is only needed for executing actions on external platforms

**Backward compatibility:**
- Existing users who already have MCP servers configured will continue to work normally
- This change only affects new installations from the marketplace

### 📚 References

- Issue: Claude Desktop "Couldn't connect to Claude" error on plugin installation
- Root cause: MCP server cascade failures during startup
- Solution: Suppress MCP auto-loading via marketplace-level configuration

---

## [1.0.0] - 2026-02-15

### 🎉 Initial Release

**Neel's Plugin Marketplace** — AI-powered plugins for Claude Code and Claude Cowork

**Featured Plugins:**
- **digital-marketing-pro** v2.2.0 — Comprehensive digital marketing execution system with 25 specialist agents, 16 integrated modules, 115 slash commands, 67 MCP integrations, agency operations, multilingual support, and quality assurance layer
- **contentforge** v2.0.0 — Enterprise multi-agent content production with batch processing, content refresh, multilingual support, platform integrations, and analytics

**Marketplace Features:**
- GitHub-based plugin distribution
- Automatic version management
- Plugin metadata and discoverability
- Integration with Claude Code and Cowork

---

[1.8.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.0.4...v1.1.0
[1.0.4]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/indranilbanerjee/neels-plugins/releases/tag/v1.0.0
