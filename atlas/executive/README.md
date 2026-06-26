# Atlas Executive

Atlas Executive is the bridge between the Atlas Planner and the eventual physical execution layer. 

## Purpose
While the Planner establishes *what* needs to happen (the `ExecutionPlan`), the Executive establishes exactly *how* it will be orchestrated step-by-step (the `Workflow`).

Crucially, **the Executive does not run commands**. It translates a high-level plan into a rigorous workflow blueprint that dictates prerequisites, approvals, and rollback paths for each individual step.

## Lifecycle
1. **Planner**: Analyzes intent and issues an `ExecutionPlan`.
2. **Executive**: Translates the `ExecutionPlan` into a sequenced `Workflow`.
3. **Approval**: Determines if human (or programmatic) intervention is required before proceeding.
4. **Executor (Future)**: Will consume the `Workflow` to physically drive modules.

## Workflow Tracking
Every time a `Workflow` is generated, its metadata (intent, risk, modules, and execution state) is committed to the workflow history module (`logs/workflow_history.json`). This ensures full auditability of intended actions even before they execute.

## Future Autonomous Execution
The structured dataclasses within the Executive (`Workflow`, `WorkflowStep`) are designed to serialize perfectly. This guarantees that future autonomous executors (like OpenClaw or an event loop) can blindly ingest and execute workflows programmatically.
