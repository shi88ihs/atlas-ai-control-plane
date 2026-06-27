# Fleet Architecture Design

## Purpose
Define the structured JSON schema and communication topology for Atlas to coordinate multiple AI deployment environments simultaneously.

## Summary
The fleet design establishes a standard contract for managing remote nodes. By enforcing a strict JSON schema for host inventory, Atlas can programmatically query capabilities, network boundaries, and runtime statuses across disparate cloud instances without requiring bespoke parsing per host.

## Architecture
- **Data Format:** JSON
- **Inventory Path:** `inventory/hosts.json`
- **Topology:** Hub-and-spoke configuration leveraging secure transport overlays (Tailscale).
- **Core Entities:** Hosts, Roles, and Sub-components (Runtimes).

## Implementation
1. **Schema Design:** Developed a structured representation capturing identity (`hostname`, `primary_ip`), transport mechanisms (`ssh`, `tailscale_state`), and specific hardware traits (OS, Architecture).
2. **Role Mapping:** Established logical roles (`control-plane`, `worker`, `database`) to allow future automation to target specific host fleets.
3. **Security Constraints:** Designed the schema specifically to *exclude* secret material (passwords, keys). It exclusively references external credential stores or implicit identity links (e.g., SSH agent).

## Outcome
The finalized fleet design provides a scalable foundation for Atlas. Future CLI extensions and continuous integration scripts can rely on this predictable schema to orchestrate complex updates across an expanding array of nodes.

## Lessons Learned
- Decoupling the host metadata from the operational credentials drastically reduces the risk of secret leakage when pushing infrastructure definitions to public repositories.