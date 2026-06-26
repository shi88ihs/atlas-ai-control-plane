# Health Report Format

## Purpose
A health report should provide a consistent snapshot of the Atlas Control Plane and runtime state without requiring guesswork.

## Required sections
- Hermes
- Gateway
- OpenClaw
- SSH
- Tailscale
- Docker
- Disk
- RAM
- Swap
- Updates
- Overall status

## Section guidance
- **Hermes**: runtime version, process state, and any obvious error signals.
- **Gateway**: service state, uptime, and recent warnings or failures.
- **OpenClaw**: whether the separate OpenClaw runtime is healthy or needs follow-up.
- **SSH**: client availability, config sanity, and whether managed access paths are intact.
- **Tailscale**: connection state and tailnet reachability.
- **Docker**: daemon presence, whether it is incidental or relevant, and any warning signs.
- **Disk**: free space, growth pressure, and any mounts that need attention.
- **RAM**: available memory and obvious pressure indicators.
- **Swap**: presence, usage, and whether it is under stress.
- **Updates**: pending updates, patch lag, or maintenance notes.
- **Overall status**: one-line summary with a clear pass, warning, or fail label.

## Output shape
- Header with hostname and timestamp
- Short bullet for each required section
- Evidence notes for any warning or fail state
- Final overall status line

## Reporting rules
- Keep the report readable by humans first.
- Include evidence, not just labels.
- Do not include secrets, tokens, or private payloads.
- If a subsystem is unknown, say so explicitly instead of guessing.
