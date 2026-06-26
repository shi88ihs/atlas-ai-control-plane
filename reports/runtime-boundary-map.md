# Runtime Boundary Map

## Safe user-space operations

Safe in the Hermes runtime workspace:

- Read and write files under `/opt/data/home/control-plane/`
- Create inventories, reports, notes, and templates
- Add helper scripts that only read local state or produce documentation
- Inspect processes, ports, routes, DNS, environment, and mounted filesystems
- Run read-only health checks and discovery commands

Examples:

- `read_file` / `write_file` on workspace documents
- `ps`, `ss`, `ip`, `findmnt`, `curl`, `journalctl` in read-only mode

## Container-only operations

These belong to a specific container boundary, not the host:

- Editing files inside a Docker container’s own filesystem
- Inspecting container logs and container-local environment
- Working with app-specific config that lives only inside the container image or container volume
- Reproducing behavior in a containerized app without changing the host

Examples:

- A containerized Hermes/OpenClaw app directory
- Container-local runtime logs
- Container entrypoint state

## Host-only operations

These require AWS host access and should not be assumed safe from user-space:

- SSH daemon config
- Tailscale config and route management
- systemd unit edits or restarts
- Firewall rules
- Docker daemon config
- Package manager operations
- Host user account changes

Examples:

- Editing `/etc/systemd/system/*.service`
- Changing host firewall policy
- Reconfiguring Docker networking

## AWS-only operations

These are AWS-side host/platform actions, separate from local user-space work:

- EC2 metadata access
- Instance recovery and SSM workflows
- Security group or network policy changes in AWS
- IAM or AWS-console-based management
- Host boot/recovery decisions that belong to the AWS instance boundary

Examples:

- Reading IMDS
- Using SSM session access
- Changing the EC2 security group

## Future desktop-management operations

These belong to the local desktop/laptop fleet-management boundary, not the AWS host:

- Approved SSH access to the desktop
- Tunnel setup to the desktop
- Desktop-specific service checks
- File sync or remote inventory for that machine

Examples:

- Managing the local PC over an approved SSH alias
- Maintaining a desktop host inventory record

## What should never be done from inside the container

- Modify host SSH, Tailscale, Docker, systemd, firewall, or package state
- Restart Hermes/OpenClaw/gateway processes unless explicitly approved
- Generate SSH keys without explicit approval
- Open inbound exposure or change host networking policy
- Assume container-local state applies to the AWS host

## Boundary rule

If a change affects the machine globally or persists outside the control-plane workspace, it is outside the safe user-space boundary and requires explicit approval at the correct layer.
