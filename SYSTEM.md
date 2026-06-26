# System

## Architecture
- The canonical Hermes runtime is the systemd-managed gateway running on the AWS host.
- The duplicate Docker deployment has been removed and is no longer the source of truth.
- The control plane in this workspace is a user-space documentation and coordination layer for long-term operations.
- The workspace is intentionally read-heavy and documentation-first; host-level changes remain outside this phase.

## Canonical installation
- Hermes installation: `/home/ec2-user/hermes-agent`
- Hermes configuration: `/home/ec2-user/.hermes`
- Control plane root: `/opt/data/home/control-plane`
- Reports: `/opt/data/home/control-plane/reports`

## Runtime
- Current machine: `ip-172-31-0-144.ap-southeast-2.compute.internal`
- Operating system: Amazon Linux 2023
- Kernel: `6.1.174-217.345.amzn2023.x86_64`
- Init system: systemd
- Canonical runtime service: `hermes-gateway.service`
- Service location: `/home/ec2-user/.config/systemd/user/hermes-gateway.service`
- Runtime model: long-lived user service, not a Docker-managed runtime

## Service ownership
- Hermes gateway ownership belongs to the Hermes runtime operator through the user-level systemd service.
- The control plane documents the runtime and records procedures; it does not own host system configuration.
- OpenClaw remains a separate operational concern and should not be conflated with Hermes gateway ownership.

## Data locations
- Primary control plane documents: `/opt/data/home/control-plane/`
- Inventory material: `/opt/data/home/control-plane/inventory/` when created
- Reports: `/opt/data/home/control-plane/reports/`
- Backups and snapshots for control-plane artifacts: `/opt/data/home/control-plane/backups/`
- Workspace notes and helper material should remain in user-space, not in system directories.

## Logs
- Hermes gateway logs: `~/.hermes/logs/gateway.log`
- Systemd journal for the user service: `journalctl --user -u hermes-gateway`
- Host service logs and daemon logs should be treated as separate from control-plane documentation.
- Any operational note captured here should link to evidence, not duplicate secrets or raw sensitive payloads.

## Restart ownership
- Restart authority for the canonical Hermes gateway belongs to the runtime operator.
- The approved logical restart target is the user service `hermes-gateway.service`.
- This phase does not change restart policy or service configuration.
- No restart should be attempted from the control plane without explicit operational approval and a verified reason.

## Backup locations
- Control-plane artifact backups: `/opt/data/home/control-plane/backups/`
- Human-readable phase reports: `/opt/data/home/control-plane/reports/`
- Any future inventory exports or snapshots should be copied into the workspace backup area before being treated as durable records.
- Host-level backups remain outside this documentation layer.
