# Control Plane Bootstrap Report

## Summary
Phase 4 control-plane bootstrap has been documented successfully.
The canonical Hermes runtime is now recorded as the systemd-managed gateway on the AWS host, with the duplicate Docker deployment treated as non-canonical.
This phase remained documentation-only and did not modify SSH, Tailscale, firewall, systemd, packages, or running services.

## Documents created
- `/opt/data/home/control-plane/SYSTEM.md`
- `/opt/data/home/control-plane/INVENTORY.md`
- `/opt/data/home/control-plane/OPERATIONS.md`
- `/opt/data/home/control-plane/ROADMAP.md`
- `/opt/data/home/control-plane/HEALTH.md`

## Remaining gaps
- No structured fleet inventory has been seeded yet.
- No formal SSH client onboarding standard has been documented beyond the initial roadmap entry.
- No daily report automation exists yet.
- No health check runner or automation library has been created yet.
- OpenClaw still needs its own dedicated inventory and operations record if it becomes an active managed surface.

## Recommended Phase 5
- Create the fleet inventory schema and seed the current host.
- Document the client-side SSH setup workflow for managed machines.
- Add a standard health-check report generator.
- Define the daily report cadence and storage path.
- Start the automation library with read-only discovery and verification helpers.
- Add the first desktop onboarding record once a target is approved.
