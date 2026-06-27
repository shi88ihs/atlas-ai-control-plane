# Inventory

## Current machine
- Hostname: `Atlas runtime`
- Runtime user: `atlas-admin`
- Operating system: Linux server
- Kernel: `redacted`
- Architecture: `x86_64`
- Init system: systemd
- Working directory during discovery: `~`

## Runtime
- Canonical Hermes runtime: systemd-managed user service
- Canonical service name: `hermes-gateway.service`
- Service file: `~/.config/systemd/user/hermes-gateway.service`
- Current runtime state: active and running
- Deployment model: local AWS host runtime, not Docker-canonical

## Hermes
- Installation: `<install-path>/hermes-agent`
- Configuration home: `<config-dir>/.hermes`
- Gateway logs: `~/.hermes/logs/gateway.log`
- Atlas Control Plane workspace: `/opt/data/home/control-plane`
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
