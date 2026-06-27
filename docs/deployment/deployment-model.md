# Deployment Model

## The Target Environment
Atlas is designed to be deployed onto robust Linux server environments. It is agnostic to the underlying cloud provider (AWS, GCP, Bare Metal), provided a standard Linux kernel and `systemd` are available.

## Native Execution vs. Containerization
While Atlas can orchestrate Docker containers, the core Atlas Control Plane and primary AI engines (like Hermes) run as native processes managed by a user-level `systemd` instance. 

**Why native?**
Containerizing the core orchestrator creates a "chicken-and-egg" problem when the AI needs to restart the container daemon or manage host-level network states. Running natively provides deeper visibility and reliability without the networking overhead of bridging.

## The Deployment Lifecycle
1. **Provisioning:** A Linux host is provisioned, and the `atlas-admin` user is created.
2. **Overlay Connection:** The host joins the secure overlay network.
3. **Repository Sync:** The Atlas Control Plane repository is cloned into the user-space directory.
4. **Daemon Launch:** `systemctl --user enable --now hermes-gateway` initiates the AI runtime.
5. **Continuous Verification:** The Atlas status engine runs periodically, validating the environment against the known Git baseline.