# Legacy Container Runtime Deprecation

## Purpose
Safely halt and disable the auto-restart policies of legacy containerized AI runtimes to ensure they do not conflict with the newly established canonical `systemd` daemon.

## Summary
As part of the architecture unification, the redundant Docker-based deployments of the Hermes agent and its dashboard were systematically disabled. This eliminated race conditions over network ports and prevented dual-brain execution anomalies while keeping the container images intact for rollback if needed.

## Architecture
- **Target Engine:** Docker Daemon
- **Target Containers:** `hermes`, `hermes-dashboard`
- **Canonical Replacement:** `hermes-gateway.service`
- **Action:** Halt execution and strip restart policies without destroying data volumes.

## Implementation
1. **Policy Modification:** Executed `docker update --restart no hermes hermes-dashboard` to ensure the containers would not revive upon host reboot or daemon restart.
2. **Graceful Halt:** Executed `docker stop hermes hermes-dashboard` to send SIGTERM and cleanly spin down the redundant processes.
3. **State Verification:** Queried Docker (`docker ps -a`) to confirm the target containers entered the `Exited` state.
4. **Conflict Check:** Verified that no zombie processes remained bound to critical gateway ports (`8090`), successfully releasing the network sockets.

## Outcome
The host environment was successfully stabilized. The canonical systemd service now operates with exclusive ownership of the runtime state, eliminating duplication and simplifying future telemetry collection.

## Lessons Learned
- Modifying restart policies prior to halting containers guarantees that watchdog scripts or system reboots will not unexpectedly resurrect deprecated infrastructure during a migration window.