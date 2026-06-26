def get_scenario_impact(intent: str) -> dict:
    """Returns dummy lists of files and services affected based on the intent."""
    scenarios = {
        "doctor": {"files": [], "services": []},
        "stabilize": {"files": ["/opt/data/home/control-plane/reports/latest-health-report.md"], "services": []},
        "release": {"files": ["/opt/data/home/control-plane/logs/workflow_history.json"], "services": []},
        "backup": {"files": ["/opt/data/home/control-plane/backups/snapshot.tar.gz"], "services": []},
        "onboard-desktop": {"files": ["/opt/data/home/control-plane/inventory/hosts.json", "/opt/data/home/control-plane/ssh/config"], "services": ["ssh-agent"]},
        "update-machine": {"files": ["/var/log/dnf.log"], "services": ["systemd-resolved", "docker"]}
    }
    return scenarios.get(intent.lower(), {"files": ["Unknown"], "services": ["Unknown"]})
