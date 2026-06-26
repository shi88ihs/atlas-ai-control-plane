# Atlas Core

Atlas Core is the central coordination module for the Atlas Control Plane. It is responsible for orchestrating control plane commands, maintaining centralized configuration, and tracking the state of all available platform capabilities.

## Purpose

The primary responsibilities of Atlas Core are:
1. **Module Registry**: Maintain a list of all active and planned control plane modules, abstracting their capabilities.
2. **Central Configuration**: Provide a unified configuration object (`AtlasConfig`) so future modules do not rely on scattered, hardcoded paths.
3. **Command Coordination**: Act as the single source of truth for available commands via the `control-plane` CLI.

## Module Architecture

Every module integrated into the Atlas Control Plane must register with the `ModuleRegistry` in `atlas/core.py`. 

The core data structure requires:
- `name`: Module identity
- `version`: Module version
- `description`: Human-readable purpose
- `available_commands`: CLI commands exposed by the module
- `health_status`: Current runtime health
- `dependencies`: Inter-module dependencies
- `status`: Lifecycle stage (e.g., `Loaded`, `Planned`)

## Future Expansion Model

As new capabilities (such as Fleet Management or the Event Timeline) are built, they will be registered in `atlas/core.py`. Modules will utilize the `AtlasConfig` for standard directory resolution, ensuring the control plane remains organized, portable, and cleanly structured across future nodes.
