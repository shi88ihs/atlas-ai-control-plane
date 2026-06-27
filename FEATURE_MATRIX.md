# Feature Matrix

This document outlines the core capabilities of the Atlas AI Control Plane and its managed AI engines.

| Capability | Status | Description |
|---|---|---|
| **AI Providers** | ✅ Supported | Native support for Google Vertex AI, OpenAI, Anthropic, and custom endpoints. |
| **Multi-model Routing** | ✅ Supported | Dynamically route tasks to models based on cost, reasoning requirements, or configuration. |
| **Mission Control** | 🚧 In Progress | Unified web-based dashboard for single-pane-of-glass observability. |
| **Telegram Integration** | ✅ Supported | Built-in polling and message handling for remote agent communication. |
| **Docker Deployment** | ⏸️ Deprecated | Legacy Docker deployments have been deprecated in favor of native Systemd. |
| **Workflow Automation** | ✅ Supported | Cron-like execution and declarative job specifications via the Atlas Planner. |
| **Document Search** | ✅ Supported | Integrated tooling for searching logs, configurations, and historical memory. |
| **Monitoring** | ✅ Supported | Read-only Atlas Doctor and Status engines for host/container diagnostics. |
| **Self-Hosting** | ✅ Supported | Fully self-hosted architecture designed for Linux servers and cloud VPCs. |
| **Fleet Management** | 🔮 Planned | Coordinate multiple agent nodes across a distributed cloud topology. |
| **Impact Simulator** | 🔮 Planned | Dry-run AI tasks to predict and approve filesystem/network changes securely. |