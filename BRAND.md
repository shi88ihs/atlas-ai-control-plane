# Atlas Control Plane Branding

## Mission
To provide a unified, durable operations platform for managing, diagnosing, and automating AI execution engines and infrastructure fleets.

## Vision
Atlas serves as the single pane of glass and coordination layer. It abstracts away host-level differences and provides structured health monitoring, deployment verification, and read-only diagnostics for managed runtimes.

## Architecture
Atlas Control Plane is the overarching operations platform. It manages individual execution engines rather than being the engine itself. 

The primary managed runtimes are:
- **Hermes**: The canonical AI execution engine.
- **OpenClaw**: An optional AI execution engine.
- **Future managed runtimes**: Additional agents and execution environments seamlessly integrated under Atlas.

## Relationship
- **Atlas**: The control plane (inventory, status, reporting, Git integration, automation).
- **Hermes**: A managed AI runtime living within the Atlas ecosystem.
- **OpenClaw**: A secondary, operationally adjacent AI runtime also managed by Atlas.
