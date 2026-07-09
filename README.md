# Neel's Plugin Marketplace

> **You run marketing for a single brand, an agency portfolio, or a content team — and you want the same depth across every brand, every article, every campaign, with no per-platform lock-in. You don't want to learn six different "AI marketing" SaaS UIs that all charge per-seat per-month.**

Install three open-source plugins from one marketplace. Same skills, same agents, same outputs across **Claude Code**, **Anthropic Cowork**, **OpenAI Codex**, **Cursor 2.5+**, **GitHub Copilot CLI**, **Google Antigravity 2.0**, **Hermes Agent**, and **OpenClaw** + 35+ additional Agent Skills platforms — via the Agent Skills open standard. Zero global hooks, zero auto-connecting MCP servers, MIT-licensed, no telemetry, no seats.

[![Version](https://img.shields.io/badge/version-3.16.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-3-orange.svg)](#-available-plugins)
[![Total skills](https://img.shields.io/badge/skills-195%20across%20suite-blueviolet.svg)](#which-plugin-do-i-need)
[![Total tests](https://img.shields.io/badge/tests-404%20across%20suite-brightgreen.svg)](#whats-new)
[![Surfaces](https://img.shields.io/badge/all%203%20plugins-8%20native%20%2B%2035%20Agent%20Skills-success.svg)](#-platform-compatibility)
[![Cowork](https://img.shields.io/badge/Cowork-team%20persistent-brightgreen.svg)](#-platform-compatibility)

> 🆕 **July 7, 2026 — marketplace v3.16.0: Digital Marketing Pro v3.15.0, the Reliability & Truth release.** A full-repo audit (orchestration / agents / skills / commands / scripts / docs-manifests) surfaced ~200 findings — all fixed in one coordinated pass, mirroring ContentForge's v3.16.0. One shared `_common.py` ends the storage split-brain; a new doc-vs-argparse contract linter (`check_skill_contracts.py`) locks every skill invocation to real script flags; all 18 execution skills carry a uniform typed-approval gate + `disable-model-invocation: false` (**closes issue #6**); the Tessl review workflow moved to the `tessl review` CLI (**closes issue #8**); agents consolidated 25 → 24; `embed-c2pa.py` gained the EU AI Act Article 50 `--ai-disclosure` assertion; connectors are honestly opt-in (fictional npm packages purged). DMP tests 123 → **207**. **404 tests passing** (DMP 207 + CF 143 + SF 54). [Read what's new →](#whats-new) · [Full changelog →](CHANGELOG.md)

A custom plugin marketplace by [Indranil Banerjee](https://indranil.in) · [LinkedIn](https://www.linkedin.com/in/askneelnow/) · [X](https://x.com/askneelnow). Agent Skills was donated to the Agentic AI Foundation December 2025; adopted by **41+ agent products** by June 2026.

---

## Which plugin do I need?

| Your job-to-be-done | Install | What's in the box |
|---|---|---|
| **Run end-to-end brand-strategy engagements across a portfolio** (agencies, in-house, consultants) | [`digital-marketing-pro`](https://github.com/indranilbanerjee/digital-marketing-pro) | 158 skills · 24 agents · 12-Part Strategy Flow · 6-platform AEO/GEO · EU AI Act Article 50 · Cowork-team-persistent · multi-brand · multi-jurisdiction compliance |
| **Produce publish-ready long-form content** (blog posts, white papers, case studies, executive briefs) | [`contentforge`](https://github.com/indranilbanerjee/contentforge) | 21 skills · 13 agents · 10 quality gates · 35-pattern AI humanizer · fact-checker · real `.docx` output · C2PA signing |
| **Produce social media assets at agency scale** (carousels, single-image posts, AI image / video creatives) | [`socialforge`](https://github.com/indranilbanerjee/socialforge) | 16 skills · 25 commands · asset-first compositing · AI image (Vertex AI Nano Banana Pro) · AI video (Kling v3.0 Pro) · C2PA signing |

**The three plugins are complementary, not overlapping.** A typical agency workflow uses all three: DMP for strategy + campaign planning, ContentForge for the long-form articles a campaign produces, SocialForge for the social assets a campaign produces. All three share the same brand-state directory (`~/.claude-marketing/<brand>/`) so a brand profile created in DMP is immediately picked up by CF and SF.

---

## Who this suite is for

| If you're a... | Why this matters |
|---|---|
| 🏢 **Marketing agency** (50–200 brands) | One toolchain across every client, audit-trail compliance, new-hire onboarding from 6 weeks → 6 hours, Cowork team persistence so your senior strategists work in browser-based Cowork while your team Drive has every artifact. |
| 👔 **In-house marketing team** | Single canonical strategy document underwriting every campaign + content piece. No more "the deck and the blog post say different things." |
| 🚀 **Marketing automation builder** (n8n / Zapier / Make / Pipedream) | DMP's connector-resolver + executor pattern. 8 verified HTTP connectors execute end-to-end; 25 more return manifest-ready specs for OAuth-mediated platforms. |
| 💼 **Solo consultant** / freelance marketer | Per-engagement billing model: 50–60 canonical files for $15–40 of API spend in ~60 minutes. Installs on Codex / Cursor / Copilot CLI / Antigravity for terminal-native or IDE-native workflows. |
| 📈 **Growth team** / product marketer | Funnel architecture, attribution, MMM, incrementality testing, retention, churn — all anchored to the strategy document. |
| 🛡 **Compliance-led marketer** (EU · UK · India · Brazil · California) | EU AI Act Article 50, C2PA content provenance, deepfake disclosure, GDPR + CCPA + DPDPA + LGPD + 12 more jurisdictions baked into every output. |

---

## What's new

### v3.16.0 (July 7, 2026) — Digital Marketing Pro v3.15.0: the Reliability & Truth release

DMP v3.14.1 → **v3.15.0** + marketplace v3.15.0 → **v3.16.0**. (CF v3.16.0 and SF v1.13.1 unchanged.)

A full-repo audit (orchestration / agents / skills / commands / scripts / configs-docs-manifests) surfaced ~200 findings — all fixed in one coordinated pass, mirroring ContentForge's v3.16.0 the day before. DMP tests 123 → **207** (suite total 404):

- **Storage split-brain fixed** — one shared `_common.py` (`workspace_root` / `slugify_brand` / atomic writes / `finish`) adopted across the script layer; ends the four-different-slugifier bug that misfiled Cowork/Drive brand state.
- **Doc↔script contract linter** — new `check_skill_contracts.py` parses every fenced script call in skills/commands/agents and validates actions/flags against each script's real argparse (0 mismatches, wired into CI).
- **Issue #6 closed** — all 18 execution skills carry a uniform `## Execution gate` (typed approval, cancel-on-anything, never-proceed-on-ambiguous input) + `disable-model-invocation: false` so Codex's frontmatter validator stops erroring.
- **Issue #8 closed** — Tessl review workflow moved from the retired `tesslio/skill-review@main` Action to the `tessl review` CLI + `.github/tessl-rubric.yml`.
- **EU AI Act Article 50** — `embed-c2pa.py --ai-disclosure` embeds the C2PA 2.4 `c2pa.ai-disclosure` assertion (applicable Aug 2, 2026).
- **Agents 25 → 24** — `competitor-intelligence` merged into `competitive-intel` (`mode: snapshot|monitoring`); `memory-manager` thinned to storage-only; `intelligence-curator` owns intake/interpretation.
- **Connector honesty** — the "13 connectors pre-configured" fiction removed (shipped `.mcp.json` is empty), fictional npm packages purged, memory backends demoted to "only if you have a working server connected".

### v3.15.0 (July 7, 2026) — ContentForge v3.16.0: the Reliability & Truth release

CF v3.15.3 → **v3.16.0** + marketplace v3.14.1 → **v3.15.0**. (DMP v3.14.1 and SF v1.13.1 unchanged.)

The deepest ContentForge engineering pass since v3.0 — a five-layer audit (orchestration / agents / skills / scripts / configs) implemented end to end. CF tests 53 → **143** (suite total 320):

- **Checkpoint/resume actually wired** — every phase saves to a canonical run directory; `/contentforge:resume` works for skill-started runs, honors mid-loop rework, reloads run metadata.
- **File-based phase handoff contract** — agents read prior artifacts by path; full Pipeline Contract table (inputs → outputs → gate → loop target).
- **Measured gates** — new `text-metrics.py` computes burstiness / FK grade / keyword placements; orchestrator verifies instead of trusting subagent self-reports. Density gate retired for placement checks.
- **GEO protection** — Phase 6 structure manifest stops the humanizer from dismantling answer blocks; humanizer catalog 29 → 35 patterns with a defined AI-signal formula.
- **EU AI Act Article 50** (applicable Aug 2, 2026) — AI-disclosure step in the publish path + per-platform AI-label fields; social specs add TikTok, Bluesky, YouTube Shorts.
- **Script hardening** — shared `_common.py` (single slugifier fixes the Cowork sync-path bug, atomic writes, Windows UTF-8 guard, real exit codes); .docx gets image embedding + TOC + page footer.
- **Truth pass** — honest "10 phases / 10 quality gates" claim, connector docs match the shipped empty `.mcp.json`, ~50 broken slash references fixed, drift-locking release-consistency tests added.

### v3.14.1 (June 28, 2026) — README-sync patch + test-coverage extension

DMP v3.14.0 → **v3.14.1** + CF v3.15.2 → **v3.15.3** + SF v1.13.0 → **v1.13.1** + marketplace v3.14.0 → **v3.14.1**.

A second-pass cleanup after v3.14.0 caught two real classes of drift the release-consistency suite was not yet covering:

- **Stale README section heading**: DMP's `## Supported surfaces (vX.Y.Z)` was still on v3.13.1 even though every manifest had been bumped to v3.14.0. CF/SF tests caught this kind of drift; DMP's didn't.
- **Stale "What's new" section in DMP README**: the latest entry was v3.13.0; v3.13.1 and v3.14.0 had shipped without being added.

Fixed:
- DMP README — Cowork badge anchor + Supported-surfaces heading + 2nd `#supported-surfaces` anchor + 3 new "What's new" entries (v3.14.1 + v3.14.0 + v3.13.1).
- CF README — added v3.15.3, v3.15.2, v3.15.1 entries to Release notes.
- SF README — rewrote "Current Release" body with actual v1.13.0 content (heading had been renamed but body still described v1.12.0).
- Marketplace README — added v3.14.1 + v3.14.0 entries (this one).
- **DMP `tests/test_release_consistency.py` extended** to lock the `## Supported surfaces (vX.Y.Z)` heading to canonical version + verify all `#supported-surfaces-v…` anchor links match — closes the drift class permanently for DMP (CF/SF already had this).

Suite tests: 222 → **224** (+1 in DMP for new section-heading lock, +1 for anchor-sync lock).

### v3.14.0 (June 28, 2026) — June market-refresh sweep

DMP v3.13.1 → **v3.14.0** + CF v3.15.1 → **v3.15.2** + SF v1.12.1 → **v1.13.0**. Coordinated suite-wide refresh covering everything that shipped, broke, or got deprecated in the marketing-tech ecosystem since the last refresh on 2026-06-09. Every claim verified against primary vendor docs.

- **Meta Graph API bumped v20.0 → v24.0** in DMP `scripts/connector_resolver.py` (4 callsites). Pre-v24 calls scheduled to fail 2026-06-09.
- **Model registry rebuilt to 47 entries** verified against Anthropic / OpenAI / Google primary docs. New active flagships: Claude Opus 4.8, GPT-5.5 family, gpt-image-2, Gemini 3.1 Pro Preview, Gemini 3.1 Flash-Lite, Veo 3.1 Preview, Nano Banana Pro/2 GA. Newly deprecated: full GPT-5 family + o3 family (shutdown 2026-12-11), Gemini 2.5 family (shutdown 2026-10-16), Imagen 4. Newly retired (auto-routed): Gemini 2.0 family (June 1), Gemini 3 preview image variants (June 25), Veo 2.0/3.0/3.0-Fast (June 30).
- **Resolver hardened** — now unconditionally rewrites `retired` model IDs to `replacement_id` (was previously only `deprecated`). New test covers this.
- **`--check-params` scanner** flags unsafe `temperature` / `top_p` / `top_k` near Claude Opus 4.7+ targets (HTTP 400 risk).
- **18 aliases re-pointed** across all 3 plugins. `latest-text-anthropic` → claude-opus-4-8, `latest-text-openai` → gpt-5.5, `latest-video-google` → veo-3.1-generate-preview, `latest-image-photoreal-google` → gemini-3-pro-image (Imagen 4 was deprecated path).
- **Google Ads API v24.1 + v24.2** sections added to DMP `skills/paid-advertising/google-ads.md` — ADOPT_AI_MAX experiment type, mobile_device_platform segment, Local Services Ads via `google_local_services_info`, GENERATE_LANDING_PAGE_TEXT, beta MultiPartyAuthReview.
- **EU AI Act Code of Practice second-draft refresh** in DMP `skills/context-engine/eu-code-of-practice.md` — Section 1 two-layered marking (C2PA satisfies metadata), Section 2 dropped AI-generated-vs-AI-assisted taxonomy, operational readiness checklist for 2026-08-02 applicability.
- **I/O 2026 additions** to DMP `aeo-audit` (Information Agents callout) + `local-seo` (Agentic Booking expansion to local services / home repair / beauty / pet care).
- **EvoLink vendor** added to the model curator via community PR (multi-provider API gateway aggregating DeepSeek / Doubao / MiniMax via single API key).
- **Suite-wide `docs/MODEL-CURATOR.md` refresh** with current aliases table + new § "Parameter compatibility — Claude Opus 4.7 and later".

Suite tests: 221 → **222** in this entry (DMP 115 + CF 53 + SF 54). Then v3.14.1 brought it to 224.

### v3.13.1 (June 9, 2026) — Suite-wide test-infrastructure polish

CF v3.15.0 → **v3.15.1** + SF v1.12.0 → **v1.12.1**. DMP unchanged at v3.13.1. Mirrors DMP's v3.13.1 test-infra polish into the other two plugins.

- **CF release-consistency suite** added (`tests/test_release_consistency.py`, +30 tests; CF total **23 → 53**)
- **SF release-consistency suite** added (+31 tests; SF total **23 → 54**)
- **Suite total: 160 → 221 tests** passing (DMP 114 + CF 53 + SF 54)
- Each suite catches: cross-manifest version drift (7 manifest files per plugin), README badge staleness, hero-callout drift, CHANGELOG out-of-sync, install commands going missing, critical README sections going missing, internal anchor links pointing at non-existent headings, byte-identical description sharing across the 5 Claude-family manifests, and skill-count claims that don't match `skills/` directory contents
- **SF descriptions sharpened**: all 5 Claude-family manifests now lead with `16 skills` (was a generic feature list) — better marketplace search relevance + the new test enforces the count going forward
- **SF README** fixed: broken internal anchor `#current-release-v182` re-pointed at the live Current Release section

### v3.13.0 (June 9, 2026) — Suite-wide multi-harness parity

CF v3.14.0 → **v3.15.0** + SF v1.11.0 → **v1.12.0**. DMP unchanged at v3.13.1. Brings ContentForge + SocialForge into native Hermes Agent + native OpenClaw parity with DMP. Now all 3 plugins ship `plugin.yaml` + `__init__.py` (Hermes adapter) + `openclaw.plugin.json` at their repo root, plus a stdlib-unittest suite.

- **All 3 plugins now on 8 native platforms** (Claude Code · Cowork · Codex · Cursor · Copilot CLI · Antigravity · Hermes Agent · OpenClaw) + 35+ Agent Skills clients
- **Tests across the suite: 160 passing** (DMP 114 + CF 23 + SF 23) — was 0 in CF + SF before this release
- Skill counts unchanged: DMP 158 + CF 21 + SF 16 = **195 total**

### v3.12.1 (June 9, 2026) — DMP test infrastructure hardening

DMP v3.13.0 → **v3.13.1**. CF + SF unchanged. Test suite expanded 70 → 114 with cross-manifest drift detection. New `tests/test_release_consistency.py` (25 tests) catches version drift, README badge staleness, CHANGELOG out-of-sync, install commands going missing, critical sections going missing, broken anchor links. New `tests/test_hermes_edge_cases.py` (10 tests) for adapter resilience. New README sections: "Get started in 5 minutes (non-developer path)" + "Troubleshooting" covering all 8 native platforms.

### v3.12.0 (June 9, 2026) — DMP Hermes Agent + OpenClaw + 40+ Agent Skills

DMP v3.12.1 → **v3.13.0**. CF + SF unchanged. Native Hermes Agent plugin (plugin.yaml + Python adapter at repo root walking skills/ and registering via `ctx.register_skill()`). Native OpenClaw manifest (openclaw.plugin.json with skills: `["./skills"]`). 35 additional Agent Skills platforms documented (Goose, OpenHands, OpenCode, Junie, Gemini CLI, Roo Code, Kiro, Letta, Amp, and 26 more). Test count 49 → 70.

### v3.11.1 (June 8, 2026) — Discoverability + documentation polish

DMP v3.12.0 → **v3.12.1**. CF + SF unchanged. README "Who this is for" audience table (agencies / in-house / automation builders / consultants / growth / compliance). "How does this compare?" table vs Anthropic Marketing, Composio Marketing, claude-seo. "Real workflows you'd actually run" with 6 copy-paste examples. Recent-release callout at top. 2 new FAQ entries (Cowork persistence + model freshness). GitHub repo descriptions + topics refreshed across all 4 repos for SEO.

### v3.11.0 (June 8, 2026) — DMP Cowork persistence + fallback models + tests

DMP v3.11.0 → **v3.12.0**. CF + SF unchanged. Research-grounded hardening pass after web research confirmed `${CLAUDE_PLUGIN_DATA}` is NOT persistent across Anthropic Cowork sessions ([GitHub issue #51398](https://github.com/anthropics/claude-code/issues/51398)). DMP now ships a new `/digital-marketing-pro:cowork-setup` skill that routes brand state through a Google Drive MCP. Plus `fallbackModel` chain in `settings.json.example`, `requiredMinimumVersion: 2.1.157` in plugin.json, model-registry freshness check in `/doctor`, 49-test stdlib suite.

## What's new in v3.10.0 (June 4, 2026) — DMP v3.11.0 SEO expansion

DMP bumped 3.10.1 → 3.11.0. CF + SF unchanged. Three new SEO skills (keyword-cluster / backlink-gap / seo-drift) + pattern upgrades across 10 existing SEO skills (Confirm-Then-Dispatch dispatcher, numbered intermediate-file output, quality scorecards). See [DMP CHANGELOG.md](https://github.com/indranilbanerjee/digital-marketing-pro/blob/main/CHANGELOG.md) for the full entry.

## What's new in v3.9.0 (June 4, 2026)

Coordinated platform-refresh release: **DMP v3.10.0** + **SF v1.11.0**. Every claim verified against primary sources before code changes.

- **DMP** ships a new `/digital-marketing-pro:gsc-ai-performance` skill for the Google Search Console AI Performance Report rolled out 3 June 2026, plus a new `skills/context-engine/eu-code-of-practice.md` reference doc for EU AI Act Article 50 transparency. Updates to `aeo-geo`, `aeo-audit`, `c2pa-metadata`, `paid-advertising` (Google Ads API v24 breaking changes), `analytics-insights` + `attribution-report` (GA4 AI Assistant channel group added 13 May 2026).
- **SF** ships C2PA spec refresh — Content Credentials 2.3 expanded formats + Spec 2.4 `c2pa.ai-disclosure` assertion for Article 50 deployer compliance.

---

## 🚀 Quick Start

### 1. Add this marketplace to Claude

```
/plugin marketplace add indranilbanerjee/neels-plugins
```

In Cowork: Settings → Plugins → Add Marketplace → paste `indranilbanerjee/neels-plugins`.

### 2. Browse available plugins

```
/plugin list neels-plugins
```

### 3. Install a plugin

```
/plugin install contentforge@neels-plugins
```

(Replace `contentforge` with `digital-marketing-pro` or `socialforge` as desired.)

### 4. Stay current — turn auto-update on (recommended)

**Third-party marketplaces have auto-update OFF by default in Claude Code.** When we ship a new ContentForge / DM Pro / SocialForge release, you will not be notified — you will keep running whatever version you installed first.

To get future updates automatically: open `/plugin`, go to the **Marketplaces** tab, find `neels-plugins`, and toggle **Enable auto-update**. After an auto-update fires you will be prompted to run `/reload-plugins` to pick up changes mid-session (no full Claude Code restart needed; conversation context preserved).

To update manually instead, see the [Updating](#updating) section below.

---

## 📦 Available Plugins

| Plugin | Version | What it does |
|--------|---------|--------------|
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 3.15.0 | The most comprehensive open-source AI marketing plugin — 158 skills, 24 specialist agents, 12-Part Strategy Flow producing the Four Core Documents, Two-Views Model, Decision Matrix, Living Project Instruction File. Built for marketing agencies, in-house teams running 50–200 brands, and consultancies. EU AI Act Article 50 ready (C2PA content provenance signing + `embed-c2pa.py --ai-disclosure`). 6-platform AEO/GEO audit including Google AI Mode. 16 privacy-law jurisdictions. 8 verified HTTP MCP connectors (opt-in; more return manifest-ready specs), 86 Python scripts (optional), 169 reference knowledge files, 18 top-level slash commands. **v3.15.0** (Reliability & Truth) ships one shared `_common.py` (ends the storage split-brain), a doc-vs-argparse contract linter, uniform typed-approval execution gates (closes issue #6), and the Tessl CLI review workflow (closes issue #8). **207 tests** passing. |
| **[contentforge](https://github.com/indranilbanerjee/contentforge)** | 3.16.0 | Open-source enterprise content production pipeline — **21 skills**, 13 specialist agents, 10 quality gates, 35-pattern AI-detection humanizer, fact-checker subagent, three-category internal linking (topical / commercial / authority), real .docx output with embedded SEO + Quality + Production + Internal-Link appendices. EU AI Act Article 50 ready via `--c2pa-sign` on `scripts/generate-docx.py`. 16 opt-in HTTP MCP connectors catalogued in `.mcp.json.connectors-reference`. **v3.15.x** ships real native manifests for Codex / Antigravity / Cursor / Copilot CLI / Hermes Agent / OpenClaw — installs on all 8 native platforms + 35+ Agent Skills clients. **143 tests** passing (checkpoint roundtrip, docx parser, text metrics + release-consistency drift locks added in v3.16.0). |
| **[socialforge](https://github.com/indranilbanerjee/socialforge)** | 1.13.1 | Open-source agency-grade social media production engine — calendar parsing, asset-first compositing, AI image generation (Vertex AI Nano Banana Pro), AI video generation (WaveSpeed Kling v3.0 Pro), multi-platform copy adaptation (Instagram, TikTok, LinkedIn, Threads, X, Facebook, YouTube Shorts), human-in-the-loop review galleries, C2PA signing for EU AI Act Article 50 compliance. **16 skills**, 25 commands, 5 agents, 22 scripts, 10 HTTP MCP connectors (all Cowork-compatible), 0 global hooks. Four creative modes (ANCHOR_COMPOSE / ENHANCE_EXTEND / STYLE_REFERENCED / PURE_CREATIVE). **v1.12.x** ships real native manifests for Codex / Antigravity / Cursor / Copilot CLI / Hermes Agent / OpenClaw — installs on all 8 native platforms + 35+ Agent Skills clients. **54 tests** passing (release-consistency suite added in v1.12.1). |

> **v3.7.0 (2026-05-27): real native manifests for 5 surfaces.** Ships verified-real manifests for OpenAI Codex (`.codex-plugin/plugin.json` per the published OpenAI schema), Google Antigravity 2.0 (`gemini-extension.json` at repo root per Google's `gemini-cli-extensions/data-agent-kit-starter-pack` reference pattern), Cursor 2.5+ (`.cursor-plugin/plugin.json` per the verified Cursor JSON Schema), and GitHub Copilot CLI (`.github/plugin/plugin.json` per the verified GitHub schema). All three plugins ship matching native manifests in their own repos at the same version bump (DMP 3.8.0 / CF 3.13.0 / SF 1.9.0). Replaces the v3.5-v3.6 era invented manifests that were correctly removed in marketplace v3.6.0 on 2026-05-26. Pre-flight verified: all 190 skills across the 3 plugins pass the Codex `[a-z0-9-]` regex.

### Per-platform install commands

```bash
# Claude Code (CLI + IDE extensions)
/plugin marketplace add indranilbanerjee/neels-plugins
/plugin install <plugin-name>@neels-plugins

# Anthropic Cowork — UI only (no /plugin slash commands)
# Plugins panel → Add marketplace → paste indranilbanerjee/neels-plugins → Install

# OpenAI Codex (CLI + IDE + App)
codex plugin marketplace add indranilbanerjee/neels-plugins
codex plugin install <plugin-name>@neels-plugins

# Cursor 2.5+ (in any Agent chat — no marketplace add needed)
/add-plugin digital-marketing-pro@https://github.com/indranilbanerjee/digital-marketing-pro
/add-plugin contentforge@https://github.com/indranilbanerjee/contentforge
/add-plugin socialforge@https://github.com/indranilbanerjee/socialforge

# GitHub Copilot CLI
copilot plugin marketplace add indranilbanerjee/neels-plugins
copilot plugin install <plugin-name>@neels-plugins

# Google Antigravity 2.0 CLI (no marketplace concept — install per-plugin URL)
agy plugin install https://github.com/indranilbanerjee/digital-marketing-pro
agy plugin install https://github.com/indranilbanerjee/contentforge
agy plugin install https://github.com/indranilbanerjee/socialforge
```

---

## 🌐 Platform Compatibility

| Feature | Claude Code CLI | Anthropic Cowork |
|---|---|---|
| All 3 plugins install | ✓ | ✓ |
| Skills, agents, custom commands | ✓ | ✓ |
| Persistent data via `${CLAUDE_PLUGIN_DATA}` | ✓ | ✓ |
| Python scripts via Bash | ✓ | ✓ |
| HTTP MCP connectors (Notion, Canva, Webflow, Slack, Gmail, GCal, Figma, fal-ai, Replicate, Pipedream, Composio, Zapier, Make) | ✓ | ✓ |
| stdio/npx MCP servers (in `.mcp.json.example` files) | ✓ | ✗ — use HTTP aggregators instead |

ContentForge v3.9.1's connectors reference catalog includes Pipedream, Composio, Zapier, and Make.com aggregator MCPs that cover Google Sheets/Drive and 1000+ other SaaS services — these are the recommended path for Cowork users.

---

## 🛡️ Compliance

All three plugins are designed to comply with the [Anthropic Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy):

- No financial transaction processing
- No advertising or ad-serving
- No circumvention of Claude safety guardrails
- AI-generated images (where supported) require explicit user approval and are produced in a clear marketing-content context
- All MCP connectors use OAuth 2.0 or API-key authentication via the connector provider's official endpoint

---

## 🧠 Shared model curator (v3.5.1+)

All three plugins ship the same model-selection infrastructure under `scripts/`:

- **`model_registry.json`** — single source of truth for every AI model id used by the plugin (Claude / GPT / Gemini / Imagen / Veo / Kling / Higgsfield), with vendor, tier, modality, status, and `replacement_id` for deprecated entries.
- **`resolve_model.py`** — resolver. Aliases like `latest-balanced-anthropic`, `latest-image-google`, `latest-video-wavespeed` resolve to concrete ids at call time; deprecated ids passed via `--model` auto-fall-forward to their replacement with a stderr warning.
- **`refresh_models.py`** — polls Anthropic / OpenAI / Google list endpoints with your API keys and reports drift versus the registry.

Why it matters: frontier models change every ~6 weeks. Hardcoding `claude-sonnet-4-5-20250929` or `veo-2.0-generate-001` across dozens of scripts means a provider deprecation silently 404s. The curator prevents that. Each plugin documents the alias map at `docs/MODEL-CURATOR.md`.

---

## 🔧 For Developers

### Adding a New Plugin to This Marketplace

1. Create your plugin with a `.claude-plugin/plugin.json` manifest (include `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`).
2. Push it to its own GitHub repository with a LICENSE file.
3. Add an entry to `.claude-plugin/marketplace.json` in this repo with the `source: { source: "github", repo: "owner/repo" }` format.
4. Bump the marketplace `metadata.version` (semver: minor bump for a new plugin or feature release in an existing plugin; patch for hotfixes).
5. Commit and push — the marketplace updates instantly.

### Marketplace Structure

```
neels-plugins/
├── .claude-plugin/
│   └── marketplace.json     ← Plugin catalog (3 plugins)
├── CHANGELOG.md             ← Release history
├── LICENSE                  ← MIT
└── README.md                ← This file
```

### Plugin Coexistence Pattern

All three plugins follow a strict "no global side-effects" pattern as of May 2026:

- `hooks/hooks.json` ships as `{"hooks":{}}`. Plugin hooks fire globally on every Claude Code operation regardless of working directory, so embedding compliance/verification logic in hooks pollutes unrelated work. The work lives instead in agent files (where it runs in proper context) and Quality Gate criteria.
- `.mcp.json` ships as `{"mcpServers":{}}`. Plugin-bundled MCP servers auto-connect on plugin enable, which means shipping N servers triggers N connection attempts (and likely auth prompts) for users who only want some of them. Each plugin ships its full connector catalog as a `.mcp.json.connectors-reference` file with per-entry auth notes; users opt in via the plugin's connect skill.

If you contribute a plugin to this marketplace, please follow the same pattern.

---

## Updating

> **If you see "/plugin isn't available in this environment"** — you're in the standard **Claude chat app** (browser OR installed desktop app). The `/plugin` slash command is **only** supported in two environments: **Claude Code** (the developer CLI / IDE at [claude.com/code](https://claude.com/code), `npm install -g @anthropic-ai/claude-code`) and **Anthropic Cowork**. Everywhere else — `claude.ai` web chat, the Claude Desktop app, mobile — plugins are managed through the UI, not slash commands.
>
> Plugins from this marketplace still install and run in those environments (skills auto-discover and work normally); only the `/plugin` management command is unavailable.
>
> **Fix:**
> 1. **In the chat UI** — click the **Plugins** button at the bottom of the chat → **Manage plugins** → find the plugin → look for Update / Refresh / Remove. If there's no Update button, **Remove** then **Add plugin** → re-install from `indranilbanerjee/neels-plugins`. The re-pull fetches the latest version.
> 2. **For slash-command management** — switch to Claude Code (CLI or IDE) or Cowork. All three plugins run identically across every Anthropic surface; you're choosing where to type management commands.
>
> The rest of this section assumes you're in Claude Code or Cowork.

There are two paths depending on whether you turned on auto-update during Quick Start step 4.

### If auto-update is ON (recommended)

Claude Code refreshes the marketplace at startup and pulls the latest version automatically. After it fires, run `/reload-plugins` when prompted to pick up the new version mid-session.

### If you prefer manual updates

```
/plugin marketplace update neels-plugins
/plugin uninstall <plugin-name>@neels-plugins
/plugin install <plugin-name>@neels-plugins
/reload-plugins
```

`/plugin marketplace update` only refreshes the catalog — it does not bump installed plugin versions. The uninstall + reinstall is what actually pulls the new version.

### Force-reinstall (version unchanged but content changed)

Happens during fast-iteration debugging:

```
rm -rf ~/.claude/plugins/cache/neels-plugins
/plugin install <plugin-name>@neels-plugins
/reload-plugins
```

### How to know when there's a new version

There is currently no in-product update notification for third-party marketplaces — no banner, no badge. Either:
- Watch this repo on GitHub (Releases) — you'll get an email when we tag a new version
- Check `CHANGELOG.md` in the individual plugin repos
- Or just run `/plugin marketplace update neels-plugins` periodically

---

## 📄 License

MIT © Indranil Banerjee. See [LICENSE](LICENSE).
