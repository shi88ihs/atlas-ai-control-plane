# Systemd Service Audit

## Purpose
Audit the host system's service manager (`systemd`) to identify the canonical source of truth for the Hermes AI runtime lifecycle and configuration.

## Summary
The audit successfully identified the canonical execution path for the AI engine: a user-level systemd service (`hermes-gateway.service`). By uncovering this, Atlas verified that legacy containerized versions of the engine were no longer active and that the deployment environment utilizes a robust, auto-restarting native Linux daemon structure.

## Architecture
- **Lifecycle Manager:** `systemd` (User instance)
- **Unit Name:** `hermes-gateway.service`
- **Execution Context:** Python virtual environment (`venv`) isolated to the `atlas-admin` user.
- **Environment Injection:** Loads `.env` configurations natively via `EnvironmentFile`.

## Implementation
1. **Systemd Query:** Ran `systemctl --user list-units` to discover active user-space processes.
2. **Unit Inspection:** Extracted configuration parameters (ExecStart, WorkingDirectory) using `systemctl --user cat`.
3. **Process Mapping:** Mapped the resulting `MainPID` to the underlying python process executing the runtime CLI.
4. **Log Tracing:** Verified that operational logs are continuously aggregated into `journalctl --user`, ensuring standard Linux observability.

## Outcome
The audit established the single pane of truth for runtime management. It allowed the deprecation of legacy orchestration structures (e.g., redundant Docker Compose files) and directed all future Atlas automation workflows to target the canonical `systemd` unit.

## Lessons Learned
- Utilizing `systemd --user` for agent runtimes provides deep OS-level integration (auto-restart, log rotation, environment enforcement) without requiring risky root escalation.
- Establishing the exact binary path (`.../venv/bin/python`) ensures that diagnostic tools inspect the correct dependencies and Python paths.