# Neel's Plugin Marketplace

[![Version](https://img.shields.io/badge/version-2.5.0-blue.svg)](CHANGELOG.md)
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

---

## 📦 Available Plugins

| Plugin | Version | What it does |
|--------|---------|--------------|
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 3.1.0 | End-to-end digital marketing engagement methodology. v3.0 introduced the 12-Part Strategy Flow producing the Four Core Documents (61 explicit steps), Two-Views Model, Decision Matrix, Update-Back Rule, and Living Project Instruction File on top of 25 specialist agents, 141 atomic skills, 65 Python scripts, and 14 HTTP MCP connectors. v3.1 ships zero global hooks for clean multi-plugin coexistence. |
| **[contentforge](https://github.com/indranilbanerjee/contentforge)** | 3.9.1 | Enterprise content production pipeline with 13 agents, 19 skills, and 16 opt-in HTTP MCP connectors. v3.9 ships a 29-pattern AI-detection humanizer (adapted from Wikipedia: Signs of AI writing + blader/humanizer), a self-critique meta-pass, and optional voice calibration from a writing sample. v3.9.1 adds Cowork-compatible aggregator MCPs (Pipedream, Composio, Zapier, Make) for Google Sheets/Drive and other services. |
| **[socialforge](https://github.com/indranilbanerjee/socialforge)** | 1.5.0 | Agency-grade social media calendar automation with asset-first compositing. 19 commands, 15 skills, 5 agents, 18 scripts, 10 HTTP connectors. AI image generation via Vertex AI (Nano Banana 2/Pro), video generation via WaveSpeed (Kling v3.0 Pro). v1.5 ships zero global hooks; credential status now via `/sf:status` on demand. |

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

## 📄 License

MIT © Indranil Banerjee. See [LICENSE](LICENSE).
