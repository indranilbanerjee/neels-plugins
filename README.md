# Neel's Plugin Marketplace

[![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-2-orange.svg)](#-available-plugins)

A custom plugin marketplace for **Claude Code** and **Claude Cowork** — built and maintained by [Indranil Banerjee](https://www.linkedin.com/in/askneelnow/).

---

## 🚀 Quick Start

### 1. Add this marketplace to Claude

```
/plugin marketplace add indranilbanerjee/neels-plugins
```

### 2. Browse available plugins

```
/plugin list neels-plugins
```

### 3. Install a plugin

```
/plugin install digital-marketing-pro@neels-plugins
```

---

## 📦 Available Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 2.5.0 | Plan, execute, and measure digital marketing across all channels. 25 specialist agents, 7 commands, 118 skills, 14 HTTP connectors, connector discovery and onboarding. |
| **[contentforge](https://github.com/indranilbanerjee/contentforge)** | 3.1.0 | Enterprise content production pipeline with 12 agents, 7 commands, 18 skills, and zero hallucinations. Research, draft, fact-check, humanize, publish, translate, and repurpose. |

---

## 🔧 For Developers

### Adding a New Plugin

1. Create your plugin with a `.claude-plugin/plugin.json` manifest
2. Push it to its own GitHub repository
3. Add an entry to `.claude-plugin/marketplace.json` in this repo
4. Commit and push — the marketplace updates instantly

### Marketplace Structure

```
neels-plugins/
├── .claude-plugin/
│   └── marketplace.json     ← Plugin catalog
└── README.md                ← This file
```

---

## 📄 License

MIT © Indranil Banerjee
