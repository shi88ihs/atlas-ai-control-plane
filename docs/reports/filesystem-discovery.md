# Filesystem Architecture Discovery

## Purpose
Map the file ownership, permissions, and directory structures of the deployment environment to validate the security boundary of the `atlas-admin` user.

## Summary
The filesystem audit confirmed that the Atlas Control Plane and Hermes runtime operate securely within a clearly bounded user-space footprint. The `atlas-admin` user acts as the execution boundary, preventing lateral movement or unauthorized modification of host-level system files.

## Architecture
- **Execution User:** `atlas-admin` (Restricted privileges)
- **Control Plane Root:** `/opt/data/home/control-plane` (Owned by `atlas-admin`)
- **Runtime Root:** `<config-dir>/.hermes`
- **Isolation Strategy:** Native Linux user and group permissions (`chown`/`chmod`).

## Implementation
1. **Home Directory Audit:** Validated the existence and ownership of `~` and verified that the `HOME` environment variable appropriately points to the isolated runtime home directory.
2. **Workspace Verification:** Confirmed that the Atlas Control Plane directory (`/opt/data/home/control-plane`) is correctly chowned to `atlas-admin:atlas-admin`, enabling Git and execution scripts to run without `sudo`.
3. **Immutability Check:** Asserted that sensitive host configurations (e.g., `/etc/systemd/system`) are not writable by the runtime user, strictly enforcing the user-level systemd topology.

## Outcome
The discovery phase proved that the underlying infrastructure adheres to the principle of least privilege. The filesystem hierarchy cleanly segregates the orchestrator's documentation, configuration, and execution layers, reducing the attack surface.

## Lessons Learned
- Validating the divergence between the actual `HOME` variable and the `passwd`-defined home directory is crucial for tools (like Git and SSH) that rely heavily on implicit configuration paths.