# Security Policy

## What this repository ships

This is the **neels-plugins marketplace**. It ships two things:

1. **Listing manifests** for five hosts: `.claude-plugin/marketplace.json` (Claude Code, Cowork, and Copilot CLI, which also reads it), `.github/plugin/marketplace.json` (Copilot CLI), `.agents/plugins/marketplace.json` (Codex), `.cursor-plugin/marketplace.json` (Cursor) and `.grok-plugin/marketplace.json` (Grok). Each entry points at a plugin's own repository. In the Claude Code, Copilot and Codex manifests every entry is pinned to a release tag (`ref`), and in the Claude Code and Copilot manifests also to that tag's full commit (`sha`), so an install takes the released code, not whatever is on the default branch. The Cursor and Grok formats document no pin field, so those entries still name only the repository.
2. **The Hermes Agent bundle**, `hermes/digital-marketing-pro/`: Digital Marketing Pro, ContentForge and SocialForge folded into one Hermes listing. It holds **plugin code**: copies of each plugin's skills, agents and Python scripts, taken with `git archive` at the release commit recorded in `BUNDLE-MANIFEST.json`, with a sha256 for every file. `scripts/build_hermes_bundle.py --check` and `tests/test_hermes_bundle.py` fail if any file differs from that record.

The plugins themselves live in their own repositories. CutForge is listed here but has its own policy.

## Supported versions

The latest marketplace release is the supported one; please update before reporting.

| Marketplace | Supported |
|-------------|-----------|
| 3.60.x | ✅ |
| 3.59.x | ⚠️ Security fixes only when trivially backportable |
| < 3.59 | ❌ Please upgrade |

The plugin versions each release lists are in `.claude-plugin/marketplace.json` and the CHANGELOG.

## Where to report

- **A listing problem** (a manifest pointing at the wrong repository, tag or commit, a tampered entry, a Hermes bundle file that does not match its manifest): [this repository's private advisory form](https://github.com/indranilbanerjee/neels-plugins/security/advisories/new).
- **A problem in plugin code**, including code you found in the Hermes bundle: the plugin's own form, so the fix lands at the source and the bundle is rebuilt from it:
  - [Digital Marketing Pro](https://github.com/indranilbanerjee/digital-marketing-pro/security/advisories/new)
  - [ContentForge](https://github.com/indranilbanerjee/contentforge/security/advisories/new)
  - [SocialForge](https://github.com/indranilbanerjee/socialforge/security/advisories/new)
  - [CutForge](https://github.com/indranilbanerjee/cutforge/security/advisories/new)

**Do NOT open a public GitHub Issue for a vulnerability.** If you cannot use a private advisory, contact the maintainer via the email listed on [indranil.in](https://indranil.in) with the subject line `[neels-plugins security]`.

### What to include

- A clear description of the vulnerability and its impact
- Steps to reproduce (example commands, payloads or files)
- The marketplace version, the plugin and its version, and the host (Claude Code, Cowork, Codex, Cursor, Copilot CLI, Grok, Hermes)
- A suggested fix, if you have one
- Whether you'd like credit in the advisory, and how you'd like to be named

### What you can expect

- **Acknowledgement within 48 hours**
- **Initial assessment within 7 days**, with a severity and a tentative timeline
- **Coordinated disclosure**: a disclosure date agreed with you that gives users time to update
- **Credit in the published advisory** unless you prefer to stay anonymous
- **No bug bounty**: this is open source maintained by one person. Responsible disclosure is much appreciated.

## Scope

In scope:
- The five listing manifests: wrong or unpinned sources, entries that disagree across hosts
- The Hermes bundle: its adapter (`__init__.py`, `plugin.yaml`), `BUNDLE-MANIFEST.json`, and every copied file, scripts included
- `scripts/build_hermes_bundle.py` and the release workflow

Out of scope (report them where they belong):
- Bugs in a plugin's own repository: use that plugin's advisory form above
- Claude Code, Cowork, Codex, Cursor, Copilot CLI, Grok or Hermes themselves: report to their vendors
- Third-party MCP servers and gateways: report to their operators (see below)
- Upstream Python or npm dependencies: report to those projects, and tell us so we can upgrade
- Reports from automated scanners without proof of exploitability

## Where the plugins keep data and keys

| Plugin | Brand and run data | Deliverables | Keys |
|--------|--------------------|--------------|------|
| Digital Marketing Pro | `~/.claude-marketing/brands/{slug}/` (or `CLAUDE_MARKETING_HOME`, or the host's plugin data folder) | `~/Documents/DigitalMarketingPro/` | Environment variables only; `credential-manager.py` stores variable names, never values |
| ContentForge | `~/.claude-marketing/{brand-slug}/`, runs in `{brand-slug}/runs/{run_id}/` (or the host's plugin data folder) | `~/Documents/ContentForge/` (or `CONTENTFORGE_PUBLISH_DIR`) | Environment variables (Airtable, image providers); a Google service-account JSON for Drive and Sheets tracking, read from the path you give or `~/.claude-marketing/google-credentials.json` |
| SocialForge | `${CLAUDE_PLUGIN_DATA}/socialforge/brands/{slug}/`, fallback `~/socialforge-workspace/brands/{slug}/` | the brand's month folder | `credentials.json` in the same data folder records environment variable **names**; a key you type or pipe in goes to the OS keychain when `keyring` is installed, otherwise to that file in plain text with a warning. Since 1.31.0 the Vertex AI service-account file is used where you keep it, not copied. On Windows the file is limited to your account with `icacls`; `chmod 600` does nothing there |

Treat all of these folders as client data: they hold strategy documents, brand assets and contact lists.

## Connectors

No plugin connects anything on install: no `.mcp.json` ships, and every connector is opt-in. Not every catalogued connector is the platform's own endpoint. Digital Marketing Pro's `.mcp.json.connectors-reference` says who runs each one (`_operator`):

- **The platform's own server** (HubSpot, Slack, Notion, Stripe, Klaviyo, Meta Ads, Amazon Ads and the rest)
- **Third-party gateways** (Pipedream, Composio, Zapier, Make.com): the gateway holds the tokens for every platform you connect through it
- **Third-party services** (Synter Media AI, Ryze AI): another company, not the ad platform, receives your ad-account access, write access included
- **Community code you host yourself** (`northbeam-mcp-selfhosted`): not affiliated with the vendor; audit it before you run it

Writes to ad and CRM accounts go through each skill's typed `yes`, and on Claude Code through the host's permission prompt.

## Hardening recommendations for operators

1. **Never commit `.mcp.json` with real keys.** Use environment variables or a secret manager; `.mcp.json.example` is the safe template.
2. **Install from a release, not from a branch.** The marketplace entries are pinned; if you add a plugin repository directly, pin it to a tag or commit yourself.
3. **Read the permission prompt before a live write.** Digital Marketing Pro's skills pre-approve no live-write step, and on Claude Code its one hook makes the host ask before each prepare, approve and fire command. Bypass-permissions mode removes that check.
4. **Treat fetched and client-supplied text as untrusted.** Every agent and skill says so; a page or file that tells the assistant what to run is an attack, not an instruction.
5. **Review SKILL.md changes like code.** Skills run with whatever permissions your host grants. Treat an edit to a skill as you would a code change in production.

## Coordinated disclosure timeline

For valid reports:
- **Day 0**: report received, acknowledged within 48 hours
- **Day 7**: initial severity assessment shared with the reporter
- **Day 7–30**: fix developed, tested and released in the plugin; the marketplace pins the new release
- **Day 30–45**: coordinated disclosure window, so users can update
- **Day 45**: public advisory with full details and credit

We may move faster for actively exploited issues. We will not move slower without the reporter's agreement.
