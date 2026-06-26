# Atlas Control Plane AWS Server Roadmap

The following objectives outline the planned evolution of the AWS server hosting the Atlas Control Plane and Hermes/OpenClaw runtimes.

## Core Platform Objectives
- **Atlas Simulator**: Safe impact prediction before physical execution. (Current phase)
- **Atlas Executor**: Controlled, programmatic workflow execution following planner/executive/simulator gates.
- **Snapshot command**: Point-in-time state capture of config, workspaces, and logs.
- **Timeline module**: Immutable sequence of operational events across the environment.

## Fleet and Discovery
- **Fleet inventory**: Structured mapping of all machines, virtual and physical.
- **Desktop onboarding**: Safely attaching external endpoints via Tailscale and SSH integrations.

## Monitoring and Reporting
- **Automated daily health reports**: Unattended execution of `doctor` and `status` intents pushed to tracking channels.
- **Telegram `/status` integration**: Webhook/polling response providing near-time state output over Telegram.
- **Backup verification**: Checksum validation and consistency auditing for generated snapshots.
- **AUR/package security auditor**: Recurring system-level package discrepancy checks.
