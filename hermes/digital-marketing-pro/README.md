# Digital Marketing Pro for Hermes Agent: three toolkits, one listing

This is the folder Hermes installs from the [neels-plugins marketplace](https://github.com/indranilbanerjee/neels-plugins) as
`digital-marketing-pro` (version 3.56.0). Hermes allows one plugin per vendor, so the Hermes
listing holds three of our marketing plugins as skill groups. **207 skills in all.** It is
generated, never hand-edited: `scripts/build_hermes_bundle.py` in the marketplace repo copies each
plugin's runtime files from its release commit and records the commit and a sha256 per file in
`BUNDLE-MANIFEST.json`.

| Folder | Plugin | Version | Commit | Skills | What it covers |
|---|---|---|---|---|---|
| `strategy/` | [digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro) | 3.35.2 | `6d7365d7a71a` | 164 | marketing strategy, SEO/AEO/GEO, paid media, CRM and analytics |
| `content/` | [contentforge](https://github.com/indranilbanerjee/contentforge) | 4.5.2 | `9d82163294bf` | 22 | long-form content: research, fact-check, draft, humanize, audit |
| `social/` | [socialforge](https://github.com/indranilbanerjee/socialforge) | 1.29.2 | `f8ed7dd44a39` | 21 | social creative: calendar to images, carousels, video and copy |

On every other platform (Claude Code, Cowork, Codex, Cursor, Copilot CLI, Antigravity, OpenClaw,
Grok) the three plugins are separate products installed from their own repos, which stay
self-contained; nothing here changes them. Only Hermes gets the combined folder.

## How it loads

- `plugin.yaml` + `__init__.py` is a skills-only Hermes plugin: it registers every `SKILL.md` of the
  three groups with `ctx.register_skill`. The skills keep their own names and Hermes shows them as
  `digital-marketing-pro:<skill>`. A test keeps the names unique across the groups.
- **What it adds to the system prompt.** Hermes lists the skills of an enabled plugin in the system
  prompt's skills index. This listing registers its 207 skills by name only (the adapter passes no
  descriptions): 207 rows, about 8,845 characters (roughly 2,211 tokens).
  Disable the plugin to remove them; a skill's full text loads with `skill_view` when it is asked for.
- It registers **no tools, hooks or middleware**, so `hermes tools` has nothing to switch on or off
  per group, and there is no group switch. Use the skills you want; ignore the rest.
- Each skill that runs a script says where it is when `${CLAUDE_PLUGIN_ROOT}` is not set (it is not set
  on Hermes): the group's `scripts/` folder, next to its `skills/`.

## What it never does

- **Install a package or a browser on its own.** A missing package prints its exact pinned install command;
  Playwright's browser and the optional packages install only when you say yes.
- **Send, publish or spend without your say-so.** Live writes wait for your typed `yes`; SocialForge
  shows a live price quote before any paid image or video generation and waits for "go".
- **Ask for an API key in the chat.** Keys come from environment variables.
- **Connect a service you did not set up.** No MCP server is configured by this listing and no hook runs.
- **Remove or hide AI watermarks.** AI involvement is disclosed, with C2PA provenance.

## Disclosures

These are the points a Hermes user should know before installing.

- **The agent creates and approves its own live-write records, and Hermes does not prompt before those
  script runs.** For writes the plugin sends itself (`/digital-marketing-pro:execute-action`), the script
  creates a single-use approval record at prepare, with a preview of the exact request. The skill approves
  that record after you type `yes`, and the request must match it byte for byte within 15 minutes. The
  record proves the approval step ran for this request, once; it cannot prove who typed `yes`, because
  the agent runs every command. Writes through MCP server tools are outside this check and rely on the
  skill's typed `yes` and your host's permission prompt. Keep script runs and MCP write tools out of
  your host's allowlist so it asks every time.
- **`refresh_models.py` reads your provider keys.** The optional model-registry refresh in each group
  reads `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` and `GEMINI_API_KEY` from the environment, and only when
  you run it; a provider without a key is skipped.
- **Keys and data live outside the Hermes profile.** SocialForge keeps its credentials and brand data in
  `~/socialforge-workspace` when no plugin-data folder is set; ContentForge and Digital Marketing Pro keep
  brand data under `~/.claude-marketing/`.
- **Installs run only when you say yes.** Nothing installs itself. SocialForge's setup lists what is
  missing and installs the pinned versions after an explicit `yes`.
- Network calls happen only when you, or a skill you invoked, run a script, and only to the endpoints each
  group lists in its `PRIVACY.md`.

Each group carries its own `README.md`, `PRIVACY.md` and `CHANGELOG.md` for the plugin it was copied from.

## What is left out

Tests, evals, most docs, research notes, hooks, workflows, the other platforms' manifests and the README
translations are not copied: a Hermes install never reads them. A `docs/` file stays when a skill, script
or agent points at it.

## Verifying

```bash
python __init__.py                       # what register() would do, without Hermes
python -c "import json;print(json.load(open('BUNDLE-MANIFEST.json'))['groups']['content']['commit'])"
```

`BUNDLE-MANIFEST.json` lists every copied file with its sha256. The marketplace's tests rebuild the folder
from those commits and fail on any difference, and Hermes's own `hermes plugins validate` runs on it.
