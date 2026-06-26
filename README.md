# Atlas Control Plane Workspace

This directory is the user-space Atlas Control Plane for operations and infrastructure management. It is a working area for structured inventory, notes, logs, scripts, templates, and reports that support runtime automation without changing host-level configuration.

## Directory guide

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
  - Purpose: user-space helper scripts for automation inside the Hermes runtime.
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

- `reports/`
  - Purpose: human-readable phase summaries and verification notes.
  - Put here: setup reports, audit summaries, completed task writeups.
  - Do not store here: raw dumps better suited for `logs/`.

- `templates/`
  - Purpose: reusable document and config templates.
  - Put here: markdown templates, JSON templates, runbook skeletons.
  - Do not store here: live secrets or environment-specific data.

- `sessions/`
  - Purpose: session-specific artifacts and handoff state.
  - Put here: session notes, checkpoints, in-progress task context.
  - Do not store here: permanent data that belongs in `inventory/` or `reports/`.

## Boundary: container vs AWS host

- The AWS host is the machine running the Hermes runtime and its supporting infrastructure.
- The Atlas Control Plane workspace is user-space data under `/opt/data/home/control-plane/`.
- Files here should describe, coordinate, or support runtime work — not alter host networking, SSH, Tailscale, Docker, firewalling, gateway processes, or package state.
- If a task requires host-level change, it must be handled separately and explicitly; this workspace is not the place to make those changes.

## Current known limitations

- This is only a documentation and coordination layer; it does not execute privileged changes by itself.
- Host-level state can still drift independently of these files.
- Sensitive material must be kept out of this tree unless a task explicitly requires a secure handling path.
- The workspace currently has no automation beyond the directory structure and documentation.

## Atlas Control Plane CLI wrapper

The status engine now has a simple user-space wrapper at:

- `/opt/data/home/control-plane/scripts/control-plane`

Supported commands:

- `control-plane status`
- `control-plane collect`
- `control-plane report`
- `control-plane doctor`
- `control-plane help`

Optional manual shell helpers are shown below. These examples are for copy/paste only; they do not modify shell profiles automatically.

### Bash

```bash
cp-status() {
  /opt/data/home/control-plane/scripts/control-plane status
}

cp-report() {
  /opt/data/home/control-plane/scripts/control-plane report
}
```

### Fish

```fish
function cp-status
    /opt/data/home/control-plane/scripts/control-plane status
end

function cp-report
    /opt/data/home/control-plane/scripts/control-plane report
end
```

## Next recommended phase

Phase 3 should add structured runtime inventory and a small set of user-space helper scripts, then define a repeatable workflow for:

1. recording host and container boundaries,
2. collecting non-sensitive runtime status,
3. storing phase reports,
4. and preparing safe handoff artifacts for future work.

Keep Phase 3 user-space only unless a separate host-level change is explicitly approved.