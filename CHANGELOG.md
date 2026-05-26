# Changelog

All notable changes to the neels-plugins marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.7.1] - 2026-05-27 (hotfix)

**Cowork install hazard fix in DMP + SF: bumps plugin versions to v3.8.1 / v1.9.1.**

Live Cowork-readiness testing of the v3.7.0 release (fetching marketplace.json + each plugin's `.claude-plugin/plugin.json` from GitHub raw, then sweeping for Cowork-incompatible patterns) surfaced that **DMP and SocialForge silently shipped populated `.mcp.json` files** (14 + 10 auto-connecting HTTP MCPs respectively) — meaning a fresh Cowork install would have triggered cascading OAuth prompts on plugin enable, and two of the URLs (gmail.mcp.claude.com, gcal.mcp.claude.com) were stale and returned HTTP 404 anyway.

ContentForge was unaffected — it has had the correct `{"_readme": "...", "mcpServers": {}}` empty state since v3.9.0 (May 2026).

### Plugin version bumps

- `plugins[digital-marketing-pro].version`: 3.8.0 → **3.8.1** (Cowork hotfix)
- `plugins[contentforge].version`: 3.13.0 (unchanged — was already correct)
- `plugins[socialforge].version`: 1.9.0 → **1.9.1** (Cowork hotfix)
- `metadata.version`: 3.7.0 → **3.7.1**

### Fixed

- DMP `.mcp.json` and SF `.mcp.json` now empty `{"mcpServers": {}}` with `_readme` explaining the design (same pattern as CF).
- SF gains a `.mcp.json.connectors-reference` file (was missing; SF previously only shipped `.mcp.json.example`). 10-entry catalog with corrected Gmail + Calendar URLs.
- 4 marketplace catalog files all version-bumped: `.claude-plugin/marketplace.json` + `.agents/plugins/marketplace.json` + `.cursor-plugin/marketplace.json` + `.github/plugin/marketplace.json`.

### Not changed

- v3.7.0's 5-surface native manifests across all 3 plugins unchanged.
- Zero changes to any runtime files (skills, agents, commands, scripts, hooks).
- ContentForge unchanged at v3.13.0 (was already correct).

### Verified

- Post-fix re-sweep: all 3 plugins' `.mcp.json` now empty with `_readme` (Cowork-safe install).
- Live fetch from GitHub raw (the same read path Cowork uses) parses cleanly for all 4 manifests.
- Version cross-check: marketplace v3.7.1 → DMP 3.8.1 + CF 3.13.0 + SF 1.9.1 matches each plugin's own .claude-plugin/plugin.json.

## [3.7.0] - 2026-05-27

**Real native manifests for 5 verified agent surfaces across the suite.** Coordinates the suite-wide build-out: all three plugins ship verified-real manifests for OpenAI Codex, Google Antigravity 2.0, Cursor 2.5+, and GitHub Copilot CLI in this release.

### Per-surface support (verified-real schemas)

| Surface | Manifest path per plugin | Marketplace path in this repo | Schema source |
|---|---|---|---|
| Claude Code (CLI + IDE extensions) + Anthropic Cowork | `.claude-plugin/plugin.json` | `.claude-plugin/marketplace.json` | Claude Code published format |
| OpenAI Codex (CLI + IDE + App) | `.codex-plugin/plugin.json` | `.agents/plugins/marketplace.json` | `developers.openai.com/codex/plugins/build` |
| Cursor 2.5+ | `.cursor-plugin/plugin.json` | `.cursor-plugin/marketplace.json` | `cursor.com/schemas/cursor-plugin/plugin.json` |
| GitHub Copilot CLI | `.github/plugin/plugin.json` | `.github/plugin/marketplace.json` | `docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating` |
| Google Antigravity 2.0 (CLI + IDE) | `gemini-extension.json` (repo root) | (No marketplace concept — install per-plugin via URL) | Per Google's `gemini-cli-extensions/data-agent-kit-starter-pack` reference |

### Plugin version bumps (all coordinated with this release)

- [digital-marketing-pro v3.8.0](https://github.com/indranilbanerjee/digital-marketing-pro/releases/tag/v3.8.0)
- [contentforge v3.13.0](https://github.com/indranilbanerjee/contentforge/releases/tag/v3.13.0)
- [socialforge v1.9.0](https://github.com/indranilbanerjee/socialforge/releases/tag/v1.9.0)
- `metadata.version`: 3.6.0 → **3.7.0** (minor — visible positioning shift)

### Added

- `.agents/plugins/marketplace.json` — Codex marketplace catalog with 3 plugins. Users run `codex plugin marketplace add indranilbanerjee/neels-plugins`.
- `.cursor-plugin/marketplace.json` — Cursor marketplace catalog with 3 plugins (for Team marketplace + monorepo install patterns).
- `.github/plugin/marketplace.json` — GitHub Copilot CLI marketplace catalog. Users run `copilot plugin marketplace add indranilbanerjee/neels-plugins`.

### Changed

- `.claude-plugin/marketplace.json` — metadata.description rewritten to advertise 5 verified surfaces with real install commands per platform. Each plugin's description bumped to reflect v3.8.0 / v3.13.0 / v1.9.0 state.
- `README.md` — version badge 3.6.0 → 3.7.0; added "5 agent surfaces" badge; rewritten hero line; added per-platform install command block under the plugin table; new v3.7.0 callout. Plugin table version cells bumped (DMP 3.7.13 → 3.8.0, CF 3.12.11 → 3.13.0, SF 1.8.5 → 1.9.0) with concise updated descriptions.

### Not changed

- Marketplace structure, primary install command (`/plugin marketplace add indranilbanerjee/neels-plugins`), Cowork install path (Plugins UI panel) — all unchanged.
- Zero changes to any plugin's runtime files (skills/, commands/, agents/, scripts/, hooks/, .mcp.json).
- All 3 plugins behave byte-identically in Claude Code + Cowork to their previous release.

### Pre-flight verified

- 190/190 skills across the suite (153 DMP + 21 CF + 16 SF) pass the Codex `[a-z0-9-]` regex
- SKILL.md frontmatter `name:` field matches each folder
- Descriptions ≤ 1024 chars (Codex limit)
- All 16 JSON files across the suite parse cleanly (4 marketplace + 12 plugin manifests)

## [3.6.0] - 2026-05-26

**Honest positioning across the suite: Claude Code + Cowork only. Removes the v3.3-v3.5 era claim of installing on 5 coding-agent surfaces.**

A May 2026 deep research pass (saved at `memory/antigravity-plugin-spec-may-2026.md` and `memory/codex-plugin-spec-may-2026.md`) confirmed that the OpenAI Codex / Cursor / GitHub Copilot CLI / Google Antigravity 2.0 manifests we shipped in the v3.3-v3.5 era marketplace releases (along with the v1.7/v1.8 SF + v3.11/v3.12 CF + v3.6/v3.7 DMP underlying plugin manifests) did not match the platforms' actual install specs:

- **Antigravity** uses `gemini-extension.json` at repo root — not `.antigravity/plugin.json` (the path we shipped). Google's reference repo (`gemini-cli-extensions/data-agent-kit-starter-pack`) and the `agy plugin import gemini` migrator both confirm this.
- **OpenAI Codex** uses the `.codex-plugin/plugin.json` path (that part was right), but the schema we hand-rolled was invented. The real schema is published at `developers.openai.com/codex/plugins/build`.
- **Cursor** plugin format we shipped was not a real Cursor manifest path.
- **GitHub Copilot CLI** auto-discovery of `.claude-plugin/plugin.json` was unverified.

Honest position from v3.6.0 onwards: **Claude Code (CLI + IDE extensions) + Anthropic Cowork.** Real OpenAI Codex / Cursor / GitHub Copilot CLI / Google Antigravity 2.0 support is on the roadmap with research complete — build deferred. This release is **minor (3.5.14 → 3.6.0)** because the visible positioning shift is user-facing, not a patch.

### Plugin version bumps (all coordinated honesty cleanup, zero functional change)

- `plugins[digital-marketing-pro].version`: 3.7.12 → **3.7.13**
- `plugins[contentforge].version`: 3.12.10 → **3.12.11**
- `plugins[socialforge].version`: 1.8.4 → **1.8.5**
- `metadata.version`: 3.5.14 → **3.6.0**

### Changed

- `metadata.description` — rewritten to advertise Claude Code (CLI + IDE extensions) + Anthropic Cowork only. Drops the "5 coding-agent surfaces" framing.
- Each plugin's `description` field — rewritten to drop the "Installs on 5 coding-agent surfaces" claim and the Codex / Cursor / Copilot CLI / Antigravity-specific feature claims. Current state (per-plugin honesty cleanup release content) reflected accurately.
- `README.md` — version badge bumped (3.5.14 → 3.6.0); plugin table refreshed (DMP 3.4.2 → 3.7.13, CF 3.10.0 → 3.12.11, SF 1.6.0 → 1.8.5) with current concise descriptions; new "v3.6.0: honest positioning" callout under the plugin table.

### Per-plugin cleanup releases (all ship same day)

- **digital-marketing-pro v3.7.13** — removed `.codex-plugin/`, `.cursor-plugin/`, `.antigravity/`, `docs/cross-platform-install.md`; plugin.json description + keywords + README + PR template + SECURITY + CHANGELOG updated; misleading keywords (`openai-codex`, `cursor-plugin`, `github-copilot`, `antigravity`) dropped.
- **contentforge v3.12.11** — same cleanup pattern (`.codex-plugin/`, `.cursor-plugin/`, `.antigravity/`, `docs/cross-platform-install.md` removed; same metadata + docs sweep).
- **socialforge v1.8.5** — same cleanup pattern; plus `SOCIALFORGE-COMPLETE-ENGINEERING-SPEC.md` install-surface lines fixed (Gemini image-generation references for Vertex AI Nano Banana Pro untouched — those are model references, not install claims).

### Not changed

- Zero changes to any plugin's `skills/`, `commands/`, `agents/`, `scripts/`, `hooks/hooks.json`, `.mcp.json`, `.mcp.json.connectors-reference`. All 3 plugins behave byte-identically in Claude Code + Cowork to v3.5.14.
- Marketplace structure, install command (`/plugin marketplace add indranilbanerjee/neels-plugins`), Cowork install path (Plugins UI panel), update procedure — all unchanged.
- Historical CHANGELOG entries for v3.3.0, v3.4.0, v3.5.x are intact below — they describe what was shipped at the time. v3.6.0 is the correction.

### Verified

- `marketplace.json` parses cleanly with metadata.version=3.6.0 and 3 plugins at 3.7.13 / 3.12.11 / 1.8.5.
- All 3 plugin `plugin.json` files parse cleanly.

## [3.5.14] - 2026-05-26

**ContentForge v3.12.10 — closes the three Cowork+Drive roadmap items + fixes `/plugin` scope error.**

v3.12.9 introduced Cowork+Drive routing for the final `.docx` but left three roadmap items. v3.12.10 ships all three: (1) brand profile read-back from Drive on session start (cf-style-guide Step 0); (2) cross-session checkpoint resume in Cowork (checkpoint-manager auto-marks files for Drive sync, output-manager uploads after each phase, resume command pulls from Drive first); (3) multi-team namespace isolation (cf-cowork-setup asks for Drive root folder name, different teams pick different names).

New `scripts/drive-sync-state.py` is the single source of truth for the local-side state (config, profile hash, per-run pending list). 15-test harness covers all state transitions plus checkpoint-manager integration. All pass.

Also fixed: `/plugin` slash command scope was wrongly documented as working in Cowork. Verified wrong via Indranil's live Cowork testing. `/plugin` works ONLY in Claude Code (CLI + IDE extension); in Cowork, plugin management is via the UI panel. README + MEMORY updated.

### Changed

- `plugins[contentforge].version`: 3.12.9 → 3.12.10
- `metadata.version`: 3.5.13 → 3.5.14

## [3.5.13] - 2026-05-26

**ContentForge v3.12.9 — Cowork becomes the recommended team environment, with Google Drive routing.**

User feedback during the v3.12.8 testing cycle was direct: marketing teams won't use Claude Code CLI; Cowork is the only Anthropic surface friendly enough for non-technical contributors. v3.12.8 told users to switch to local Claude Code as a workaround — which contradicts how teams actually want to work. v3.12.9 fixes this properly.

When ContentForge detects it's running in Cowork AND a Google Drive MCP is connected (Anthropic platform Settings → Integrations is the easiest path), the output-manager agent uploads the final `.docx` to `My Drive/ContentForge/<brand>/<type>/<YYYY-MM>/` instead of the ephemeral sandbox. Brand profiles also save to Drive (persist across sessions). New `/contentforge:cf-cowork-setup` skill is the one-shot wizard that verifies the environment, finds the Drive MCP, creates the canonical Drive folder layout, and stores config for future sessions.

README cross-platform section rewritten — Cowork+Drive is now the **first row, marked Recommended for teams**. Added a "How to pick" decision guide naming the three personas (marketing teams, solo developers, on-prem). The previous "Cowork = partial support, use local instead" framing is gone.

### Changed

- `plugins[contentforge].version`: 3.12.8 → 3.12.9
- `metadata.version`: 3.5.12 → 3.5.13

## [3.5.12] - 2026-05-26

**ContentForge v3.12.8 — live metadata in /contentforge:help + honest Cowork documentation.**

Two production findings from the v3.12.7 testing cycle:

1. `/contentforge:help` was showing `Version: 3.8.0` on a v3.12.7 install. Skill body had hardcoded version strings + asset counts that drifted out of sync every release. v3.12.8 introduces `scripts/plugin-metadata.py` (single source of truth, reads disk) and rewrites the help skill to call it. Nothing hardcoded anymore.

2. `.docx` files produced in Cowork landed in the Linux sandbox, not in the user's `~/Documents/ContentForge/`. The v3.12.3 dual-copy save doesn't fire in Cowork because the bash sandbox can't write to the Windows/Mac host. README falsely claimed "Full support" for Cowork. v3.12.8 honestly documents Cowork as **Partial Support** with specific limits enumerated, and ships a new `/contentforge:cf-environment` skill that surfaces a per-capability matrix at runtime.

### Changed

- `plugins[contentforge].version`: 3.12.7 → 3.12.8
- `metadata.version`: 3.5.11 → 3.5.12

## [3.5.11] - 2026-05-26

**ContentForge v3.12.7 — Drive MCP autodetect at brand-setup.**

Fixes a real bug from the v3.12.6 testing cycle: even when a user already had a Google Drive MCP configured (Anthropic platform integration, Pipedream / Composio / Zapier / Make Drive aggregator), `/contentforge:brand-setup` ignored it and walked them through the full service-account JSON setup as if no Drive existed. The two Drive code paths (service-account SDK vs MCP tool calls) had no glue.

CF v3.12.7 adds `scripts/detect-drive-mcp.py` (stdlib, probes both `.mcp.json` and the legacy credentials file) and a new **Step G.0** in `brand-setup.md` that runs the probe BEFORE the tracking-backend menu. If a Drive MCP is detected, brand-setup short-circuits to confirmation and skips the service-account flow entirely. Step E (Knowledge Vault verification) now documents two routes: MCP-tool-call route OR service-account-SDK route.

Also fixes 6 phantom slash command references in `brand-setup.md` that pointed to skills under the wrong namespace (`/contentforge:style-guide` instead of `/contentforge:cf-style-guide`, etc.) — users clicking these were getting "command not found" even though the skills existed.

### Changed

- `plugins[contentforge].version`: 3.12.6 → 3.12.7
- `metadata.version`: 3.5.10 → 3.5.11

## [3.5.10] - 2026-05-26

**DMP v3.7.12 — code hygiene pass.** Zero behavior change; refactors `connector-status.py` from 973 to 342 lines by importing `CONNECTOR_REGISTRY` and helpers from the v3.7.10 `_connector_registry.py` instead of duplicating them. Removes 4 unused imports across the suite. Adding a connector now means editing one file. All 44 DMP tests (27 resolver + 17 executor mock-HTTP-server) still pass.

### Changed

- `plugins[digital-marketing-pro].version`: 3.7.11 → 3.7.12
- `metadata.version`: 3.5.9 → 3.5.10

## [3.5.9] - 2026-05-26

**DMP v3.7.11 — Python-side HTTP executor closes the resolver loop.**

The v3.7.10 resolver returned manifests of "what would be sent." v3.7.11 ships `scripts/connector_executor.py` (stdlib `urllib.request`, no third-party deps) that actually fires those manifests against real APIs for **8 verified connectors**:

| Connector | Env var | Auth | Endpoint example |
|-----------|---------|------|---------------------|
| Slack | `SLACK_BOT_TOKEN` | `Authorization: Bearer xoxb-...` + body.ok post-check | `POST /api/chat.postMessage` |
| HubSpot | `HUBSPOT_PRIVATE_APP_TOKEN` | `Authorization: Bearer pat-...` | `GET /automation/v4/flows`, `POST /marketing/v3/campaigns` (201) |
| Klaviyo | `KLAVIYO_PRIVATE_KEY` | `Authorization: Klaviyo-API-Key ...` + revision 2026-04-15 | `GET /api/flows`, `PATCH /api/flows/{id}` (vnd.api+json) |
| SendGrid | `SENDGRID_API_KEY` | `Authorization: Bearer SG.xxx` | `POST /v3/mail/send` (202 success) |
| Brevo | `BREVO_API_KEY` | `api-key:` header (lowercase, NOT Bearer) | `POST /v3/smtp/email` |
| Customer.io | `CUSTOMERIO_APP_API_KEY` | `Authorization: Bearer` (App key only) | `POST /v1/send/email` |
| Mailchimp | `MAILCHIMP_API_KEY` | Basic auth, dc from key suffix | `GET /3.0/automations` |
| Ahrefs | `AHREFS_API_KEY` | `Authorization: Bearer` | `GET /v3/site-explorer/metrics` |

**25 OAuth-only connectors** (Google Ads, Meta, LinkedIn, TikTok, Twitter OAuth 1.0a, Gmail, Google Calendar, GSC, GA4, Salesforce, Zoho, Buffer, Hootsuite, Cision, Muckrack, etc.) return `execute_blocked_reason: "use MCP path"` with the manifest still returned — Python can't run OAuth flows from a script, so those route through Claude's MCP tools.

**Safety gates:** dry-run by default; write ops require `--execute --confirm`; missing env vars block with `setup_hint_credential`; unresolved `{VAR}` placeholders never fire; every executed call logs to `~/.claude-marketing/{brand}/executions/`.

**Test coverage:** 17 mock-HTTP-server tests in `_shared/dmp_executor_test_harness.py` (stdlib `http.server` in daemon thread — real send-and-receive, not shape inspection). Combined with v3.7.10's 27 resolver scenarios = **44/44 pass**.

New slash command: `/digital-marketing-pro:execute-action` (14 commands total). Plugin counts: 13 → 14 commands, 76 → 77 Python scripts.

### Changed

- `plugins[digital-marketing-pro].version`: 3.7.10 → 3.7.11
- `plugins[digital-marketing-pro].description` updated with the executor + 8-connector-verified matrix
- `metadata.version`: 3.5.8 → 3.5.9

## [3.5.8] - 2026-05-26

**DMP v3.7.10 — Connector-aware action resolver replaces 14 unconfigured-only action stubs.**

v3.7.5–v3.7.7 shipped 14 actions across 4 scripts (`performance-monitor`, `crm-sync`, `execution-tracker`, `seo-executor`) as honest-but-static stubs that always returned `status: stub_implementation` regardless of which connectors the user had configured. v3.7.10 introduces `scripts/connector_resolver.py` that probes live `.mcp.json` + env-var state on every call and resolves each action to one of three modes:

- **`real`** — runs end-to-end with no external API (`arm-watchdog` writes `~/.claude-marketing/{brand}/watchdogs/`)
- **`manifest_ready`** — a matching connector is configured; response includes the exact HTTP request manifest (method, URL, headers, body template, auth pattern) for the orchestrator (Claude via MCP) to execute. Write ops set `approval_required: true`.
- **`stub_unconfigured`** — no matching connector; response includes manual fallback PLUS copy-paste `.mcp.json` setup snippet, env-var list, and Cowork compatibility note.

New files in DMP: `scripts/_connector_registry.py` (33 connectors, 11 categories) + `scripts/connector_resolver.py` (ACTION_SPECS + manifest builders for 20+ APIs) + `scripts/action-doctor.py` + `commands/doctor.md` (the `/digital-marketing-pro:doctor` slash command) + `_shared/dmp_action_test_harness.py` (27 scenarios, all pass).

Cross-platform verified: no Windows-isms, ASCII output for cp1252 consoles, UTF-8 stdout reconfigure as defensive backstop, no `os.system` / `shell=True`.

### Changed

- `plugins[digital-marketing-pro].version`: 3.7.9 → 3.7.10
- `plugins[digital-marketing-pro].description` rewritten with 3-mode contract
- `metadata.version`: 3.5.7 → 3.5.8

## [3.5.7] - 2026-05-25

**Corrects an inaccuracy in the v3.5.6 README callout across the suite.**

v3.5.6 documented the `/plugin isn't available in this environment` gotcha but attributed it only to **claude.ai web chat**. User correction from Indranil after re-reviewing Shreea's screenshot: the chat was in the **Claude Desktop app** (the installed Anthropic chat client), not web. The correct rule is: `/plugin` slash commands are supported only in **Claude Code** (CLI / IDE at claude.com/code) and **Anthropic Cowork** — not in the standard Claude chat app, whether browser OR installed desktop. Both surfaces return the same error.

### Changed

- **digital-marketing-pro: 3.7.8 → 3.7.9** — README callout reworded.
- **contentforge: 3.12.5 → 3.12.6** — same.
- **socialforge: 1.8.3 → 1.8.4** — same.
- **marketplace `README.md`** — same correction, plus expanded the recovery framing so it's clear plugins ARE installed and skills DO work; only the management slash command is blocked.

## [3.5.6] - 2026-05-25

**README fix for the "claude.ai web" gotcha across the suite.** User-team report from Shreea via WhatsApp screenshot: `/plugin update contentforge@neels-plugins` in claude.ai web chat returns `"/plugin isn't available in this environment"`. The plugins ARE installed and their skills work, but `/plugin` slash commands are only supported in Claude Code CLI / Desktop / Cowork. Documented across all 4 READMEs (marketplace + 3 plugins) so the next user hitting this finds the recovery path immediately.

### Changed

- **digital-marketing-pro: 3.7.7 → 3.7.8** — README "If you see /plugin isn't available" callout in Updating section.
- **contentforge: 3.12.4 → 3.12.5** — same.
- **socialforge: 1.8.2 → 1.8.3** — same.
- **marketplace `README.md`** — same callout at the top of the Updating section, with explicit recovery paths: (1) **Plugins** UI button at bottom of web chat → **Manage plugins** → Remove + Add for re-pull, OR (2) switch to Claude Code CLI / Desktop / Cowork for management commands.

## [3.5.5] - 2026-05-25

**DMP v3.7.7 — resumable workflows + visible output folder + 4 more audit gaps fixed.**

### Changed

- **digital-marketing-pro: 3.7.6 → 3.7.7** — Direct fix for the user-team feedback that "dm pro also taking too long to process" (Shreea, v3.12.2 cycle). The headline 12-Part `/engagement` workflow now writes per-part checkpoints via the new `scripts/checkpoint-manager.py` so an interruption resumes from the next un-checkpointed part instead of losing 30+ minutes of work. Same for `campaign-plan`, `content-engine`, `seo-audit`, `competitor-analysis`, `campaign-audit`, `launch-campaign`. New `/digital-marketing-pro:resume` command. Plus dual-copy save via the new `scripts/output-publisher.py` — every artifact now lands in `~/Documents/DigitalMarketingPro/{brand}/{workflow}/{YYYY-MM}/` as well as the internal tracking copy. New `/digital-marketing-pro:output-folder` command. Mirrors the ContentForge v3.12.3 pattern. Also an audit pass that caught 4 more broken refs missed by v3.7.6 (2 missing actions + 2 broken slash refs + 2 broken file refs — all fixed; re-audit clean). Verified end-to-end with a 5-scenario simulation that runs in 5.8s.

## [3.5.4] - 2026-05-25

**DMP v3.7.6 wires the v3.7.5 skill surface to real script actions.**

### Changed

- **digital-marketing-pro: 3.7.5 → 3.7.6** — Audit pass mirroring the ContentForge v3.12.4 production-simulation fix. The 3 new skills shipped in v3.7.5 (`/validate-profile`, `/campaign-audit`, `/launch-campaign`) referenced 15 script actions that didn't exist in the underlying Python scripts and 2 missing flags on `connector-status.py`. v3.7.6 adds all of them: `inventory` / `automations` / `cadence` / `diagnostic` / `arm-watchdog` to `performance-monitor.py`, `audit-workflows` / `create-campaign` to `crm-sync.py`, `enable-automation` / `schedule-posts` / `notify-influencers` / `pr-send` / `internal-kickoff` to `execution-tracker.py`, plus `--probe-only` and `--no-secrets` flags to `connector-status.py`. Action handlers return structured `stub_implementation` contracts so the orchestrator has a clean response surface; `connector-status.py` flags are fully implemented (probe + recursive secret redaction). All 14 new invocations pass; all 71 DMP scripts still pass `--help`; `/validate-profile` end-to-end simulation passes.

## [3.5.3] - 2026-05-25

**CF v3.12.4 quality fix discovered via full production simulation.**

### Changed

- **contentforge: 3.12.3 → 3.12.4** — Fixes a heading-style quality bug found while running the full production simulation: H1/H2/H3 markdown headings rendered as plain bold text instead of using Word's `Heading 1/2/3` paragraph styles. Impact: no Navigation Pane, no auto-TOC, no PDF bookmarks, screen-reader accessibility regression. Fixed across `render_blocks()`, the 4 appendix headers, and the document title. Re-verified against 4 doc types (whitepaper, article, blog, research paper) — Title=1, H1=1, H2=10-16, H3=0-15 styles now properly applied.

## [3.5.2] - 2026-05-25

**DMP closes 3-skill audit gap; CF fixes 2 production bugs reported by beta users.**

### Changed

- **digital-marketing-pro: 3.7.4 → 3.7.5** — Built the 3 skills the v3.7.4 audit had previously mapped to existing-skill chains. `/validate-profile` (brand profile + connector health, no credential exposure), `/campaign-audit` (cross-channel current-state inventory with 4-tier triage), `/launch-campaign` (multi-channel 14-step launch orchestrator). Skill count 150 → 153.
- **contentforge: 3.12.2 → 3.12.3** — Fixes two production bugs from the beta-user feedback cycle:
  1. **Final `.docx` invisible to users.** Pipeline now writes to TWO locations: internal tracking (`~/.claude-marketing/<brand>/tracking/outputs/...`) AND user-visible (`~/Documents/ContentForge/<brand>/<type>/<YYYY-MM>/<slug>.docx`). The completion card surfaces the visible path prominently.
  2. **No way to resume an interrupted pipeline run.** New `scripts/checkpoint-manager.py` writes each phase output to disk; new `/contentforge:resume` command picks up from the last completed phase. New `/contentforge:output-folder` reveals the visible output folder in the OS file manager.
- **socialforge: 1.8.2** — unchanged (no new work this cycle).

### Quality

- Per-file content sweep: 188 SKILL.md + 43 agents + 69 reference docs clean (was 185 SKILL.md last cycle; the 3 net new are DMP's campaign-audit + validate-profile + launch-campaign).
- All 13 plugin.json + marketplace.json files valid JSON.
- DMP skill count corrected to 153 across README + docs + plugin.json description.
- CF script count 11 → 12 (added checkpoint-manager.py), command count 7 → 9 (added resume + output-folder).

## [3.5.1] - 2026-05-25

**Model curator + correctness sweep across the suite.** All three plugins bumped to add a shared model-selection infrastructure and a 13-finding correctness pass.

### Changed

- **digital-marketing-pro: 3.7.3 → 3.7.4** — model curator wired into `scripts/ai-visibility-checker.py` (replaces hardcoded deprecated `claude-sonnet-4-5-20250929` and stale `gpt-4o-mini`); 26 broken Gmail/Calendar/Drive MCP URLs replaced; 51 stale `/dm:X` slash refs rewritten to `/digital-marketing-pro:X`; DPDPA § 1.11 updated to 2025 Rules; 2 skill-name mismatches and 3 missing skill refs fixed; broken `contentauthenticity.org/community/cr-cli` URL replaced. See `digital-marketing-pro/CHANGELOG.md` for the full list.
- **contentforge: 3.12.1 → 3.12.2** — model curator added; Gmail/Calendar MCP URLs replaced; shorthand `/cf:X` slash refs canonicalised; broken `contentauthenticity.org/community/cr-cli` URL replaced. See `ContentForge/CHANGELOG.md`.
- **socialforge: 1.8.1 → 1.8.2** — model curator wired into `generate_image.py` / `edit_image.py` / `index_assets.py` / `generate_video.py` (replaces hardcoded deprecated `gemini-2.0-flash`, `gemini-2.0-flash-exp-image-generation`, and `veo-2.0-generate-001`); added `--model` / `--video-model` / `--list-models` flags everywhere; fixed broken `cloud.higgsfield.ai/api-keys` and `gmail/gcal/drive.mcp.claude.com` URLs; shorthand `/sf:X` slash refs canonicalised; fixed a pre-existing arg-order bug where `aspect_ratio` was passed as `duration` in the Kling call site. See `SocialForge/CHANGELOG.md`.
- **Top-level description** updated to mention the shared model curator (`scripts/model_registry.json` + `resolve_model.py`).

### Quality

- All 4 manifests for each plugin (`.claude-plugin`, `.codex-plugin`, `.cursor-plugin`, `.antigravity`) bumped consistently.
- Per-plugin `docs/MODEL-CURATOR.md` added documenting alias map, deprecation auto-fall-forward, and the `refresh_models.py` drift workflow.
- 102 of 103 Python scripts pass `--help` smoke test (1 timeout from pre-existing pip auto-install behaviour).
- 185 SKILL.md + 43 agents + 69 reference docs swept clean of deprecated model ids, dead URLs, shorthand slash refs, and hardcoded user paths.

## [3.5.0] - 2026-05-24

**Suite parity + community standards.** Brought ContentForge and SocialForge to digital-marketing-pro's baseline:

- All three plugins now ship `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/ISSUE_TEMPLATE/` files.
- Star History charts added to all three READMEs.
- Plugin descriptions and `plugin.json` keywords rewritten/expanded for marketplace discoverability.
- GitHub repo metadata refreshed via gh CLI (homepage → indranil.in, Discussions enabled, SEO topics added on all three repos).
- digital-marketing-pro v3.7.3, ContentForge v3.12.1, SocialForge v1.8.1.

## [3.4.x] - 2026-05-24

digital-marketing-pro 3.7.1 README rewrite for organic SEO + indranil.in branding; stale-count sweep across docs; GitHub topics refreshed.

## [3.3.0] - 2026-05-24

DMP 3.7.0 / CF 3.12.0 / SF 1.8.0 — 5-platform install matrix (Claude Code + Codex + Cursor + Copilot CLI + Antigravity experimental).

## [2.7.2] - 2026-05-03

### Changed — SocialForge Count Sync (19 cmds → 25, 18 scripts → 19)

The SocialForge entry in the marketplace catalog and the marketplace README plugin table carried stale counts that pre-dated the v1.4 era cleanup which finalized SocialForge at 25 commands and 19 scripts. The plugin itself was correctly tagged v1.5.1 and shipped with the right files; only the catalog descriptions were out of date.

This release updates:
- `.claude-plugin/marketplace.json` socialforge description: "19 commands ... 18 scripts" → "25 commands ... 19 scripts"
- `README.md` plugin table for socialforge: same correction
- `README.md` version badge: 2.7.1 → 2.7.2
- Marketplace metadata version: 2.7.1 → 2.7.2

In parallel, the SocialForge plugin's own README (`socialforge/README.md`) was updated to match: the header was still showing **Version: 1.4.0** with `4 hooks` listed in the Architecture section despite the plugin being v1.5.1 since the v1.5.0 hook removal. The cross-reference to Digital Marketing Pro in SocialForge's "Neelverse Marketing Suite" section also still claimed "141 skills" — corrected to 149. ContentForge's same cross-reference was also corrected.

No plugin version changes. Pure metadata correction across the marketplace + plugin READMEs to bring catalog text in sync with what is actually shipping.

---

## [2.7.1] - 2026-05-03

### Changed — DMP Skill-Count Sync (147 → 149)

Description correction. The DMP v3.2.0 release added 2 new skills (`/dm:check` and `/dm:status`) on top of the 147 that existed at v3.1.x, bringing the total to 149. The marketplace metadata + plugin table description in v2.7.0 referenced the pre-v3.2 count of 147 skills.

This release updates:
- `.claude-plugin/marketplace.json` digital-marketing-pro description: "147 skills" → "149 skills (141 atomic + 6 v3.0 methodology + 2 v3.2 quality-and-status)"; also surfaces "10 top commands"
- `README.md` plugin table for digital-marketing-pro: same correction
- `README.md` version badge: 2.7.0 → 2.7.1
- Marketplace metadata version: 2.7.0 → 2.7.1

No plugin version changes. Pure metadata correction. The DMP plugin itself is still at 3.2.0 (this fix happens in the marketplace catalog only).

#### Why the count drifted

DMP v3.2.0 was released as `feat(v3.2.0): close v3.1 hook-removal gaps with explicit replacements` and bumped DMP plugin version to 3.2.0 with the correct internal count. The marketplace metadata was bumped to 2.7.0 the same day but in a separate commit window where the description text was carried forward from the v3.1.1 era when DMP had 147 skills. The DMP plugin's own README already shows 149 (corrected in DMP commit `a4a546c` "docs: update stale skill/script/command counts across all v3.2 docs"). This release brings the marketplace catalog back in sync.

---

## [3.0.0] - 2026-05-12

### Fixed — ContentForge v3.9.4: real pipeline orchestration + real .docx output (CRITICAL)

Empirical pipeline run on a test brand surfaced two architectural gaps in ContentForge that made the plugin appear to work without actually doing the work. Bumped marketplace to v3.0.0 to signal this is a meaningful behavior change for ContentForge users.

- **contentforge v3.9.3 → v3.9.4** — fixes pipeline orchestration (SKILL.md now explicitly tells Claude to dispatch each phase via the `Task` tool with the phase's `subagent_type`; previously the description-only spec let Claude collapse the 11-phase pipeline into a single inference pass that skipped real research / fact-checking / humanizer 29-pattern catalog / reviewer scoring) and ships a real `scripts/generate-docx.py` (auto-installs python-docx; produces a Microsoft Word file with title page, full body, and three appendices: SEO Scorecard / Quality Scorecard / Production Details). Phase 8 output-manager now invokes the script as the canonical execution path. Verification is empirical: a successful run produces `pipeline-run.json` (proves phase tracker calls fired), the `.docx` file (proves output-manager actually ran), and `[PHASE-AUDIT]` lines for every phase.

### Updated
- Marketplace metadata version bumped to 3.0.0
- contentforge bumped to v3.9.4

---

## [2.9.0] - 2026-05-09

### Fixed — Slash Command Namespace Consistency Across All Plugins

After the v2.8.0 manifest install fix landed, an audit found that all three plugins inconsistently used short slash command shortcuts (`/cf:`, `/dm:`, `/sf:`) in some docs and runtime files. Claude Code auto-namespaces plugin commands as `/<plugin-name>:<command>` based on the plugin's `name` field, so the canonical forms are `/contentforge:`, `/digital-marketing-pro:`, and `/socialforge:`. Whether the short forms work depends on undocumented namespace strictness in Claude Code; the long forms are guaranteed to work per the documented spec.

#### Coordinated patch release

- **digital-marketing-pro v3.2.1 → v3.2.2** — swept ~600 `/dm:` references across ~50 files (README, getting-started, TESTING-GUIDE, engagement-methodology, multi-brand-guide, brand-guidelines, architecture, v3.2-opt-ins, all 6 agent files, all 149 skill SKILL.md files, command files, and CHANGELOG)
- **contentforge v3.9.2 → v3.9.3** — swept ~300 `/cf:` references across ~30 files (README, USER-GUIDE, TESTING-GUIDE, UPGRADE-GUIDE, CONNECTORS, CHANGELOG, all 13 agent files, all 19 skill SKILL.md files, all 7 command files, eval JSON files, config files)
- **socialforge v1.5.2 → v1.5.3** — swept ~200 `/sf:` references across ~30 files (README, USER-GUIDE, TESTING-GUIDE, OPERATIONS, CONNECTORS, CHANGELOG, all 5 agent files, all 15 skill SKILL.md files, all 25 command files, hooks-reference.example.json, references/troubleshooting.md)

Skill filenames preserved in all three plugins — skill names like `cf-help`, `cf-style-guide`, `cf-publish` are skill identifiers (used by the Skill tool), not slash command names. They appear in slash form as `/contentforge:cf-help` etc.

#### Why this matters at runtime

Agent files in all three plugins emit slash command recommendations during execution (e.g., ContentForge's Phase 7 reviewer agent recommends `/contentforge:audit` for low-scoring drafts; DMP's content-creator agent recommends `/digital-marketing-pro:check` after draft acceptance). Before this release, agents were emitting commands with the short prefixes that may not match Claude Code's auto-namespace. After this release, agents emit the canonical form that's guaranteed to fire correctly.

#### What users should do

For users hitting any "command not found" issue with shortcuts: `claude plugin update <plugin>@neels-plugins` to pick up the new version with consistent namespace usage.

If `/cf:`, `/dm:`, `/sf:` shortcuts work in your environment they'll continue to work; this just makes the docs match the documented Claude Code namespace pattern so users have one consistent form to copy from any doc.

### Updated
- Marketplace metadata version bumped to 2.9.0
- All 3 plugin entries bumped to their patch versions
- Marketplace metadata description notes canonical slash command syntax

---

## [2.8.0] - 2026-05-03

### Fixed — Plugin Manifest Install Format Across All Three Plugins (CRITICAL)

Users reported `claude plugins install` failing with "the manifest's `repository` field is an object when Claude Code expects a string." Diagnosis confirmed two issues introduced by the v2.5–v2.7 manifest-hardening sweep:

1. **`repository` shipped as npm-shorthand object** (`{type: "git", url: "..."}`) instead of the string URL form Claude Code's plugin schema requires.
2. **`$schema` field**: although `$schema` is a standard JSON convention for editor validation, Claude Code's plugin schema parser rejects unknown top-level keys.

Both issues affected every plugin in the marketplace — anyone trying a fresh install since v2.5.0 hit the error. Workaround in the wild was to clone, patch, and install via local marketplace; this release removes the need for that.

#### Coordinated patch release across all three plugins

- **digital-marketing-pro v3.2.0 → v3.2.1** — manifest fix
- **contentforge v3.9.1 → v3.9.2** — manifest fix
- **socialforge v1.5.1 → v1.5.2** — manifest fix
- **marketplace v2.7.2 → v2.8.0** — manifest fix in marketplace.json + version refs updated to all three patches

#### What users need to do

For users hitting the install error: `claude plugin marketplace update neels-plugins` then re-attempt install.

For existing installs: `claude plugin update <plugin>@neels-plugins` to pick up the patched manifest.

For users who applied the local-marketplace workaround: switch back to the upstream marketplace install once you confirm the fix landed.

### Updated
- Marketplace metadata version bumped to 2.8.0
- All 3 plugin entries bumped to their patch versions

---

## [2.7.0] - 2026-05-03

### Changed — Documentation Sync + DMP v3.2.0 Bump

Sweep to bring marketplace metadata + plugin home pages back in sync after the rapid v3.9.x ContentForge / v3.1.x DMP / v1.5.x SocialForge releases of the same day.

#### digital-marketing-pro v3.1.1 → v3.2.0

DMP v3.2.0 closes the gaps left by v3.1's hook-removal:
- New `/dm:check` command — explicit pre-publish gate replacing the global `PreToolUse` hook (no more drive-by checks on every Write/Edit, but still an opt-in safety net before publishing)
- New `/dm:status` command — richer on-demand brand snapshot replacing the global `SessionStart` banner
- Embedded mandatory hallucination check inside content-creator, email-specialist, social-media-manager, pr-outreach agents (in-context, not global)
- Opt-in `auto_save_insights` brand flag for ambient learning capture (off by default)
- Documented hook re-enable pattern at the user's own settings level (do NOT bring back the `PreToolUse mcp_.*` matcher — it intercepts every MCP call from every plugin)

#### Marketplace README sync

- Plugin table updated: DMP 3.1.0 → 3.2.0 with new v3.2 features summary; SocialForge 1.5.0 → 1.5.1 with manifest hardening note
- Version badge bumped to 2.7.0
- ContentForge entry already current (3.9.1)

#### ContentForge README sync (v3.9.1)

ContentForge's README was stuck at v3.8.0 in its header even after the v3.9.0 humanizer overhaul + v3.9.1 Cowork aggregators were shipped. README now correctly shows v3.9.1 with a full "What's New in v3.9.x" section.

#### SocialForge README sync (v1.5.1)

SocialForge's "Current Release" section was stuck at v1.4.0 even after v1.5.0 hook removal + v1.5.1 manifest hardening. README now correctly shows v1.5.1.

### Updated
- Marketplace metadata version bumped to 2.7.0
- digital-marketing-pro bumped to v3.2.0

---

## [2.6.0] - 2026-05-03

### Added — Cowork-Compatible Connectors Across All Three Plugins

Cross-plugin sweep applying the v2.5.0 ContentForge pattern (`.mcp.json.connectors-reference` with HTTP MCPs + aggregator paths for stdio-only services) to the other two plugins, plus manifest hardening.

#### digital-marketing-pro v3.1.0 → v3.1.1

Adds [.mcp.json.connectors-reference](https://github.com/indranilbanerjee/digital-marketing-pro/blob/main/.mcp.json.connectors-reference) — sectioned catalog of 25+ HTTP MCPs:
- First-party marketing MCPs already in active `.mcp.json`: HubSpot, Stripe, Klaviyo, Amplitude, Ahrefs, Similarweb
- Collaboration/publishing: Notion, Slack, Asana, Webflow, Canva, Figma, Gmail, Google Calendar
- **Aggregator MCPs for Cowork** — Pipedream entries for Google Analytics, Google Search Console, Google Ads, Google Sheets, Google Drive, Meta Marketing, Mailchimp, LinkedIn, Salesforce, plus generic templates covering Pipedream's 1000+ services. Composio, Zapier, Make.com as alternatives. This is the critical addition — `.mcp.json.example` ships ~60 stdio/npx MCPs that don't work in Cowork; the new catalog gives Cowork users a documented HTTP path for every category.
- Image/video: fal-ai, Replicate

#### socialforge v1.5.0 → v1.5.1

Plugin manifest hardened to parity with DMP and ContentForge: added `$schema`, `homepage`, `repository.url`, `license`, `author.url`, and a 14-tag `keywords` array. SocialForge does not need an aggregator catalog — all 10 of its connectors are HTTP and Cowork-compatible already.

### Updated
- Marketplace metadata version bumped to 2.6.0
- digital-marketing-pro bumped to v3.1.1
- socialforge bumped to v1.5.1

---

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
