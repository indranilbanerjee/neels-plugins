# Neel's Plugin Marketplace

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
| **[digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro)** | 2.2.0 | Comprehensive digital marketing execution system with 25 specialist agents, 16 integrated modules, 115 slash commands, 67 MCP integrations, agency operations, multilingual support, and quality assurance layer. |

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
