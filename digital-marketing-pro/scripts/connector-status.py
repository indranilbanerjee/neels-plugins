#!/usr/bin/env python3
"""
connector-status.py
===================
Connector discovery and status reporting for Digital Marketing Pro.

Reports which MCP connectors are configured (HTTP and npx), which are
available but not yet connected, and which skills gain capabilities
from each connector category.

Usage:
    python connector-status.py --action status          # Full status dashboard
    python connector-status.py --action list-available   # All available connectors
    python connector-status.py --action check <name>     # Check specific connector
    python connector-status.py --action setup-guide <name>  # Setup instructions for a connector
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Plugin root = parent of scripts/
PLUGIN_ROOT = Path(__file__).resolve().parent.parent
MCP_JSON = PLUGIN_ROOT / ".mcp.json"
MCP_EXAMPLE = PLUGIN_ROOT / ".mcp.json.example"

# ── Connector Registry ──────────────────────────────────────────────
# Every connector the plugin knows about, grouped by category.
# "http" = available as HTTP connector (works in Cowork + Claude Code)
# "npx"  = requires local npx server (Claude Code only)

CONNECTOR_REGISTRY = {
    "chat": {
        "description": "Team messaging and notifications",
        "connectors": {
            "slack": {
                "transport": "http",
                "url": "https://mcp.slack.com/mcp",
                "description": "Slack — send reports, alerts, team notifications",
                "env_vars": [],
                "skills_unlocked": [
                    "send-notification", "send-report", "campaign-status"
                ],
            },
            "intercom": {
                "transport": "npx",
                "package": "mcp-intercom",
                "description": "Intercom — customer messaging, churn detection",
                "env_vars": ["INTERCOM_ACCESS_TOKEN"],
                "skills_unlocked": ["send-notification"],
            },
        },
    },
    "design": {
        "description": "Visual design and creative assets",
        "connectors": {
            "canva": {
                "transport": "http",
                "url": "https://mcp.canva.com/mcp",
                "description": "Canva — design creation, brand kit, templates",
                "env_vars": [],
                "skills_unlocked": ["ad-creative", "social-strategy"],
            },
            "figma": {
                "transport": "http",
                "url": "https://mcp.figma.com/mcp",
                "description": "Figma — design files, prototypes, components",
                "env_vars": [],
                "skills_unlocked": ["ad-creative", "landing-page-audit"],
            },
        },
    },
    "crm": {
        "description": "Customer relationship management",
        "connectors": {
            "hubspot": {
                "transport": "http",
                "url": "https://mcp.hubspot.com/anthropic",
                "description": "HubSpot — contacts, deals, email, pipeline",
                "env_vars": [],
                "skills_unlocked": [
                    "crm-sync", "lead-import", "pipeline-update",
                    "segment-audience", "client-report",
                ],
            },
            "salesforce": {
                "transport": "npx",
                "package": "mcp-salesforce",
                "description": "Salesforce — CRM pipeline, leads, accounts",
                "env_vars": [
                    "SALESFORCE_INSTANCE_URL", "SALESFORCE_ACCESS_TOKEN"
                ],
                "skills_unlocked": [
                    "crm-sync", "lead-import", "pipeline-update",
                    "segment-audience",
                ],
            },
            "pipedrive": {
                "transport": "npx",
                "package": "mcp-pipedrive",
                "description": "Pipedrive — deal pipeline, contacts, activities",
                "env_vars": ["PIPEDRIVE_API_TOKEN"],
                "skills_unlocked": [
                    "crm-sync", "lead-import", "pipeline-update",
                ],
            },
            "zoho-crm": {
                "transport": "npx",
                "package": "mcp-zoho-crm",
                "description": "Zoho CRM — leads, contacts, deals, campaigns",
                "env_vars": [
                    "ZOHO_CLIENT_ID", "ZOHO_CLIENT_SECRET",
                    "ZOHO_REFRESH_TOKEN",
                ],
                "skills_unlocked": [
                    "crm-sync", "lead-import", "pipeline-update",
                ],
            },
        },
    },
    "seo": {
        "description": "Search engine optimization and analysis",
        "connectors": {
            "ahrefs": {
                "transport": "http",
                "url": "https://api.ahrefs.com/mcp/mcp",
                "description": "Ahrefs — backlinks, keywords, content gaps",
                "env_vars": [],
                "skills_unlocked": [
                    "seo-audit", "keyword-research", "competitor-analysis",
                    "tech-seo-audit", "content-decay-scan",
                ],
            },
            "similarweb": {
                "transport": "http",
                "url": "https://mcp.similarweb.com",
                "description": "Similarweb — traffic analysis, competitor benchmarks",
                "env_vars": [],
                "skills_unlocked": [
                    "competitor-analysis", "share-of-voice",
                ],
            },
            "semrush": {
                "transport": "npx",
                "package": "mcp-semrush",
                "description": "SEMrush — keyword research, site audit, backlinks",
                "env_vars": ["SEMRUSH_API_KEY"],
                "skills_unlocked": [
                    "seo-audit", "keyword-research", "competitor-analysis",
                ],
            },
            "moz": {
                "transport": "npx",
                "package": "mcp-moz",
                "description": "Moz — domain authority, rank tracking, SERP",
                "env_vars": ["MOZ_ACCESS_ID", "MOZ_SECRET_KEY"],
                "skills_unlocked": ["seo-audit", "keyword-research"],
            },
        },
    },
    "email-marketing": {
        "description": "Email campaigns and automation",
        "connectors": {
            "klaviyo": {
                "transport": "http",
                "url": "https://mcp.klaviyo.com/mcp",
                "description": "Klaviyo — email/SMS campaigns, flows, segmentation",
                "env_vars": [],
                "skills_unlocked": [
                    "send-email-campaign", "email-sequence",
                    "segment-audience",
                ],
            },
            "mailchimp": {
                "transport": "npx",
                "package": "mcp-mailchimp",
                "description": "Mailchimp — email campaigns, lists, automation",
                "env_vars": ["MAILCHIMP_API_KEY"],
                "skills_unlocked": [
                    "send-email-campaign", "email-sequence",
                ],
            },
            "sendgrid": {
                "transport": "npx",
                "package": "mcp-sendgrid",
                "description": "SendGrid — transactional + marketing email",
                "env_vars": ["SENDGRID_API_KEY"],
                "skills_unlocked": ["send-email-campaign"],
            },
            "brevo": {
                "transport": "npx",
                "package": "mcp-brevo",
                "description": "Brevo — email/SMS/WhatsApp, automation, CRM",
                "env_vars": ["BREVO_API_KEY"],
                "skills_unlocked": [
                    "send-email-campaign", "send-sms",
                ],
            },
            "customer-io": {
                "transport": "npx",
                "package": "mcp-customer-io",
                "description": "Customer.io — behavioral email/SMS, segments",
                "env_vars": ["CUSTOMERIO_API_KEY"],
                "skills_unlocked": [
                    "send-email-campaign", "email-sequence",
                ],
            },
        },
    },
    "advertising": {
        "description": "Paid ad platforms",
        "connectors": {
            "google-ads": {
                "transport": "npx",
                "package": "mcp-google-ads",
                "description": "Google Ads — campaigns, keywords, bid optimization",
                "env_vars": [
                    "GOOGLE_ADS_CUSTOMER_ID",
                    "GOOGLE_ADS_DEVELOPER_TOKEN",
                    "GOOGLE_APPLICATION_CREDENTIALS",
                ],
                "skills_unlocked": [
                    "launch-ad-campaign", "performance-check",
                    "budget-tracker", "media-plan",
                ],
            },
            "meta-marketing": {
                "transport": "npx",
                "package": "mcp-meta-marketing",
                "description": "Meta — Facebook/Instagram ads, audiences",
                "env_vars": [
                    "META_ACCESS_TOKEN", "META_AD_ACCOUNT_ID"
                ],
                "skills_unlocked": [
                    "launch-ad-campaign", "performance-check",
                    "budget-tracker", "media-plan",
                ],
            },
            "linkedin-marketing": {
                "transport": "npx",
                "package": "mcp-linkedin-marketing",
                "description": "LinkedIn Ads — B2B targeting, company pages",
                "env_vars": [
                    "LINKEDIN_ACCESS_TOKEN", "LINKEDIN_AD_ACCOUNT_ID"
                ],
                "skills_unlocked": [
                    "launch-ad-campaign", "performance-check",
                    "media-plan",
                ],
            },
            "tiktok-ads": {
                "transport": "npx",
                "package": "mcp-tiktok-ads",
                "description": "TikTok Ads — campaigns, creative insights",
                "env_vars": [
                    "TIKTOK_ACCESS_TOKEN", "TIKTOK_ADVERTISER_ID"
                ],
                "skills_unlocked": [
                    "launch-ad-campaign", "performance-check",
                    "media-plan",
                ],
            },
        },
    },
    "analytics": {
        "description": "Website and product analytics",
        "connectors": {
            "amplitude": {
                "transport": "http",
                "url": "https://mcp.amplitude.com/mcp",
                "description": "Amplitude — behavioral analytics, experiments",
                "env_vars": [],
                "skills_unlocked": [
                    "performance-check", "cohort-analysis",
                    "funnel-audit",
                ],
            },
            "google-analytics": {
                "transport": "npx",
                "package": "@anthropic/mcp-google-analytics",
                "description": "Google Analytics 4 — traffic, conversions, audiences",
                "env_vars": [
                    "GA_PROPERTY_ID", "GOOGLE_APPLICATION_CREDENTIALS"
                ],
                "skills_unlocked": [
                    "performance-check", "seo-audit",
                    "funnel-audit", "attribution-report",
                ],
            },
            "google-search-console": {
                "transport": "npx",
                "package": "@anthropic/mcp-google-search-console",
                "description": "Google Search Console — rankings, queries, CTR",
                "env_vars": [
                    "GSC_SITE_URL", "GOOGLE_APPLICATION_CREDENTIALS"
                ],
                "skills_unlocked": [
                    "seo-audit", "keyword-research",
                    "tech-seo-audit", "rank-monitor",
                ],
            },
            "mixpanel": {
                "transport": "npx",
                "package": "mcp-mixpanel",
                "description": "Mixpanel — events, funnels, user behavior",
                "env_vars": ["MIXPANEL_API_TOKEN"],
                "skills_unlocked": [
                    "performance-check", "cohort-analysis",
                    "funnel-audit",
                ],
            },
        },
    },
    "social-media": {
        "description": "Social media publishing and management",
        "connectors": {
            "twitter-x": {
                "transport": "npx",
                "package": "mcp-twitter",
                "description": "Twitter/X — post tweets, threads, media uploads",
                "env_vars": [
                    "TWITTER_API_KEY", "TWITTER_API_SECRET",
                    "TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_SECRET",
                ],
                "skills_unlocked": ["schedule-social", "social-strategy"],
            },
            "linkedin-publishing": {
                "transport": "npx",
                "package": "mcp-linkedin-publishing",
                "description": "LinkedIn — post articles, share updates",
                "env_vars": ["LINKEDIN_ACCESS_TOKEN"],
                "skills_unlocked": ["schedule-social", "social-strategy"],
            },
            "instagram": {
                "transport": "npx",
                "package": "mcp-instagram",
                "description": "Instagram — publish images/videos, insights",
                "env_vars": [
                    "INSTAGRAM_ACCESS_TOKEN",
                    "INSTAGRAM_BUSINESS_ACCOUNT_ID",
                ],
                "skills_unlocked": ["schedule-social", "social-strategy"],
            },
            "tiktok-content": {
                "transport": "npx",
                "package": "mcp-tiktok-content",
                "description": "TikTok — publish videos/photos, creator tools",
                "env_vars": ["TIKTOK_ACCESS_TOKEN"],
                "skills_unlocked": ["schedule-social", "social-strategy"],
            },
            "pinterest": {
                "transport": "npx",
                "package": "mcp-pinterest",
                "description": "Pinterest — create pins, manage boards",
                "env_vars": ["PINTEREST_ACCESS_TOKEN"],
                "skills_unlocked": ["schedule-social", "social-strategy"],
            },
            "youtube": {
                "transport": "npx",
                "package": "mcp-youtube",
                "description": "YouTube — upload videos, playlists, Shorts",
                "env_vars": ["YOUTUBE_OAUTH_TOKEN"],
                "skills_unlocked": [
                    "schedule-social", "video-script",
                ],
            },
        },
    },
    "knowledge-base": {
        "description": "Documentation, wikis, and knowledge management",
        "connectors": {
            "notion": {
                "transport": "http",
                "url": "https://mcp.notion.com/mcp",
                "description": "Notion — brand docs, campaign wikis, databases",
                "env_vars": [],
                "skills_unlocked": [
                    "save-knowledge", "search-knowledge",
                    "content-calendar",
                ],
            },
        },
    },
    "product-analytics": {
        "description": "Product and behavioral analytics",
        "connectors": {
            "amplitude": {
                "transport": "http",
                "url": "https://mcp.amplitude.com/mcp",
                "description": "Amplitude — behavioral analytics, cohorts",
                "env_vars": [],
                "skills_unlocked": [
                    "performance-check", "cohort-analysis",
                    "funnel-audit",
                ],
            },
        },
    },
    "payments": {
        "description": "Payment processing and revenue data",
        "connectors": {
            "stripe": {
                "transport": "http",
                "url": "https://mcp.stripe.com/",
                "description": "Stripe — revenue, conversions, LTV calculations",
                "env_vars": [],
                "skills_unlocked": [
                    "roi-calculator", "performance-check",
                    "attribution-report",
                ],
            },
        },
    },
    "project-management": {
        "description": "Task and project tracking",
        "connectors": {
            "asana": {
                "transport": "http",
                "url": "https://mcp.asana.com/sse",
                "description": "Asana — tasks, timelines, team workload",
                "env_vars": [],
                "skills_unlocked": [
                    "team-assign", "campaign-plan",
                ],
            },
            "linear": {
                "transport": "npx",
                "package": "mcp-linear",
                "description": "Linear — issues, sprints, project tracking",
                "env_vars": ["LINEAR_API_KEY"],
                "skills_unlocked": ["team-assign"],
            },
            "jira": {
                "transport": "npx",
                "package": "mcp-jira",
                "description": "Jira — issues, sprints, workflows",
                "env_vars": [
                    "JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN"
                ],
                "skills_unlocked": ["team-assign"],
            },
            "clickup": {
                "transport": "npx",
                "package": "mcp-clickup",
                "description": "ClickUp — projects, docs, goals, time tracking",
                "env_vars": ["CLICKUP_API_TOKEN"],
                "skills_unlocked": ["team-assign"],
            },
        },
    },
    "cms": {
        "description": "Content management and publishing",
        "connectors": {
            "webflow": {
                "transport": "http",
                "url": "https://mcp.webflow.com/sse",
                "description": "Webflow — CMS, landing pages, design updates",
                "env_vars": [],
                "skills_unlocked": [
                    "publish-blog", "landing-page-audit",
                    "seo-implement",
                ],
            },
            "wordpress": {
                "transport": "npx",
                "package": "mcp-wordpress",
                "description": "WordPress — posts, pages, SEO metadata",
                "env_vars": [
                    "WORDPRESS_SITE_URL", "WORDPRESS_AUTH_TOKEN"
                ],
                "skills_unlocked": [
                    "publish-blog", "seo-implement",
                ],
            },
        },
    },
    "calendar": {
        "description": "Calendar and scheduling",
        "connectors": {
            "google-calendar": {
                "transport": "http",
                "url": "https://gcal.mcp.claude.com/mcp",
                "description": "Google Calendar — events, meeting scheduling",
                "env_vars": [],
                "skills_unlocked": ["webinar-plan", "content-calendar"],
            },
        },
    },
    "email": {
        "description": "Email communication",
        "connectors": {
            "gmail": {
                "transport": "http",
                "url": "https://gmail.mcp.claude.com/mcp",
                "description": "Gmail — send reports, team communication",
                "env_vars": [],
                "skills_unlocked": ["send-report", "pr-pitch"],
            },
        },
    },
    "sms-messaging": {
        "description": "SMS and messaging platforms",
        "connectors": {
            "twilio": {
                "transport": "npx",
                "package": "mcp-twilio",
                "description": "Twilio — SMS/MMS, WhatsApp for campaigns",
                "env_vars": [
                    "TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"
                ],
                "skills_unlocked": ["send-sms"],
            },
        },
    },
    "translation": {
        "description": "Translation and localization",
        "connectors": {
            "deepl": {
                "transport": "npx",
                "package": "deepl-mcp-server",
                "description": "DeepL — professional translation, 30+ languages",
                "env_vars": ["DEEPL_API_KEY"],
                "skills_unlocked": [
                    "translate-content", "localize-campaign",
                ],
            },
            "sarvam-ai": {
                "transport": "npx",
                "package": "sarvam-mcp-server",
                "description": "Sarvam AI — 22 Indian languages specialist",
                "env_vars": ["SARVAM_API_KEY"],
                "skills_unlocked": [
                    "translate-content", "localize-campaign",
                ],
            },
        },
    },
    "productivity": {
        "description": "Document storage, spreadsheets, and collaboration",
        "connectors": {
            "google-drive": {
                "transport": "npx",
                "package": "mcp-google-drive",
                "description": "Google Drive — docs, assets, brand knowledge vault, output delivery",
                "env_vars": ["GOOGLE_APPLICATION_CREDENTIALS"],
                "skills_unlocked": [
                    "content-brief", "content-repurpose", "save-knowledge",
                    "import-guidelines", "client-report",
                ],
                "note": "Also available as a native Claude platform integration (Settings > Integrations)",
            },
            "google-sheets": {
                "transport": "npx",
                "package": "mcp-google-sheets",
                "description": "Google Sheets — reporting dashboards, data export, tracking",
                "env_vars": ["GOOGLE_APPLICATION_CREDENTIALS"],
                "skills_unlocked": [
                    "data-export", "performance-report", "client-report",
                    "live-dashboard",
                ],
            },
            "google-docs": {
                "transport": "npx",
                "package": "mcp-google-docs",
                "description": "Google Docs — collaborative content editing, deliverable output",
                "env_vars": ["GOOGLE_APPLICATION_CREDENTIALS"],
                "skills_unlocked": [
                    "content-brief", "client-proposal", "client-report",
                ],
                "note": "Also available as a native Claude platform integration (Settings > Integrations)",
            },
        },
    },
    "database": {
        "description": "Data storage and querying",
        "connectors": {
            "bigquery": {
                "transport": "npx",
                "package": "mcp-bigquery",
                "description": "BigQuery — marketing data warehouse, SQL queries",
                "env_vars": [
                    "GOOGLE_APPLICATION_CREDENTIALS", "BIGQUERY_PROJECT_ID"
                ],
                "skills_unlocked": [
                    "data-export", "performance-report",
                ],
            },
            "supabase": {
                "transport": "npx",
                "package": "mcp-supabase",
                "description": "Supabase — PostgreSQL for custom marketing data",
                "env_vars": ["SUPABASE_URL", "SUPABASE_KEY"],
                "skills_unlocked": ["data-export"],
            },
        },
    },
    "memory": {
        "description": "Persistent memory and knowledge graphs",
        "connectors": {
            "pinecone": {
                "transport": "npx",
                "package": "@pinecone-database/mcp",
                "description": "Pinecone — vector DB for brand RAG, search",
                "env_vars": ["PINECONE_API_KEY"],
                "skills_unlocked": [
                    "save-knowledge", "search-knowledge",
                    "sync-memory",
                ],
            },
            "qdrant": {
                "transport": "npx",
                "package": "mcp-server-qdrant",
                "description": "Qdrant — self-hosted vector search",
                "env_vars": ["QDRANT_URL", "QDRANT_API_KEY"],
                "skills_unlocked": [
                    "save-knowledge", "search-knowledge",
                    "sync-memory",
                ],
            },
        },
    },
    "ecommerce": {
        "description": "E-commerce platforms",
        "connectors": {
            "shopify": {
                "transport": "npx",
                "package": "mcp-shopify",
                "description": "Shopify — orders, products, customers, analytics",
                "env_vars": [
                    "SHOPIFY_STORE_URL", "SHOPIFY_ACCESS_TOKEN"
                ],
                "skills_unlocked": [
                    "performance-check", "roi-calculator",
                ],
            },
        },
    },
}


def _load_mcp_json():
    """Load the active .mcp.json and return configured server names."""
    if not MCP_JSON.exists():
        return {}
    try:
        data = json.loads(MCP_JSON.read_text(encoding="utf-8"))
        return data.get("mcpServers", {})
    except (json.JSONDecodeError, KeyError):
        return {}


def _is_configured(name, connector_info, active_servers):
    """Check if a connector is currently configured."""
    # HTTP connectors in .mcp.json
    if name in active_servers:
        return True
    # Check env vars for npx connectors
    if connector_info["transport"] == "npx" and connector_info.get("env_vars"):
        return all(os.environ.get(v) for v in connector_info["env_vars"])
    return False


def status_dashboard():
    """Full status dashboard of all connectors."""
    active_servers = _load_mcp_json()

    categories = []
    total_connected = 0
    total_available = 0

    for cat_key, cat_info in CONNECTOR_REGISTRY.items():
        connected = []
        available = []

        for name, conn in cat_info["connectors"].items():
            total_available += 1
            entry = {
                "name": name,
                "description": conn["description"],
                "transport": conn["transport"],
                "skills_unlocked": conn["skills_unlocked"],
            }

            if _is_configured(name, conn, active_servers):
                entry["status"] = "connected"
                connected.append(entry)
                total_connected += 1
            else:
                entry["status"] = "available"
                if conn["transport"] == "npx":
                    entry["env_vars_needed"] = conn["env_vars"]
                    entry["note"] = "Claude Code only (requires npx)"
                else:
                    entry["note"] = "HTTP connector — works in Cowork + Claude Code"
                if "note" in conn:
                    entry["platform_note"] = conn["note"]
                available.append(entry)

        categories.append({
            "category": cat_key,
            "description": cat_info["description"],
            "connected": connected,
            "available": available,
            "connected_count": len(connected),
            "total_count": len(connected) + len(available),
        })

    return {
        "summary": {
            "total_connected": total_connected,
            "total_available": total_available,
            "coverage_percent": round(
                (total_connected / total_available * 100) if total_available else 0
            ),
        },
        "categories": categories,
    }


def list_available():
    """List all available connectors not yet configured."""
    active_servers = _load_mcp_json()
    available = []

    for cat_key, cat_info in CONNECTOR_REGISTRY.items():
        for name, conn in cat_info["connectors"].items():
            if not _is_configured(name, conn, active_servers):
                entry = {
                    "name": name,
                    "category": cat_key,
                    "description": conn["description"],
                    "transport": conn["transport"],
                    "skills_unlocked": conn["skills_unlocked"],
                }
                if conn["transport"] == "npx":
                    entry["env_vars_needed"] = conn["env_vars"]
                available.append(entry)

    return {"available_connectors": available, "count": len(available)}


def check_connector(name):
    """Check status of a specific connector."""
    active_servers = _load_mcp_json()

    for cat_key, cat_info in CONNECTOR_REGISTRY.items():
        if name in cat_info["connectors"]:
            conn = cat_info["connectors"][name]
            configured = _is_configured(name, conn, active_servers)

            result = {
                "name": name,
                "category": cat_key,
                "description": conn["description"],
                "transport": conn["transport"],
                "status": "connected" if configured else "not_connected",
                "skills_unlocked": conn["skills_unlocked"],
            }

            if conn["transport"] == "http":
                result["url"] = conn.get("url", "")
                result["setup"] = "HTTP connector — auto-connects via OAuth when you first use it"
            else:
                result["package"] = conn.get("package", "")
                result["env_vars"] = conn.get("env_vars", [])
                if not configured:
                    env_status = {}
                    for v in conn.get("env_vars", []):
                        env_status[v] = "set" if os.environ.get(v) else "missing"
                    result["env_var_status"] = env_status
                    result["setup"] = (
                        f"Requires npx server. Set environment variables: "
                        f"{', '.join(conn['env_vars'])}. "
                        f"Then add to .mcp.json or use /dm:add-integration."
                    )

            return result

    return {"error": f"Unknown connector: {name}", "hint": "Run --action list-available to see all connectors"}


def setup_guide(name):
    """Detailed setup guide for a specific connector."""
    active_servers = _load_mcp_json()

    for cat_key, cat_info in CONNECTOR_REGISTRY.items():
        if name in cat_info["connectors"]:
            conn = cat_info["connectors"][name]
            configured = _is_configured(name, conn, active_servers)

            guide = {
                "name": name,
                "category": cat_key,
                "description": conn["description"],
                "already_configured": configured,
                "skills_unlocked": conn["skills_unlocked"],
            }

            if conn["transport"] == "http":
                guide["transport"] = "http"
                guide["url"] = conn.get("url", "")
                guide["steps"] = [
                    f"This connector is already in .mcp.json as an HTTP connector.",
                    f"When you first use a skill that needs {name}, Claude will prompt you to authorize via OAuth.",
                    f"No API keys or environment variables needed — authentication is handled by the platform.",
                    f"Works in both Claude Code and Cowork.",
                ]
                if configured:
                    guide["status_message"] = (
                        f"{name} is configured. Use any of these skills to activate it: "
                        + ", ".join(f"/dm:{s}" for s in conn["skills_unlocked"])
                    )
            else:
                guide["transport"] = "npx"
                guide["package"] = conn.get("package", "")
                guide["env_vars"] = conn.get("env_vars", [])
                guide["steps"] = [
                    f"1. Obtain API credentials from the {name} platform.",
                    f"2. Set these environment variables: {', '.join(conn['env_vars'])}",
                    f"3. Add the connector to .mcp.json using /dm:add-integration {name}",
                    f"   Or manually add this to .mcp.json:",
                ]
                guide["mcp_json_entry"] = {
                    name: {
                        "command": "npx",
                        "args": ["-y", conn["package"]],
                        "env": {v: f"${{{v}}}" for v in conn["env_vars"]},
                    }
                }
                guide["notes"] = [
                    "npx connectors require Node.js installed locally.",
                    "Works in Claude Code only (not Cowork).",
                    "API keys are read from environment variables — never stored in plugin files.",
                ]

            return guide

    return {"error": f"Unknown connector: {name}", "hint": "Run --action list-available to see all connectors"}


def main():
    parser = argparse.ArgumentParser(description="Connector status and discovery")
    parser.add_argument("--action", required=True,
                        choices=["status", "list-available", "check", "setup-guide"])
    parser.add_argument("--name", help="Connector name (for check/setup-guide)")
    parser.add_argument("name_positional", nargs="?", help="Connector name (positional)")
    args = parser.parse_args()

    name = args.name or args.name_positional

    if args.action == "status":
        result = status_dashboard()
    elif args.action == "list-available":
        result = list_available()
    elif args.action == "check":
        if not name:
            result = {"error": "Provide connector name: --name <name>"}
        else:
            result = check_connector(name)
    elif args.action == "setup-guide":
        if not name:
            result = {"error": "Provide connector name: --name <name>"}
        else:
            result = setup_guide(name)
    else:
        result = {"error": f"Unknown action: {args.action}"}

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
