# Neel's Plugin Marketplace

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-3-orange.svg)](#-available-plugins)
[![Cowork](https://img.shields.io/badge/Cowork-compatible-brightgreen.svg)](#-platform-compatibility)

A custom plugin marketplace for **Claude Code** and **Anthropic Cowork** — built and maintained by [Indranil Banerjee](https://www.linkedin.com/in/askneelnow/).

All three plugins ship with zero global hooks and zero auto-connecting MCP servers as of May 2026, so they coexist cleanly with other plugins and don't pollute unrelated Claude Code work. All HTTP MCP connectors are Cowork-compatible.

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
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 3.3.0 | End-to-end digital marketing engagement methodology. **v3.3.0** modernizes for May 2026: privacy/compliance updates (EU AI Act Article 50 enforcement Aug 2026, DPDP Phase II Nov 2026, NY synthetic-performer law June 2026, FTC May 2026 endorsement guidance, CCPA ADMT, CJEU pseudonymization ruling), channel mechanics (LinkedIn March 2026 algo + Depth Score, email DMARC + RFC 8058 + open-rate decline, TikTok USDS + AI creator labeling, WhatsApp per-message pricing, schema refresh with LLMs.txt, Sora deprecation note), AEO/GEO (Google AI Overviews + zero-click reality, Profound/Otterly/Conductor measurement). README restructured Quick Start-first. 12-Part Strategy Flow producing the Four Core Documents (61 explicit steps), Two-Views Model, Decision Matrix, Living Project Instruction File. 25 specialist agents, 149 skills, 70 Python scripts, 10 commands, 14 HTTP MCP connectors. |
| **[contentforge](https://github.com/indranilbanerjee/contentforge)** | 3.9.5 | Enterprise content production pipeline with 13 agents, 19 skills, 16 opt-in HTTP MCP connectors. **v3.9.5** splits Phase 6 internal linking into three categories — topical (informational), commercial (brand product/service), conversion (audience-matched CTA) — with new `brand_pages` schema, color-coded inline Word hyperlinks, and Appendix D internal link map. v3.9.4 fixed pipeline orchestration to actually invoke subagents via Task tool and added `generate-docx.py` for real Word output. v3.9 ships a 29-pattern AI-detection humanizer with self-critique meta-pass and optional voice calibration. |
| **[socialforge](https://github.com/indranilbanerjee/socialforge)** | 1.5.3 | Agency-grade social media calendar automation with asset-first compositing. 25 commands, 15 skills, 5 agents, 19 scripts, 10 HTTP connectors (all Cowork-compatible). AI image generation via Vertex AI (Nano Banana 2/Pro), video generation via WaveSpeed (Kling v3.0 Pro). v1.5 ships zero global hooks; credential status via `/socialforge:status` on demand. v1.5.1 hardened the plugin manifest. v1.5.2 fixed manifest install format. v1.5.3 swept `/sf:` to `/socialforge:` for namespace consistency. |

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
