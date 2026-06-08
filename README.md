# Neel's Plugin Marketplace

> **You run marketing for a single brand, an agency portfolio, or a content team — and you want the same depth across every brand, every article, every campaign, with no per-platform lock-in. You don't want to learn six different "AI marketing" SaaS UIs that all charge per-seat per-month.**

Install three open-source plugins from one marketplace. Same skills, same agents, same outputs across **Claude Code**, **Anthropic Cowork**, **OpenAI Codex**, **Cursor 2.5+**, **GitHub Copilot CLI**, and **Google Antigravity 2.0** — via the Agent Skills open standard. Zero global hooks, zero auto-connecting MCP servers, MIT-licensed, no telemetry, no seats.

[![Version](https://img.shields.io/badge/version-3.12.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-3-orange.svg)](#-available-plugins)
[![Total skills](https://img.shields.io/badge/skills-195%20across%20suite-blueviolet.svg)](#which-plugin-do-i-need)
[![Surfaces](https://img.shields.io/badge/DMP%20on-8%20native%20%2B%2035%20Agent%20Skills-success.svg)](#-platform-compatibility)
[![Cowork](https://img.shields.io/badge/Cowork-team%20persistent-brightgreen.svg)](#-platform-compatibility)

> 🆕 **June 9, 2026 — marketplace v3.12.0 (DMP v3.13.0):** DMP now ships **native Hermes Agent** + **native OpenClaw** plugins. Plus documented compatibility with **35 additional Agent Skills platforms** (Goose, OpenHands, Junie, Roo Code, Gemini CLI, Kiro, Letta, and 28 more). 70-test stdlib suite. [Read what's new →](#whats-new) · [Full changelog →](CHANGELOG.md)

A custom plugin marketplace by [Indranil Banerjee](https://indranil.in) · [LinkedIn](https://www.linkedin.com/in/askneelnow/) · [X](https://x.com/askneelnow). Agent Skills was donated to the Agentic AI Foundation December 2025; adopted by ~40 agent products by May 2026.

---

## Which plugin do I need?

| Your job-to-be-done | Install | What's in the box |
|---|---|---|
| **Run end-to-end brand-strategy engagements across a portfolio** (agencies, in-house, consultants) | [`digital-marketing-pro`](https://github.com/indranilbanerjee/digital-marketing-pro) | 158 skills · 25 agents · 12-Part Strategy Flow · 6-platform AEO/GEO · EU AI Act Article 50 · Cowork-team-persistent · multi-brand · multi-jurisdiction compliance |
| **Produce publish-ready long-form content** (blog posts, white papers, case studies, executive briefs) | [`contentforge`](https://github.com/indranilbanerjee/contentforge) | 21 skills · 13 agents · 11 quality gates · 29-pattern AI humanizer · fact-checker · real `.docx` output · C2PA signing |
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

## What's new in v3.11.0 (June 8, 2026) — DMP v3.12.0 Cowork persistence + hardening

Coordinated release. **DMP bumped 3.11.0 → 3.12.0.** CF + SF unchanged.

Research-grounded hardening pass after web research confirmed `${CLAUDE_PLUGIN_DATA}` is NOT persistent across Anthropic Cowork sessions (GitHub issue #51398). The earlier planned path-migration would NOT have fixed the bug.

### DMP ships a new `/digital-marketing-pro:cowork-setup` skill

Routes brand state through a Google Drive MCP so profiles, plans, and reports survive across Cowork sessions. Mirrors the proven ContentForge `cf-cowork-setup` pattern. Multi-team isolation via per-team folder names. Falls back to local-only mode on Claude Code.

### Platform feature uptake

- **`fallbackModel`** ready in `settings.json.example` (Sonnet 4.7 → Sonnet 4.6 → Haiku 4.5) — uses Claude Code v2.1.152's resilience chain.
- **`requiredMinimumVersion: 2.1.157`** in plugin.json — older Claude Code builds get a clear upgrade prompt instead of silent feature gaps. From Claude Code v2.1.163.
- **`disable-model-invocation: true`** on 5 true side-effect commands — context-budget savings without breaking natural-language entry points.

### Hardening + tests

- Model-registry freshness check in `/digital-marketing-pro:doctor` (severity bands: ok / warn / urgent), surfacing the exact `refresh_models.py` invocation when stale.
- Cowork+Drive routing status in `/doctor` flags `urgent` when Cowork is detected but `cowork-setup` hasn't run.
- 3 "Read all" eager-load anti-patterns fixed in `growth-plan`, `client-validation-document`, `continuous-improvement-loop`.
- 3 more top-heaviest skills got Context efficiency callouts (`seo-plan`, `content-engine`, `analytics-insights`).
- CI line-count guard (`scripts/skill-line-check.py`) — all 158 skills under 500-line threshold.
- **49 stdlib-unittest tests** (zero third-party deps) covering `resolve_model`, `drive-sync-state`, `plugin-metadata`, `skill-line-check`, `connector_resolver`. All passing.

### Skill counts

- **DMP: 157 → 158** (+1 cowork-setup)
- CF: 21 (unchanged)
- SF: 16 (unchanged)
- **Total: 195 across the suite, all passing Codex `[a-z0-9-]+` regex**

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
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 3.8.0 | The most comprehensive open-source AI marketing plugin — 153 skills, 25 specialist agents, 12-Part Strategy Flow producing the Four Core Documents (61 explicit steps), Two-Views Model, Decision Matrix, Living Project Instruction File. Built for marketing agencies, in-house teams running 50–200 brands, and consultancies. EU AI Act Article 50 ready (C2PA content provenance signing). 6-platform AEO/GEO audit including Google AI Mode. 16 privacy-law jurisdictions. 14 HTTP MCP connectors, 77 Python scripts (optional), 167 reference knowledge files, 14 top-level slash commands. v3.7.11 closes the connector-resolver loop with a stdlib urllib HTTP executor that fires manifests against real APIs for 8 verified connectors. Test harnesses: 44/44 pass. **v3.8.0** adds real native manifests for Codex / Antigravity / Cursor / Copilot CLI. |
| **[contentforge](https://github.com/indranilbanerjee/contentforge)** | 3.13.0 | Open-source enterprise content production pipeline — 19 skills, 13 specialist agents, 11 quality gates, 29-pattern AI-detection humanizer, fact-checker subagent, three-category internal linking (topical / commercial / authority), real .docx output with embedded SEO + Quality + Production + Internal-Link appendices. EU AI Act Article 50 ready via `--c2pa-sign` on `scripts/generate-docx.py`. v3.12.10 closed three Cowork-with-Drive roadmap items (cross-session checkpoint resume, brand-profile read-back from Drive, multi-team namespace isolation). 16 opt-in HTTP MCP connectors catalogued in `.mcp.json.connectors-reference`. **v3.13.0** adds real native manifests for Codex / Antigravity / Cursor / Copilot CLI. |
| **[socialforge](https://github.com/indranilbanerjee/socialforge)** | 1.9.0 | Open-source agency-grade social media production engine — calendar parsing, asset-first compositing, AI image generation (Vertex AI Nano Banana Pro), AI video generation (WaveSpeed Kling v3.0 Pro), multi-platform copy adaptation (Instagram, TikTok, LinkedIn, Threads, X, Facebook, YouTube Shorts), human-in-the-loop review galleries, C2PA signing for EU AI Act Article 50 compliance. 16 skills, 25 commands, 5 agents, 22 scripts, 10 HTTP MCP connectors (all Cowork-compatible), 0 global hooks. Four creative modes (ANCHOR_COMPOSE / ENHANCE_EXTEND / STYLE_REFERENCED / PURE_CREATIVE). May 2026 channel pack. **v1.9.0** adds real native manifests for Codex / Antigravity / Cursor / Copilot CLI. |

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
