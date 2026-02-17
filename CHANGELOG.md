# Changelog

All notable changes to the neels-plugins marketplace will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-02-17

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
