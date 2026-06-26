# Operations

## Approved maintenance workflow
1. Identify the target system, scope, and boundary.
2. Gather read-only evidence first.
3. Record the change intent in the control plane.
4. Make only the minimum approved change.
5. Verify the result with a post-change check.
6. Capture a short report in `/opt/data/home/control-plane/reports/`.
7. Back up any workspace artifact that needs rollback support.

## Incident response workflow
1. Confirm what failed and what is still healthy.
2. Preserve logs and evidence before making changes.
3. Determine whether the issue is Hermes, OpenClaw, transport, or host boundary related.
4. Prefer rollback or isolation over broad remediation.
5. Verify recovery with a read-only health check.
6. Write an incident note and link the evidence.

## Gateway restart workflow
- The canonical restart target is `hermes-gateway.service`.
- Use the documented runtime path, not the retired Docker duplicate.
- Restart workflow should always include:
  - pre-restart evidence
  - the restart action
  - post-restart health verification
  - a short note in the reports directory
- If the runtime is already healthy, do not restart it unnecessarily.

## Docker policy
- Docker is not the canonical Hermes runtime.
- The retired duplicate Docker deployment must not be revived as the primary control path.
- Docker may exist as an observed host capability, but control-plane documentation should treat it as non-canonical for Hermes runtime ownership.
- Any future Docker use must be explicitly documented as a separate boundary with its own ownership and restart rules.

## systemd policy
- systemd is the canonical service manager for the Hermes gateway on this host.
- User-level service ownership is preferred for the gateway runtime.
- This phase does not modify unit files, drop-ins, or service enablement.
- Systemd changes belong to a separate approved maintenance step with explicit verification.

## Future desktop onboarding workflow
1. Add the desktop to inventory.
2. Record the approved transport and access boundary.
3. Document the owner, role, and maintenance expectations.
4. Define logging and backup expectations.
5. Confirm the first health check and the recovery path.
6. Store the completed onboarding record as a report.
