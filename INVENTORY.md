# Inventory

## Current machine
- Hostname: `ip-172-31-0-144.ap-southeast-2.compute.internal`
- Runtime user: `ec2-user`
- Operating system: Amazon Linux 2023
- Kernel: `6.1.174-217.345.amzn2023.x86_64`
- Architecture: `x86_64`
- Init system: systemd
- Working directory during discovery: `/home/ec2-user`

## Runtime
- Canonical Hermes runtime: systemd-managed user service
- Canonical service name: `hermes-gateway.service`
- Service file: `/home/ec2-user/.config/systemd/user/hermes-gateway.service`
- Current runtime state: active and running
- Deployment model: local AWS host runtime, not Docker-canonical

## Hermes
- Installation: `/home/ec2-user/hermes-agent`
- Configuration home: `/home/ec2-user/.hermes`
- Gateway logs: `~/.hermes/logs/gateway.log`
- Control plane workspace: `/opt/data/home/control-plane`
- Reports directory: `/opt/data/home/control-plane/reports`

## OpenClaw
- OpenClaw is operationally adjacent but separate from Hermes.
- Do not assume OpenClaw and Hermes share the same service owner, process tree, or runtime contract.
- Any future OpenClaw inventory should record its own canonical service, config, and restart path.

## Future managed machines
- Desktop onboarding targets should be recorded here once approved.
- Each managed machine should include at minimum:
  - hostname
  - friendly name
  - role
  - transport
  - approval level
  - operating system
  - tailscale presence
  - SSH readiness
  - notes
- Initial future categories:
  - local desktop or laptop fleet nodes
  - dedicated admin bastions
  - additional runtime hosts used for Hermes or adjacent automation
