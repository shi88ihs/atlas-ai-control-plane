# Runtime Capability Matrix

## Purpose
Determine the execution boundary, available system tools, and isolation level of the AI runtime environments to inform safe operational constraints.

## Summary
The active runtime is executing natively within the deployment environment's user space (not inside a Docker container), leveraging a modern Linux kernel. The primary AI agents run under the restricted `atlas-admin` user, providing robust file and network access within a defined boundary while maintaining secure, non-root execution principles.

## Architecture
- **Environment:** Native Linux deployment environment
- **Init System:** `systemd` (PID 1)
- **User Context:** Restricted user (`atlas-admin`) without root evasion vectors via execution tools.
- **Process Model:** Long-lived user-space daemons managed by systemd (`systemctl --user`).

## Implementation / Capabilities
1. **Core Utilities:** Full shell/language execution validated (Bash, Python, Node, Git).
2. **System Tooling:** Process (`ps`), socket (`ss`), and interface (`ip`) inspection is fully available.
3. **Container Access:** Docker daemon socket is accessible to the user, enabling the orchestrator to spawn short-lived ephemeral workers.
4. **Networking:** `curl`, `ping`, `dig` verified for external and internal DNS resolution.
5. **Secure Overlay:** Tailscale and SSH binaries are present for secure outbound dialing.

## Outcome
The Atlas control plane correctly operates in a privileged user-space context. It possesses enough capability to observe the entire system state, manage secondary Docker-based workloads, and self-update via Git, without necessitating full `root` access for standard operations.

## Lessons Learned
- Verifying the exact `HOME` and user-space boundary early prevents subtle path resolution bugs when deploying user-level systemd services.
- Access to the Docker socket from the `atlas-admin` user is a powerful architectural choice, allowing the AI orchestrator to manage fleets without breaking standard Unix privilege separation.