# Contributing to the Neelverse plugin marketplace

This repository is the **marketplace manifest** for three plugins. It contains listing
metadata, not plugin code. Knowing which repo a change belongs in saves everyone a round trip.

## Where does my change go?

| You want to change | Repo |
|---|---|
| A skill, agent, command, script, or plugin doc | The plugin's own repo — [ContentForge](https://github.com/indranilbanerjee/contentforge), [Digital Marketing Pro](https://github.com/indranilbanerjee/digital-marketing-pro), [SocialForge](https://github.com/indranilbanerjee/socialforge) |
| A plugin's version, description, or keywords **as shown at install time** | Here — the four `marketplace.json` files |
| The suite overview, install instructions, or platform matrix | Here — `README.md` |

A bug in what a plugin *does* is never fixed here. Listing metadata is the only thing this
repo controls.

## The four manifests must stay in sync

Each platform reads a different file, and all four describe the same three plugins:

| File | Read by |
|---|---|
| `.claude-plugin/marketplace.json` | Claude Code, Anthropic Cowork |
| `.cursor-plugin/marketplace.json` | Cursor 2.5+ |
| `.agents/plugins/marketplace.json` | OpenAI Codex |
| `.github/plugin/marketplace.json` | GitHub Copilot CLI |

**Every plugin version must be identical across all four.** A bump in one is a bump in all
four. The `.agents/` variant intentionally carries no top-level marketplace version — only
per-plugin versions — so do not add one.

Two hard rules apply to every manifest here and in the plugin repos:

- `repository` must be a **string URL**, never a `{type, url}` object
- no top-level `$schema` key

## Descriptions are read at install time

The `description` field is what someone sees in the plugin browser before they install. It is
the most-read text this repo owns, and it has gone stale before — a ContentForge listing
advertised "21 skills, 35-pattern AI humanizer" for two releases after the plugin shipped 22
skills and a 41-pattern catalog.

If you change a count in a description, verify it against the plugin repo rather than another
description:

```bash
ls -d skills/*/ | wc -l      # skills
ls agents/*.md | wc -l       # agents
ls commands/*.md | wc -l     # commands
```

## Before opening a PR

```bash
# every manifest parses
python -c "import json,glob; [json.load(open(f,encoding='utf-8')) for f in
  ['.agents/plugins/marketplace.json','.claude-plugin/marketplace.json',
   '.cursor-plugin/marketplace.json','.github/plugin/marketplace.json']]; print('ok')"

# Claude Code accepts the marketplace manifest
claude plugin validate .
```

Then check that all four files agree on every plugin version.

## Proposing a new plugin for the suite

Open an issue first rather than a PR. The suite is deliberately small and each plugin is
fully standalone — no plugin may depend on a sibling. A listing is added once the plugin has
its own repo, its own test suite, and manifests for the surfaces it claims to support.

## Conduct and security

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). For vulnerabilities,
follow [SECURITY.md](SECURITY.md) — please do not open public issues for them.
