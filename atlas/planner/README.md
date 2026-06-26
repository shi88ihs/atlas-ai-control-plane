# Atlas Planner

Atlas Planner is the orchestration layer of the Atlas Control Plane. It does not execute actions directly. Instead, it interprets high-level objectives (Intents) and resolves them into structured, actionable blueprints (Execution Plans).

## Intent Model

An **Intent** represents a high-level operational goal. Supported intents include:
- `status`
- `doctor`
- `backup`
- `report`
- `git`
- `inventory`
- `health`
- `stabilize`
- `diagnose`
- `release`

## Planning Model

The planner outputs a deterministic **Execution Plan** based on the declared intent. An Execution Plan details:
- **Goal**: What the plan accomplishes.
- **Modules Required**: Which Atlas modules must be loaded.
- **Execution Order**: The exact sequence of operational steps.
- **Estimated Duration**: Expected time to complete.
- **Risk Level**: Operational risk (e.g., Read-only, Low, High).
- **Approval Required**: Whether the plan mandates human oversight before execution.
- **Rollback Strategy**: How to revert the action if an anomaly is detected.

## Future Autonomous Execution

The Atlas Planner is explicitly designed so that future AI agents (e.g., OpenClaw, future autonomous loops) can consume plans programmatically. The planner exposes structured data (via `.to_dict()`) ensuring autonomous controllers can securely evaluate risk, verify approvals, and execute workflows safely.
