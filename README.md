# Neel's Plugin Marketplace

> **You run marketing for a single brand, an agency portfolio, or a content team — and you want the same depth across every brand, every article, every campaign, with no per-platform lock-in. You don't want to learn six different "AI marketing" SaaS UIs that all charge per-seat per-month.**

Install three open-source plugins from one marketplace. Same skills, same agents, same outputs across **Claude Code**, **Anthropic Cowork**, **OpenAI Codex**, **Cursor 2.5+**, **GitHub Copilot CLI**, **Google Antigravity 2.0**, **Hermes Agent**, **OpenClaw**, and **Grok** (xAI Build CLI) + 35+ additional Agent Skills platforms — via the Agent Skills open standard. Zero global hooks, zero auto-connecting MCP servers, MIT-licensed, no telemetry, no seats.

[![Version](https://img.shields.io/badge/version-3.55.1-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-3-orange.svg)](#-available-plugins)
[![Total skills](https://img.shields.io/badge/skills-207%20across%20suite-blueviolet.svg)](#which-plugin-do-i-need)
[![Total tests](https://img.shields.io/badge/tests-1891%20across%20suite-brightgreen.svg)](#whats-new)
[![Surfaces](https://img.shields.io/badge/all%203%20plugins-9%20native%20%2B%2035%20Agent%20Skills-success.svg)](#-platform-compatibility)
[![Cowork](https://img.shields.io/badge/Cowork-team%20persistent-brightgreen.svg)](#-platform-compatibility)
[![Sponsor](https://img.shields.io/badge/sponsor-%E2%9D%A4-ea4aaa?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/indranilbanerjee)

> 🆕 **October 10, 2026 — marketplace v3.55.1: previews that show the image, and docs that tell the truth** (ContentForge **4.5.1** · Digital Marketing Pro **3.35.1** · SocialForge **1.29.1**). Rendering a real SocialForge preview for its README found that every platform preview had shown a broken-image icon while reporting success; SocialForge 1.29.1 embeds the image and checks it was drawn, keeps line breaks, and counts inline hashtags against the platform limit (an X post had been reported within 280 and published at 282). A documentation truth pass across all three plugins corrected every stale claim it found, and the doc-count guards now check the phrasings that had rotted. New diagrams, a real preview, "Try this first" and "What it will never do" sections, and a tip for 200k context windows. **1,891 tests passing.**
>
> Previously — **October 10, 2026 — marketplace v3.55.0: safer by default, after a Hermes security review** (ContentForge **4.5.0** · Digital Marketing Pro **3.35.1** · SocialForge **1.29.0**). A maintainer review of our Hermes Agent catalog listings asked for changes in all three plugins, and every point is fixed with a test that fails if the fix is undone. **No script installs a package on its own any more:** a missing package prints the exact pinned install command instead. **Names from outside can no longer choose a file path:** every brand, month, run and client name passes one containment check, including a ContentForge migration step that could have written a downloaded file anywhere on disk. **Digital Marketing Pro's live writes need a single-use approval record for that exact request**, created when you type yes; autopilot proposes instead of acting unless you set a standing rule, and the docs say plainly what the record can and cannot prove. **SocialForge quotes paid generation and waits for "go"**, and API keys stay out of the chat. C2PA signing is pinned to the current c2pa-python, which had been refusing the manifests the plugins built. **1,871 tests passing.**
>
> Previously — **October 10, 2026 — marketplace v3.54.0: skill lists that fit Claude Code's listing budget** (ContentForge **4.4.1** · Digital Marketing Pro **3.34.0** · SocialForge **1.28.1**). Claude Code shows the model every skill's name and description in one listing, capped at 1% of the context window and shared by every installed plugin; whatever does not fit is dropped. ContentForge's listing went from 15,061 to 3,824 characters, SocialForge's from 10,525 to 4,927 and Digital Marketing Pro's from about 126,600 to 25,974, with every description rewritten to one short line (the first 4.4.0 and 1.28.0 figures left each plugin's workflow out; 4.4.1 and 1.28.1 count it). Together the three need 34,725 characters, which fits a 1M window's 40,000; on a 200k window only the names fit, so set `skillListingBudgetFraction: 0.05` in `settings.json` to see descriptions. Seven side-effect skills are now directly model-invocable behind a typed "yes"; before, five were reachable only through a wrapper command and two (switch-backend, add-integration) not at all. Measured with trigger evals before and after: routing held for ContentForge and SocialForge, and Digital Marketing Pro's first-move accuracy rose from 80.5% to 90.5% of runs. **1,716 tests passing.**
>
> Older releases: [CHANGELOG.md](CHANGELOG.md)

A custom plugin marketplace by [Indranil Banerjee](https://indranil.in) · [LinkedIn](https://www.linkedin.com/in/askneelnow/) · [X](https://x.com/askneelnow). Agent Skills was donated to the Agentic AI Foundation December 2025; adopted by **41+ agent products** by June 2026.

---

## Which plugin do I need?

![Which plugin do I need: Digital Marketing Pro plans the strategy and runs campaigns, ContentForge writes publish-ready long-form, SocialForge produces a month of social; you hand a brief to ContentForge and a content calendar to SocialForge, and each plugin runs on its own](docs/assets/which-plugin.svg)

| Your job-to-be-done | Install | What's in the box |
|---|---|---|
| **Run end-to-end brand-strategy engagements across a portfolio** (agencies, in-house, consultants) | [`digital-marketing-pro`](https://github.com/indranilbanerjee/digital-marketing-pro) | 164 skills · 24 agents · 12-Part Strategy Flow · 6-platform AEO/GEO · agent-readiness audit · EU AI Act Article 50 · Cowork-team-persistent · multi-brand · multi-jurisdiction compliance |
| **Produce publish-ready long-form content** (blog posts, white papers, case studies, executive briefs) | [`contentforge`](https://github.com/indranilbanerjee/contentforge) | 22 skills · 13 agents · 10 quality gates · 43-pattern AI humanizer · fact-checker · run auditor · lifecycle loop (audit→refresh→measure→plan) · real `.docx` output · C2PA signing |
| **Produce social media assets at agency scale** (carousels, single-image posts, AI image / video creatives) | [`socialforge`](https://github.com/indranilbanerjee/socialforge) | 21 skills · 5 agents · 18 commands · research-month · asset-first compositing · AI image + video via your connected providers · delivery audit · C2PA signing |

**The three plugins are complementary, not overlapping.** A typical agency workflow uses all three: DMP for strategy + campaign planning, ContentForge for the long-form articles a campaign produces, SocialForge for the social assets a campaign produces. Each plugin is self-contained and keeps its own brand setup, so set the brand up once in each plugin you use.

### What these plugins will never do

- **Install software on their own.** A missing package prints the exact pinned install command for you to run.
- **Send, publish or spend without your say-so.** Live writes wait for your typed `yes` (Digital Marketing Pro also requires a single-use approval record for that exact request), and SocialForge shows a live quote before any paid image or video generation and waits for "go".
- **Ask for an API key in the chat.** Keys come from environment variables.
- **Connect to anything you did not set up.** No MCP server ships enabled and no hooks run.
- **Remove or hide AI watermarks.** AI involvement is disclosed, with C2PA provenance where the format supports it.
- **Depend on each other.** Each plugin is self-contained and useful alone.

---

## Who this suite is for

| If you're a... | Why this matters |
|---|---|
| 🏢 **Marketing agency** (50–200 brands) | One toolchain across every client, audit-trail compliance, an SOP library your new hires can follow, Cowork team persistence so your senior strategists work in browser-based Cowork while your team Drive has every artifact. |
| 👔 **In-house marketing team** | Single canonical strategy document underwriting every campaign + content piece. No more "the deck and the blog post say different things." |
| 🚀 **Marketing automation builder** (n8n / Zapier / Make / Pipedream) | DMP's connector-resolver + executor pattern. 8 verified HTTP connectors execute end-to-end; 28 more (OAuth-only connectors and the official ad-platform MCP servers) return manifest-ready specs for the MCP path. |
| 💼 **Solo consultant** / freelance marketer | One engagement produces the full document set (Four Core Documents, Growth Plan, channel strategies) as files you own and can bill against. Installs on Codex / Cursor / Copilot CLI / Antigravity for terminal-native or IDE-native workflows. |
| 📈 **Growth team** / product marketer | Funnel architecture, attribution, MMM, incrementality testing, retention, churn — all anchored to the strategy document. |
| 🛡 **Compliance-led marketer** (EU · UK · India · Brazil · California) | EU AI Act Article 50, C2PA content provenance, deepfake disclosure, GDPR + CCPA + DPDPA + LGPD + 12 more jurisdictions baked into every output. |

---

## What's new

### v3.55.1 (October 10, 2026) — previews that show the image, and docs that tell the truth

CF **4.5.1** · DMP **3.35.1** · SF **1.29.1** · suite **1,891 tests**. **SocialForge 1.29.1:** every platform preview had shown a broken-image icon while `render_preview.py` reported success (the page is `about:blank`, which cannot load `file://` images); the image is now embedded and the page checked for it, line breaks are kept, and `adapt_copy.py` reserves room for inline hashtags and returns `post_text`, exactly what to publish. The standalone copy-adapter skill carries the same fix. **Documentation truth pass, all three plugins:** guides that said packages install themselves, keys are pasted into setup, the plugins share one brand folder, or `.mcp.json` ships empty were corrected; an operations guide described a provider fallback chain and a price table the code no longer has; one Python minimum (3.10, from the pinned packages' own requirements) everywhere; counts re-derived, and the doc-count guards widened to the phrasings that had rotted, each with a planted wrong number. ContentForge 4.5.1's setup check now enforces that same Python 3.10. New theme-safe diagrams (how a live write is approved, the 12-part engagement, a SocialForge month, which plugin to use), a real SocialForge preview, "Try this first" and "What it will never do" sections, and a tip for 200k context windows.

### v3.55.0 (October 10, 2026) — safer by default, after a Hermes security review

CF **4.5.0** · DMP **3.35.1** · SF **1.29.0** · suite **1,871 tests**. A maintainer review of the Hermes Agent catalog listings (NousResearch/hermes-agent #132571-132573) asked for changes; every point is fixed in all three plugins, each with a test that was run against the old code and failed there. Installs: no script installs a package on its own; it prints the exact pinned command, and SocialForge's setup asks first. Paths: one containment check per plugin for every outside name that reaches a file path, enforced at the command line on every `--brand`, `--month`, `--run-id` and `--client` argument and guarded by a test that parses every script. Approvals (DMP): a live write fires only against an approved, unexpired, single-use record bound to the exact request; the record proves the approval step ran, not who typed yes; MCP-server writes are outside this check, and the docs say to keep the write command out of the host's allowlist. Quotes (SF): compose-creative, generate-video and batch full-pipeline show a live quote and wait for "go". Keys (SF): set as environment variables, never pasted into chat. C2PA: pinned to c2pa-python 0.38.0, which refused every manifest the plugins built until the created action carried a digital-source type. PRIVACY.md in each plugin lists the requests it was missing. Hermes's own validator passes all three.

### v3.54.0 (October 10, 2026) — skill lists that fit the listing budget

CF **4.4.1** · DMP **3.34.0** · SF **1.28.1** · suite **1,716 tests**. Claude Code's skill listing is measured in characters (context window × 4 × 1%) and shared by every installed plugin, so long descriptions were being dropped from the model's view. ContentForge's model-visible listing fell from 15,061 to 3,824 characters and SocialForge's from 10,525 to 4,927. The first release of each (CF 4.4.0, SF 1.28.0) published 14,846 → 3,646 and 10,305 → 4,745, which left each plugin's one workflow out of the count; the patch releases CF 4.4.1 and SF 1.28.1 rewrite those workflow descriptions to the rule and make the guards read workflows. Seven side-effect skills had been hidden from the model: five were reachable only through a wrapper command and two (switch-backend, add-integration) not at all. They are visible again, each behind an Execution gate (a scope or preview, then a typed `yes`; anything else cancels), and a guard in each plugin keeps it that way. Trigger evals (a case per skill, near-miss pairs, stay-quiet cases) ran before and after with the listing budget pinned. Digital Marketing Pro 3.34.0 does the same for its 170 descriptions (about 126,600 -> 25,974 characters), and its trigger evals moved from 80.5% to 90.5% of runs picking the right skill first. Together the three plugins need 34,725 characters, which fits a 1M window's 40,000; on a 200k window only the names fit, so set `skillListingBudgetFraction: 0.05` in `settings.json` to see descriptions. Two cases that got worse in its first run (a workflow description taking competitor questions, and a claim check that went looking for an evidence file) were fixed before release, each fix counts only if a differently worded request also passes, and the misses that remain are reported as is.

### v3.53.2 (October 4, 2026) — the opportunity build

CF **4.3.1** · DMP **3.33.3** · SF **1.27.2** · suite **1,662 tests**. Hermes Agent's install-time security scan had rated all three plugins "dangerous" (so `hermes plugins install` refused them) on harmless lines written like attacks, plus two real defects in SocialForge; fixed, guarded in each plugin, and checked here by running Hermes's own validator (`tests/test_hermes_admission.py`). DMP: agent-readiness audit, AI-visibility measurement map, official ad MCP servers (Google's read-only server is never chosen for a write), ChatGPT and AI Mode ads, Meridian 2.x, 13 duplicate commands folded, a competitor scraper that now identifies itself and follows RFC 9309. CF: the Quality Contract, a run auditor that resolves the approve line per industry and refuses a stale audit, a scorecard page, CC BY-SA notice for the humanizer catalog. SF: research-month, an opt-in Postiz hand-off, a last frame that really reaches the video model, sourced platform limits, X's weighted count, no silent drops. All three: listing fields, PRIVACY.md with network endpoints, evals, workflows, always-on recipes. Three standalone hero skills published, with a parity guard here that runs each hero's suite against its plugin.

Older releases are in [CHANGELOG.md](CHANGELOG.md).

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

> **On a 200k context window?** Claude Code lists every installed skill in a budget of 1% of the context window. With all three plugins installed, a 200k window has room for skill names only, so Claude can't see what each skill does. Add `"skillListingBudgetFraction": 0.05` to your Claude Code `settings.json` to fix that. On a 1M window the full list already fits.

### 4. Stay current — turn auto-update on (recommended)

**Third-party marketplaces have auto-update OFF by default in Claude Code.** When we ship a new ContentForge / DM Pro / SocialForge release, you will not be notified — you will keep running whatever version you installed first.

To get future updates automatically: open `/plugin`, go to the **Marketplaces** tab, find `neels-plugins`, and toggle **Enable auto-update**. After an auto-update fires you will be prompted to run `/reload-plugins` to pick up changes mid-session (no full Claude Code restart needed; conversation context preserved).

To update manually instead, see the [Updating](#updating) section below.

---

## 📦 Available Plugins

| Plugin | Version | What it does |
|--------|---------|--------------|
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 3.35.1 | End-to-end engagement methodology for agencies and in-house teams — 164 skills, 24 specialist agents, the 12-Part Strategy Flow producing the Four Core Documents, a content-engine run auditor that re-derives every "ready" claim, provenance-stamped benchmarks, 6-platform AEO/GEO audit, 16 privacy-law jurisdictions, EU AI Act Article 50 disclosure + C2PA signing, an agent-readiness audit for AI crawlers and agentic commerce. 94 stdlib Python scripts; connectors opt-in. |
| **[contentforge](https://github.com/indranilbanerjee/contentforge)** | 4.5.1 | Content lifecycle system — 22 skills, 13 specialist agents, a 10-phase pipeline with 10 quality gates, 43-pattern AI-detection humanizer, fact-checker subagent, run auditor, three-category internal linking, real `.docx` output with C2PA signing, and a measure-audit-plan loop that compounds per brand, under a published Quality Contract. README in 12 languages; five hero skills as claude.ai `.skill` uploads. |
| **[socialforge](https://github.com/indranilbanerjee/socialforge)** | 1.29.1 | Social creative engine — 21 skills, 18 commands, 5 agents: research and calendar in, on-brand creative out. Asset-first compositing (brand photos stay pixel-faithful), AI image + video through provider chains where nothing fails silently, 9-platform copy adaptation, human approval gates, delivery audit, C2PA signing. Prices and models looked up live, never stored. |

All three install natively on **9 platforms** — Claude Code, Cowork, Codex, Cursor, Copilot CLI, Antigravity, Hermes Agent, OpenClaw, Grok — plus 35+ Agent Skills clients. Live counts and test totals: see each repo's README.

### Standalone skills

Three single-purpose Agent Skills, each extracted from a suite plugin and tested for parity with it. They need no plugin and install on any Agent Skills client:

| Skill | From | Install |
|---|---|---|
| [contentforge-humanizer](https://github.com/indranilbanerjee/contentforge-humanizer) — edit your own draft so it reads naturally, with an offline scan of 43 AI-drafting habits | ContentForge | `npx skills add indranilbanerjee/contentforge-humanizer` |
| [digital-marketing-pro-agent-readiness](https://github.com/indranilbanerjee/digital-marketing-pro-agent-readiness) — can AI agents and AI crawlers use your site? | Digital Marketing Pro | `npx skills add indranilbanerjee/digital-marketing-pro-agent-readiness` |
| [socialforge-copy-adapter](https://github.com/indranilbanerjee/socialforge-copy-adapter) — one post, nine platforms, measured against sourced limits | SocialForge | `npx skills add indranilbanerjee/socialforge-copy-adapter` |

### Per-platform install commands

```bash
# Claude Code (CLI + IDE extensions)
/plugin marketplace add indranilbanerjee/neels-plugins
/plugin install <plugin-name>@neels-plugins

# Anthropic Cowork — UI only (no /plugin slash commands)
# Plugins panel → Add marketplace → paste indranilbanerjee/neels-plugins → Install

# OpenAI Codex (CLI + IDE + App)
codex plugin marketplace add indranilbanerjee/neels-plugins
codex plugin add <plugin-name>@neels-plugins

# Cursor 2.5+ (in any Agent chat — no marketplace add needed)
/add-plugin digital-marketing-pro@https://github.com/indranilbanerjee/digital-marketing-pro
/add-plugin contentforge@https://github.com/indranilbanerjee/contentforge
/add-plugin socialforge@https://github.com/indranilbanerjee/socialforge

# GitHub Copilot CLI
copilot plugin marketplace add indranilbanerjee/neels-plugins
copilot plugin install <plugin-name>@neels-plugins

# Grok (xAI Build CLI)
grok plugin marketplace add indranilbanerjee/neels-plugins
grok plugin install <plugin-name>

# Google Antigravity 2.0
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
- No `.mcp.json` ships (it is gitignored), so no MCP server connects when you install. Plugin-bundled MCP servers auto-connect on plugin enable, which means shipping N servers triggers N connection attempts (and likely auth prompts) for users who only want some of them. Each plugin ships its full connector catalog as a `.mcp.json.connectors-reference` file with per-entry auth notes; users opt in via the plugin's connect skill.

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

## Star history

[![Star History Chart](https://api.star-history.com/svg?repos=indranilbanerjee/neels-plugins&type=Date)](https://star-history.com/#indranilbanerjee/neels-plugins&Date)

---

## Sponsor this project

This plugin is MIT-licensed, free to use commercially, and collects no telemetry. What
sponsorship pays for is the unglamorous half of keeping it accurate: platform-API updates
when a vendor ships a breaking version, model-registry refreshes when a model is retired,
compliance passes when regulatory guidance moves, and issue triage.

If it saves your team time, you can [sponsor the work](https://github.com/sponsors/indranilbanerjee).
Sponsors from $25/mo are listed in [SPONSORS.md](SPONSORS.md).

[![Sponsor](https://img.shields.io/badge/sponsor%20on%20GitHub-%E2%9D%A4-ea4aaa?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/indranilbanerjee)

---

## 📄 License

MIT © Indranil Banerjee. See [LICENSE](LICENSE).
