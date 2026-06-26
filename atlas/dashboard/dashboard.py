from atlas.dashboard.widgets import (
    get_header_data,
    get_health_data,
    get_runtimes_data,
    get_git_data,
    get_planner_data,
    get_simulator_data,
    get_snapshot_data,
    get_history_data
)
from atlas.dashboard.layout import build_dashboard

def render_dashboard() -> None:
    header = get_header_data()
    health = get_health_data()
    runtimes = get_runtimes_data()
    git = get_git_data()
    planner = get_planner_data()
    simulator = get_simulator_data()
    snapshot = get_snapshot_data()
    history = get_history_data()
    
    dashboard_text = build_dashboard(
        header=header,
        health=health,
        runtimes=runtimes,
        git=git,
        planner=planner,
        simulator=simulator,
        snapshot=snapshot,
        history=history
    )
    
    print(dashboard_text)
