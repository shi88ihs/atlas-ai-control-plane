# System Overview

## Architecture
- The canonical AI runtime runs as a secure, systemd-managed gateway on the primary deployment host.
- Historical containerized variants (e.g. Docker deployments) have been deprecated to unify the process boundary under a single source of truth.
- The Atlas AI Control Plane provides a user-space documentation and operations coordination layer, enabling long-term fleet management.
- The workspace enforces a read-heavy, diagnostic-first approach; host-level mutations remain outside this operational plane to guarantee stability.

## Core Services
- Canonical runtime service: `hermes-gateway.service`
- Runtime execution model: long-lived user service, providing deep host integration without requiring root privileges.
- Atlas Control Plane tracks configuration state but does not directly modify system binaries or package management.

## Operations Ownership
- Atlas AI Control Plane records procedures, tracks telemetry, and manages orchestration scripts.
- The lifecycle authority (start/stop/restart) for the AI runtimes belongs to the runtime operator.
- Auxiliary AI runtimes (like OpenClaw) remain operationally adjacent and are managed as independent entities under the Atlas umbrella.

## Data Structure
- **Control Plane Root:** `/opt/data/home/control-plane`
- **Reports:** `/opt/data/home/control-plane/reports`
- **Backups:** `/opt/data/home/control-plane/backups/`
- Workspace configuration files and diagnostic helpers remain in user-space to avoid polluting system directories.

## Observability
- AI runtime gateway logs are tracked per component.
- Systemd journals are used as the primary source of operational event logs.
- Atlas Control Plane explicitly decouples its documentation layer from host daemon logs to prevent credential or sensitive data leakage in phase reports.

## Lifecycle Policy
- The logical restart target for the primary AI engine is `hermes-gateway.service`.
- Atlas Control Plane mandates that no restart occurs without explicit operational approval and a captured diagnostic baseline.
