from typing import Dict, Any

def render_section(title: str, items: Dict[str, str]) -> str:
    lines = [f"=== {title.upper()} ==="]
    for k, v in items.items():
        label = k.replace("_", " ").title()
        lines.append(f"{label:<20}: {v}")
    lines.append("")
    return "\n".join(lines)

def build_dashboard(
    header: Dict[str, str],
    health: Dict[str, str],
    runtimes: Dict[str, str],
    git: Dict[str, str],
    planner: Dict[str, str],
    simulator: Dict[str, str],
    snapshot: Dict[str, str],
    history: Dict[str, str]
) -> str:
    
    out = []
    out.append("================================================================================")
    out.append(f"                      ATLAS MISSION CONTROL {header['version']}                      ")
    out.append("================================================================================\n")
    
    # Header
    out.append(f"Hostname: {header['hostname']} | User: {header['user']}")
    out.append(f"Git Tag: {header['git_tag']} | Branch: {header['git_branch']}\n")
    
    out.append(render_section("Health", health))
    out.append(render_section("Runtimes", runtimes))
    out.append(render_section("Git", git))
    out.append(render_section("Planner", planner))
    out.append(render_section("Simulator", simulator))
    out.append(render_section("Snapshot", snapshot))
    out.append(render_section("History", history))
    
    out.append("================================================================================")
    out.append("Use 'control-plane help' to view available commands.")
    out.append("================================================================================")
    
    return "\n".join(out)
