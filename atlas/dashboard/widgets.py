import os
import json
import getpass
import subprocess
from pathlib import Path
from typing import Dict, Any

from atlas.config import config

def _run_cmd(cmd: list) -> str:
    try:
        res = subprocess.run(cmd, cwd=str(config.root_dir), capture_output=True, text=True, timeout=5)
        return res.stdout.strip()
    except Exception:
        return ""

def get_header_data() -> Dict[str, str]:
    tag = _run_cmd(["git", "describe", "--tags", "--abbrev=0"])
    branch = _run_cmd(["git", "branch", "--show-current"])
    return {
        "version": "v0.9",
        "hostname": os.uname().nodename,
        "user": getpass.getuser(),
        "git_tag": tag or "None",
        "git_branch": branch or "None"
    }

def get_health_data() -> Dict[str, str]:
    # Placeholder summaries that instruct the user to use the tools or parse last report
    # In a full integration, these would read from a live local cache.
    latest_report = config.reports_dir / "latest-health-report.md"
    summary = "Unknown"
    if latest_report.exists():
        content = latest_report.read_text()
        if "PASS" in content:
            summary = "PASS"
        elif "FAIL" in content:
            summary = "FAIL"
        else:
            summary = "Available"
            
    return {
        "doctor_summary": "Ready",
        "status_summary": f"Latest Report: {summary}",
        "auth_summary": "ADC Configured"
    }

def get_runtimes_data() -> Dict[str, str]:
    hermes_status = _run_cmd(["systemctl", "--user", "is-active", "hermes-gateway"])
    return {
        "hermes": hermes_status or "unknown",
        "openclaw": "Offline / Unmanaged",
        "future": "Planned"
    }

def get_git_data() -> Dict[str, str]:
    status_out = _run_cmd(["git", "status", "--porcelain"])
    last_commit = _run_cmd(["git", "log", "-1", "--format=%h - %s"])
    tag = _run_cmd(["git", "describe", "--tags", "--abbrev=0"])
    
    cleanliness = "Clean" if not status_out else f"Modified ({len(status_out.splitlines())} files)"
    
    return {
        "working_tree": cleanliness,
        "latest_commit": last_commit or "None",
        "latest_tag": tag or "None"
    }

def get_planner_data() -> Dict[str, str]:
    history_file = config.root_dir / "logs" / "workflow_history.json"
    wf_count = 0
    last_wf = "None"
    if history_file.exists():
        try:
            with open(history_file, "r") as f:
                data = json.load(f)
                wf_count = len(data)
                if wf_count > 0:
                    last = data[-1]
                    last_wf = f"{last.get('workflow_id', 'Unknown')} ({last.get('intent', 'Unknown')})"
        except Exception:
            pass
            
    return {
        "last_workflow": last_wf,
        "workflow_count": str(wf_count)
    }

def get_simulator_data() -> Dict[str, str]:
    sim_files = list(config.reports_dir.glob("simulation-*.md"))
    sim_count = len(sim_files)
    last_sim = "None"
    if sim_count > 0:
        latest = max(sim_files, key=os.path.getmtime)
        last_sim = latest.name
        
    return {
        "last_simulation": last_sim,
        "simulation_count": str(sim_count)
    }

def get_snapshot_data() -> Dict[str, str]:
    snapshots_dir = config.root_dir / "backups"
    if not snapshots_dir.exists():
        return {"latest_snapshot": "None", "timestamp": "N/A"}
        
    snaps = list(snapshots_dir.glob("*.tar.gz"))
    if not snaps:
        return {"latest_snapshot": "None", "timestamp": "N/A"}
        
    latest = max(snaps, key=os.path.getmtime)
    return {
        "latest_snapshot": latest.name,
        "timestamp": str(int(os.path.getmtime(latest)))
    }

def get_history_data() -> Dict[str, str]:
    reports = list(config.reports_dir.glob("*.md"))
    if not reports:
        return {"recent_activity": "None", "recent_reports": "None"}
        
    reports.sort(key=os.path.getmtime, reverse=True)
    recent = reports[:3]
    recent_names = ", ".join(r.name for r in recent)
    
    return {
        "recent_activity": f"{len(reports)} total reports tracked.",
        "recent_reports": recent_names
    }
