# Atlas AI Control Plane Status Engine
 
 The status engine is the first reusable Atlas AI Control Plane status layer.
It is intentionally read-only and split into three parts:

- **Collector** — gathers structured state
- **Markdown renderer** — writes the canonical report file
- **Terminal renderer** — prints a compact status summary

## Files

- `collector.py`
  - gathers read-only runtime data
  - returns structured JSON
- `renderer_markdown.py`
  - renders the collected status into markdown
  - writes `/opt/data/home/control-plane/reports/latest-health-report.md`
  - also writes a timestamped copy in `/opt/data/home/control-plane/reports/`
- `renderer_terminal.py`
  - renders compact terminal output suitable for `control-plane status`
- `schema.json`
  - stable JSON schema for component records

## Supported collectors

Initial collectors cover:

- Hermes Gateway
- OpenClaw
- systemd gateway service
- Disk usage
- Memory
- Swap
- Docker availability
- Docker container count
- SSH client availability
- Tailscale availability
- Hostname
- Kernel
- Operating system
- Current user
- Current uptime
- Current load average
- Current timestamp
- Google ADC
- Vertex AI
- Telegram

## Wrapper scripts

These wrappers live in `/opt/data/home/control-plane/scripts/`:

- `control-plane` → CLI wrapper for status/collect/report/doctor/help
- `collect` → JSON collection
- `status` → terminal rendering
- `report` → markdown rendering and report file write

## Read-only rules

The engine must not:

- restart services
- modify SSH
- modify systemd
- modify Docker
- change networking
- connect to remote hosts
- install packages

## Design goal

The collector must stay independent from presentation so future integrations can reuse the same data for terminal, markdown, Telegram, and dashboard outputs.
