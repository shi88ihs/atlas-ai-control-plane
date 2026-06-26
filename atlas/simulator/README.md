# Atlas Simulator

The Atlas Simulator sits atop the Atlas Planner and Atlas Executive. It provides a crucial safety layer by performing "dry runs" of workflows before any physical execution occurs.

## Purpose
- **Predictive Impact**: Foresees which modules, files, and services will be touched based on predetermined operational models (`scenarios.py`).
- **Risk Evaluation**: Visibly surfaces risk levels, approval requirements, and rollback strategies prior to action.
- **Reporting**: Automatically generates `latest-simulation-report.md` alongside a timestamped archive mapping the intent and its hypothetical consequence.

## Behavior
The simulator inherently performs **no real actions**. It merely orchestrates the `ExecutionPlan` and `Workflow` representations to model what *would* happen in an active execution scenario.

## Usage
`control-plane simulate <intent>`

Future execution layers (like Atlas Executor) will explicitly rely on simulator checkpoints for automated gating.
