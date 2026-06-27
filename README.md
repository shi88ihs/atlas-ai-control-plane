# Atlas AI Control Plane Workspace

Atlas AI Control Plane is an operations and infrastructure management platform designed to orchestrate, diagnose, and automate AI execution engines (like Hermes and OpenClaw) across varied deployment environments. It provides a structured, read-only coordination layer that abstracts host-level differences, offering a single pane of glass for health monitoring, deployment verification, and continuous operations.

## What is Atlas?
Atlas is the "Kubernetes for autonomous AI." It is the operational bridge between ambitious AI agents and strict enterprise infrastructure. 

## Who is it for?
- **Platform Engineers & MLOps:** Teams deploying autonomous AI agents that need a reliable, host-agnostic way to monitor and manage them.
- **AI Developers:** Builders who want to separate their agent logic from their deployment operations.
- **Enterprise Ops Teams:** Organizations requiring clear auditing, boundary enforcement, and predictable environments for LLM workloads.

## Why does it exist?
Deploying autonomous agents introduces unique challenges: they need dynamic execution environments and host integrations, but granting them too much privilege creates security risks. Atlas exists to provide bounded, secure execution environments without restricting the agent's utility.

## What problems does it solve?
- **Visibility:** Unifies telemetry and logs across discrete AI runtimes.
- **Security Boundaries:** Enforces strict user-space isolation instead of root-level virtualization.
- **Auditability:** Uses GitOps to create an immutable history of every infrastructure change.

## How do I install it?
Installation guides and setup prerequisites are detailed in the `docs/deployment/` directory.

## How do I contribute?
Check out `CONTRIBUTING.md` for guidelines on submitting Pull Requests, formatting code, and writing sanitized Markdown reports.

## Where is the roadmap?
The feature roadmap is located at `docs/development/roadmap.md`.

## Where is the documentation?
The primary documentation lives in the `docs/` folder:
- `docs/architecture/` - System design and core features.
- `docs/deployment/` - Deployment models and limits.
- `docs/reports/` - Detailed technical analyses of system capabilities.

## Directory Guide

- `inventory/`
  - Purpose: tracked lists of runtime assets, endpoints, services, and references.
  - Put here: inventories, indexes, CSV/JSON/YAML snapshots, host notes.
  - Do not store here: secrets, private keys, host system configs, or transient scratch output.

- `logs/`
  - Purpose: runtime logs and troubleshooting traces.
  - Put here: command logs, debug output, event notes, capture files.
  - Do not store here: sensitive credentials or host daemon logs copied from restricted areas unless explicitly needed.

- `backups/`
  - Purpose: safe copies of workspace artifacts.
  - Put here: exported configs, snapshots, archived reports, rollback copies.
  - Do not store here: full host backups, images, or anything that belongs to system backup tooling.

- `ssh/`
  - Purpose: SSH-related notes and client-side runtime material only.
  - Put here: host aliases, connection notes, known_hosts exports, documentation.
  - Do not store here: private keys, passphrases, or host SSH daemon configuration.

- `scripts/`
  - Purpose: user-space helper scripts for automation inside the runtime.
  - Put here: shell scripts, Python utilities, one-off operational helpers.
  - Do not store here: privileged service scripts, package-manager hooks, or host boot scripts.

- `automation/`
  - Purpose: orchestration assets for repeatable runtime workflows.
  - Put here: cron-like notes, job specs, playbooks, automation manifests.
  - Do not store here: service units, systemd overrides, Docker daemon settings, or host-wide schedulers.

- `hosts/`
  - Purpose: inventory and metadata about reachable machines.
  - Put here: host profiles, connection metadata, role notes, boundary diagrams.
  - Do not store here: secrets, tokens, or direct credentials.

- `templates/`
  - Purpose: reusable document and config templates.
  - Put here: markdown templates, JSON templates, runbook skeletons.
  - Do not store here: live secrets or environment-specific data.

- `sessions/`
  - Purpose: session-specific artifacts and handoff state.
  - Put here: session notes, checkpoints, in-progress task context.
  - Do not store here: permanent data that belongs in `inventory/` or `reports/`.

## Boundary: Container vs Deployment Environment

- The deployment environment (e.g., cloud instance, bare metal) runs the AI runtime and supporting infrastructure.
- The Atlas Control Plane workspace operates strictly in user-space.
- Files here describe, coordinate, or support runtime work — they do not alter networking, SSH, VPNs, container engines, firewalling, or package state.
- If a task requires host-level change, it must be handled separately and explicitly via approved orchestration tools; this workspace is exclusively for operations control.

## Atlas Control Plane CLI Wrapper

The status engine offers a simple CLI wrapper for operational tasks:

- `./scripts/control-plane`

Supported commands:

- `control-plane status`
- `control-plane collect`
- `control-plane report`
- `control-plane doctor`
- `control-plane help`