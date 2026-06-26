# Phase 4 Summary

## Current execution environment

- Runtime user: `ec2-user`
- Effective user: `ec2-user`
- Current working directory: `/home/ec2-user`
- Runtime HOME: `/home/ec2-user/.hermes/home`
- Passwd home for `ec2-user`: `/home/ec2-user`
- OS: Amazon Linux 2023
- Kernel: `6.1.174-217.345.amzn2023.x86_64`
- Architecture: `x86_64`
- Init: `systemd`
- PID 1: `systemd`

## SSH readiness

- SSH client exists: yes (`/usr/bin/ssh`)
- Runtime `~/.ssh` exists: no, because runtime HOME is `/home/ec2-user/.hermes/home`
- Login-home `/home/ec2-user/.ssh` exists: yes
- Login-home config exists: yes (`/home/ec2-user/.ssh/config`)
- Login-home known_hosts exists: yes (`/home/ec2-user/.ssh/known_hosts`)
- Future SSH inventory should live in the control-plane workspace, not inside either home directory

## Canonical Control Plane location

- **Recommended canonical root:** `/opt/data/home/control-plane/`

## Capabilities available

Verified available:

- shell execution (`sh`, `bash`)
- Python 3
- Node
- Git
- file read/write in the control-plane workspace
- directory creation in the control-plane workspace
- process inspection
- network interface inspection
- listening-port inspection
- environment inspection
- mounted-filesystem inspection
- `sudo`
- `systemctl`
- `journalctl`
- Docker CLI and Docker daemon
- Tailscale CLI
- SSH client and SSH server
- `curl`, `wget`, `ping`, `dig`, `nslookup`

## Capabilities unavailable or unconfirmed

- Rename-file operations were not tested
- IMDS was intentionally not tested
- Any mutating host action remains out of scope for discovery

## Trust boundaries

- Safe user-space: docs, inventory, scripts, templates, reports, read-only inspection
- Container-only: operations inside a specific container filesystem or app process boundary
- Host-only: SSH, Tailscale, Docker daemon, systemd, firewall, package manager, host users
- AWS-only: EC2 metadata, SSM, instance/network governance, AWS-side recovery paths
- Future desktop-management: approved SSH/tunnel management of the local desktop machine

## Risks

- The runtime can see both host and container processes, so automation must not assume every visible process is controllable from the same boundary.
- The runtime HOME differs from the login home, which can mislead SSH and inventory code if not handled deliberately.
- Docker, Tailscale, and systemd are all present, so a script can cross a trust boundary very easily if it is not constrained.

## Recommended Phase 5

Build a minimal, read-only inventory seed and template system so future automation can generate consistent host profiles and capability snapshots without making any host-level changes.

## IMDS status

- AWS Instance Metadata Service (IMDS): **Not Tested (Approval Required)**
