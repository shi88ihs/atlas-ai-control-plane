# Future Fleet Design

## Goal

Create a simple inventory model that can grow across AWS hosts, desktops, laptops, Windows machines, Raspberry Pi devices, and future servers without mixing host identities with operational notes.

## Naming convention

Use lowercase host IDs with a clear role suffix and stable numbering:

- `aws-control-01`
- `desktop-linux-01`
- `laptop-linux-01`
- `windows-01`
- `raspberrypi-01`
- `future-server-01`

Guidance:

- Keep names short and stable
- Avoid spaces
- Use a single canonical ID per machine
- Separate human-friendly labels from machine IDs

## Recommended directory structure

```text
control-plane/
  hosts/
    aws-control-01/
      host.md
      inventory.json
      ssh.md
      network.md
      services.md
      notes.md
    desktop-linux-01/
      host.md
      inventory.json
      ssh.md
      network.md
      notes.md
    laptop-linux-01/
      host.md
      inventory.json
      ssh.md
      network.md
      notes.md
    windows-01/
      host.md
      inventory.json
      ssh.md
      network.md
      notes.md
    raspberrypi-01/
      host.md
      inventory.json
      ssh.md
      network.md
      notes.md
    future-server-01/
      host.md
      inventory.json
      ssh.md
      network.md
      notes.md
  inventory/
    hosts.json
    hosts.csv
    endpoints.json
    services.json
  ssh/
    inventory.md
    config-notes.md
    known-hosts-notes.md
  templates/
    host.md.tpl
    inventory.json.tpl
    report.md.tpl
  sessions/
    2026-06-25/
      phase-4-notes.md
```

## Recommended host metadata fields

Store the following per host:

- `host_id`
- `display_name`
- `role`
- `os`
- `version`
- `architecture`
- `access_methods`
- `primary_ip`
- `secondary_ips`
- `dns_servers`
- `routes`
- `ssh_reachable`
- `tailscale_state`
- `docker_present`
- `service_notes`
- `trust_boundary_notes`

## Example inventory record

```json
{
  "host_id": "aws-control-01",
  "display_name": "AWS Control Host",
  "role": "aws-control",
  "os": "Linux server",
  "architecture": "x86_64",
  "access_methods": ["ssh", "tailscale", "ssm"],
  "primary_ip": "10.0.0.10",
  "ssh_reachable": true,
  "tailscale_state": "active"
}
```

## SSH inventory guidance

Future SSH inventory should live under the control-plane workspace, not in host configuration directories:

- primary inventory: `/opt/data/home/control-plane/ssh/`
- host records: `/opt/data/home/control-plane/hosts/`
- aggregate inventory: `/opt/data/home/control-plane/inventory/`

## Design principles

- Keep secrets out of the inventory tree
- Keep host facts separate from operator notes
- Generate reports from inventory rather than hand-editing everything repeatedly
- Make AWS-host and desktop-management paths explicit so future automation does not confuse them

## Recommended next step

Seed `inventory/hosts.json` and one host profile per machine type, then add a template for generating consistent read-only status reports.
