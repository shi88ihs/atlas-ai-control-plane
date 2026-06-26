# Atlas Mission Control Dashboard

Mission Control is the unified landing page and single pane of glass for the Atlas Control Plane (v0.9). It aggregates state across all major architectural pillars without executing mutative actions.

## Rules and Constraints
- **Read-Only**: The dashboard strictly reads local files, logs, and fast CLI commands.
- **No Heavy Execution**: It avoids running deep diagnostic suites at load time, preferring to summarize previously cached states.
- **Default Entry Point**: It is executed automatically when the `control-plane` command is invoked with zero arguments.

## Architecture
- `widgets.py`: Isolated data-gathering functions for each operational sector.
- `layout.py`: Presentation and ASCII layout generation.
- `dashboard.py`: Controller mapping widget data to the layout generator.
