# Runtime Capability Matrix

## Current runtime environment

- Operating system: Linux
- Distribution: Amazon Linux
- Version: Amazon Linux 2023
- Kernel: `6.1.174-217.345.amzn2023.x86_64`
- Architecture: `x86_64`
- Init system: `systemd`
- PID 1: `systemd`
- Current user: `ec2-user`
- Effective user: `ec2-user`
- Groups: `ec2-user`, `adm`, `wheel`, `systemd-journal`, `docker`
- `HOME` environment variable: `/home/ec2-user/.hermes/home`
- Passwd home for `ec2-user`: `/home/ec2-user`
- Current working directory: `/home/ec2-user`

## Runtime placement

Evidence indicates this process is running directly on the AWS host, not inside a container runtime:

- `systemd-detect-virt -c` returned `none`
- `/proc/1/cgroup` showed `0::/init.scope` with no Docker/Podman/Kubernetes markers
- PID 1 is `systemd`
- The host has Docker and Tailscale services running, but those are host-level processes, not evidence that the current shell is inside Docker

## Capability matrix

### Shell and language execution

- Execute shell commands: **Verified Available**
- Execute `bash`: **Verified Available**
- Execute `sh`: **Verified Available**
- Execute Python: **Verified Available**
- Execute Node: **Verified Available**
- Execute Git: **Verified Available**

### File and process inspection

- Read files: **Verified Available**
- Write files: **Verified Available** within the approved control-plane workspace
- Create directories: **Verified Available** within the approved control-plane workspace
- Rename files: **Unknown** (not tested)
- Inspect processes: **Verified Available**
- Inspect network interfaces: **Verified Available**
- Inspect listening ports: **Verified Available**
- Inspect environment variables: **Verified Available**
- Inspect mounted filesystems: **Verified Available**

### Privileged or host-adjacent access

- `sudo`: **Verified Available**
- `systemctl`: **Verified Available**
- `journalctl`: **Verified Available**
- Docker CLI: **Verified Available**
- Docker daemon: **Verified Available** (`docker info` returned server details)
- Tailscale CLI: **Verified Available**
- SSH client: **Verified Available**
- SSH server: **Verified Available**

### Network utilities

- `curl`: **Verified Available**
- `wget`: **Verified Available**
- `ping`: **Verified Available**
- `dig`: **Verified Available**
- `nslookup`: **Verified Available**

## Evidence highlights

- `docker info` succeeded and reported a live Docker daemon.
- `systemctl --user` showed active Hermes/OpenClaw gateway user services.
- `ss -ltnup` showed active listeners including local gateway ports and SSH on port 22.
- `curl https://example.com` returned `200`.
- `curl https://check.torproject.org` returned `200`.

## IMDS status

- AWS Instance Metadata Service (IMDS): **Not Tested (Approval Required)**

## SSH readiness

- SSH client: **Verified Available** (`/usr/bin/ssh`)
- Runtime `~/.ssh` under `/home/ec2-user/.hermes/home`: **missing**
- Login-home `/home/ec2-user/.ssh`: **present**
- Login-home `/home/ec2-user/.ssh/config`: **present**
- Login-home `/home/ec2-user/.ssh/known_hosts`: **present**

## Notes

- The runtime HOME (`/home/ec2-user/.hermes/home`) is different from the passwd home (`/home/ec2-user`).
- That mismatch matters for future SSH inventory and file-path assumptions.
- No mutating actions were taken during discovery.
