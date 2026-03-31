# Neel's Plugin Marketplace

[![Version](https://img.shields.io/badge/version-1.21.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Plugins](https://img.shields.io/badge/plugins-3-orange.svg)](#-available-plugins)

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
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 2.7.0 | Plan, execute, and measure digital marketing across all channels. 25 specialist agents, 7 commands, 141 skills, 14 HTTP connectors. v2.6 adds 6 SEO sub-skills, expanded schema markup (18 types), Google SEO reference, and DataForSEO integration. |
| **[contentforge](https://github.com/indranilbanerjee/contentforge)** | 3.8.0 | Enterprise content production pipeline with 13 agents, 19 skills, 9 HTTP connectors, 6 evals. v3.7 adds SERP-informed title curation, pre-flight brand validation, scoring fixes, per-phase tracking, expanded brand profiles. |
| **[socialforge](https://github.com/indranilbanerjee/socialforge)** | 1.2.0 | Agency-grade social media calendar automation with asset-first compositing. 4 creative modes, 8 carousel templates, multi-brand, multi-tier approval, compliance checking. |

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
├── CHANGELOG.md             ← Release history
└── README.md                ← This file
```

---

## 📄 License

MIT © Indranil Banerjee
