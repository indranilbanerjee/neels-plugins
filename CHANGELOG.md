# Changelog

All notable changes to the neels-plugins marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.1]: https://github.com/indranilbanerjee/neels-plugins/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/indranilbanerjee/neels-plugins/releases/tag/v1.0.0
