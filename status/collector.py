#!/usr/bin/env python3
"""Read-only status collection for the control plane.

Collects structured JSON only. No service restarts, no configuration changes,
and no remote connections.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import socket
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path("/opt/data/home/control-plane")
REPORTS_DIR = ROOT / "reports"
HERMES_SERVICE = "hermes-gateway.service"
OPENCLAW_SERVICE = "openclaw-gateway.service"
SCHEMA_VERSION = "1.0"

SEVERITY_ORDER = {"info": 0, "warning": 1, "critical": 2, "unknown": -1}


@dataclass(frozen=True)
class ProbeResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def run_command(args: list[str], timeout: int = 5) -> ProbeResult:
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return ProbeResult(completed.returncode, completed.stdout.strip(), completed.stderr.strip(), False)
    except FileNotFoundError as exc:
        return ProbeResult(127, "", str(exc), False)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.strip() if isinstance(exc.stdout, str) and exc.stdout else ""
        stderr = exc.stderr.strip() if isinstance(exc.stderr, str) and exc.stderr else "timeout"
        return ProbeResult(124, stdout, stderr, True)


def read_proc_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def parse_kv_lines(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def human_seconds(seconds: float) -> str:
    total = max(0, int(seconds))
    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    parts: list[str] = []
    if days:
        parts.append(f"{days}d")
    if hours or parts:
        parts.append(f"{hours}h")
    if minutes or parts:
        parts.append(f"{minutes}m")
    if not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)


def memory_snapshot() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in read_proc_file("/proc/meminfo").splitlines():
        parts = line.split(":", 1)
        if len(parts) != 2:
            continue
        key, raw = parts[0].strip(), parts[1].strip()
        number = raw.split()[0] if raw else "0"
        try:
            values[key] = int(number) * 1024
        except ValueError:
            values[key] = 0
    return values


def percent(used: float, total: float) -> int:
    if total <= 0:
        return 0
    return int(round((used / total) * 100))


def record(component: str, status: str, severity: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "component": component,
        "status": status,
        "severity": severity,
        "message": message,
        "details": details or {},
        "timestamp": iso_now(),
    }


def service_probe(service: str) -> dict[str, Any]:
    probe = run_command(
        [
            "systemctl",
            "--user",
            "show",
            service,
            "-p",
            "LoadState",
            "-p",
            "ActiveState",
            "-p",
            "SubState",
            "-p",
            "UnitFileState",
            "-p",
            "FragmentPath",
            "-p",
            "MainPID",
            "-p",
            "ExecMainStatus",
        ]
    )
    details = parse_kv_lines(probe.stdout)
    details.update({
        "exit_code": probe.returncode,
        "timed_out": probe.timed_out,
        "stderr": probe.stderr,
    })
    load_state = details.get("LoadState", "unknown")
    active_state = details.get("ActiveState", "unknown")
    unit_state = details.get("UnitFileState", "unknown")
    if load_state == "not-found":
        return record(
            component=service,
            status="missing",
            severity="warning",
            message="systemd unit is not installed on this host",
            details=details,
        )
    if active_state == "active":
        return record(
            component=service,
            status="running",
            severity="info",
            message="systemd service is active",
            details=details,
        )
    if active_state in {"inactive", "failed", "activating", "deactivating"}:
        severity = "warning" if active_state == "inactive" else "critical"
        return record(
            component=service,
            status=active_state,
            severity=severity,
            message=f"systemd service is {active_state}",
            details=details,
        )
    return record(
        component=service,
        status=unit_state if unit_state != "unknown" else active_state,
        severity="unknown",
        message="systemd service state could not be determined",
        details=details,
    )


def collect_hermes_gateway() -> dict[str, Any]:
    probe = service_probe(HERMES_SERVICE)
    probe["component"] = "Hermes Gateway"
    if probe["status"] == "running":
        probe["message"] = "Hermes gateway runtime is active"
    elif probe["status"] == "missing":
        probe["message"] = "Hermes gateway unit is unavailable"
    return probe


def collect_openclaw() -> dict[str, Any]:
    probe = service_probe(OPENCLAW_SERVICE)
    probe["component"] = "OpenClaw"
    if probe["status"] == "running":
        probe["message"] = "OpenClaw runtime is active"
    elif probe["status"] == "missing":
        probe["message"] = "OpenClaw gateway unit is not present on this host"
    return probe


def collect_systemd_gateway_service() -> dict[str, Any]:
    probe = service_probe(HERMES_SERVICE)
    probe["component"] = "systemd gateway service"
    if probe["status"] == "running":
        probe["message"] = "Canonical gateway service is enabled and active"
    return probe


def collect_disk_usage() -> dict[str, Any]:
    target = str(ROOT)
    probe = run_command(["df", "-P", target])
    details: dict[str, Any] = {"target": target, "exit_code": probe.returncode, "stderr": probe.stderr, "timed_out": probe.timed_out}
    lines = [line for line in probe.stdout.splitlines() if line.strip()]
    if len(lines) >= 2:
        columns = lines[1].split()
        if len(columns) >= 6:
            filesystem, blocks, used, available, capacity, mountpoint = columns[:6]
            details.update(
                {
                    "filesystem": filesystem,
                    "size_bytes": int(blocks) * 1024,
                    "used_bytes": int(used) * 1024,
                    "available_bytes": int(available) * 1024,
                    "used_percent": int(capacity.rstrip("%")),
                    "mountpoint": mountpoint,
                }
            )
    used_percent = details.get("used_percent", 0)
    severity = "info" if used_percent < 80 else "warning" if used_percent < 90 else "critical"
    status = f"{used_percent}%"
    return record(
        component="Disk usage",
        status=status,
        severity=severity,
        message=f"{used_percent}% used on {target}",
        details=details,
    )


def collect_memory() -> dict[str, Any]:
    mem = memory_snapshot()
    total = mem.get("MemTotal", 0)
    available = mem.get("MemAvailable", 0)
    used = max(0, total - available)
    used_percent = percent(used, total)
    severity = "info" if used_percent < 80 else "warning" if used_percent < 90 else "critical"
    return record(
        component="Memory",
        status=f"{used_percent}%",
        severity=severity,
        message=f"{used_percent}% memory used",
        details={
            "total_bytes": total,
            "available_bytes": available,
            "used_bytes": used,
            "used_percent": used_percent,
        },
    )


def collect_swap() -> dict[str, Any]:
    mem = memory_snapshot()
    total = mem.get("SwapTotal", 0)
    free = mem.get("SwapFree", 0)
    used = max(0, total - free)
    used_percent = percent(used, total) if total else 0
    severity = "info" if used_percent < 50 else "warning" if used_percent < 80 else "critical"
    return record(
        component="Swap",
        status=f"{used_percent}%",
        severity=severity,
        message=f"{used_percent}% swap used",
        details={
            "total_bytes": total,
            "free_bytes": free,
            "used_bytes": used,
            "used_percent": used_percent,
        },
    )


def collect_docker_availability() -> dict[str, Any]:
    docker = shutil.which("docker")
    if not docker:
        return record(
            component="Docker availability",
            status="unavailable",
            severity="warning",
            message="docker CLI is not installed",
            details={"binary": None},
        )
    probe = run_command([docker, "version", "--format", "{{.Server.Version}}"], timeout=10)
    details = {"binary": docker, "exit_code": probe.returncode, "stderr": probe.stderr, "timed_out": probe.timed_out}
    if probe.returncode == 0 and probe.stdout:
        details["server_version"] = probe.stdout
        return record(
            component="Docker availability",
            status="available",
            severity="info",
            message="docker CLI and daemon are available",
            details=details,
        )
    return record(
        component="Docker availability",
        status="unavailable",
        severity="warning",
        message="docker CLI is present but the daemon was not reachable",
        details=details,
    )


def collect_docker_container_count() -> dict[str, Any]:
    docker = shutil.which("docker")
    if not docker:
        return record(
            component="Docker container count",
            status="unknown",
            severity="unknown",
            message="docker CLI is unavailable",
            details={"binary": None},
        )
    probe = run_command([docker, "ps", "-aq"], timeout=10)
    details = {"binary": docker, "exit_code": probe.returncode, "stderr": probe.stderr, "timed_out": probe.timed_out}
    if probe.returncode == 0:
        count = len([line for line in probe.stdout.splitlines() if line.strip()])
        return record(
            component="Docker container count",
            status=str(count),
            severity="info" if count == 0 else "warning" if count > 0 else "info",
            message=f"{count} container(s) visible to the daemon",
            details={**details, "count": count},
        )
    return record(
        component="Docker container count",
        status="unknown",
        severity="unknown",
        message="docker daemon could not be queried for container count",
        details=details,
    )


def collect_ssh_client_availability() -> dict[str, Any]:
    ssh = shutil.which("ssh")
    if ssh:
        probe = run_command([ssh, "-V"], timeout=5)
        details = {"binary": ssh, "exit_code": probe.returncode, "stderr": probe.stderr, "timed_out": probe.timed_out}
        version = probe.stderr or probe.stdout
        if version:
            details["version"] = version
        return record(
            component="SSH client availability",
            status="available",
            severity="info",
            message="ssh client is available",
            details=details,
        )
    return record(
        component="SSH client availability",
        status="unavailable",
        severity="warning",
        message="ssh client is not installed",
        details={"binary": None},
    )


def collect_tailscale_availability() -> dict[str, Any]:
    tailscale = shutil.which("tailscale")
    if not tailscale:
        return record(
            component="Tailscale availability",
            status="unavailable",
            severity="warning",
            message="tailscale CLI is not installed",
            details={"binary": None},
        )
    probe = run_command([tailscale, "status", "--json"], timeout=10)
    details = {"binary": tailscale, "exit_code": probe.returncode, "stderr": probe.stderr, "timed_out": probe.timed_out}
    if probe.returncode == 0 and probe.stdout:
        try:
            payload = json.loads(probe.stdout)
            details["backend_state"] = payload.get("BackendState")
            self_state = payload.get("Self") or {}
            details["self_host_name"] = self_state.get("HostName")
            details["self_tailnet_ip"] = self_state.get("TailscaleIPs", [None])[0]
            backend_state = str(payload.get("BackendState", "unknown")).lower()
            if backend_state == "running":
                return record(
                    component="Tailscale availability",
                    status="available",
                    severity="info",
                    message="tailscale daemon is running",
                    details=details,
                )
            return record(
                component="Tailscale availability",
                status=backend_state or "unknown",
                severity="warning",
                message="tailscale is installed but not fully connected",
                details=details,
            )
        except json.JSONDecodeError:
            details["raw_output"] = probe.stdout
    return record(
        component="Tailscale availability",
        status="unavailable",
        severity="warning",
        message="tailscale daemon could not be queried",
        details=details,
    )


def collect_hostname() -> dict[str, Any]:
    hostname = socket.gethostname()
    return record(
        component="Hostname",
        status="available",
        severity="info",
        message=hostname,
        details={"hostname": hostname},
    )


def collect_kernel() -> dict[str, Any]:
    kernel = platform.release()
    return record(
        component="Kernel",
        status="available",
        severity="info",
        message=kernel,
        details={"kernel": kernel},
    )


def collect_operating_system() -> dict[str, Any]:
    os_release = read_proc_file("/etc/os-release")
    details = parse_kv_lines(os_release)
    pretty = details.get("PRETTY_NAME") or f"{details.get('NAME', 'Unknown')} {details.get('VERSION_ID', '')}".strip()
    return record(
        component="Operating system",
        status="available",
        severity="info",
        message=pretty,
        details=details,
    )


def collect_current_user() -> dict[str, Any]:
    user = os.getenv("USER") or os.getenv("LOGNAME") or os.getenv("USERNAME") or "unknown"
    return record(
        component="Current user",
        status="available",
        severity="info",
        message=user,
        details={"user": user},
    )


def collect_current_uptime() -> dict[str, Any]:
    uptime_text = read_proc_file("/proc/uptime")
    seconds = 0.0
    if uptime_text:
        try:
            seconds = float(uptime_text.split()[0])
        except (ValueError, IndexError):
            seconds = 0.0
    return record(
        component="Current uptime",
        status="available",
        severity="info",
        message=human_seconds(seconds),
        details={"uptime_seconds": int(seconds), "uptime_human": human_seconds(seconds)},
    )


def collect_current_load_average() -> dict[str, Any]:
    loadavg = read_proc_file("/proc/loadavg")
    values: list[float] = []
    if loadavg:
        try:
            values = [float(part) for part in loadavg.split()[:3]]
        except ValueError:
            values = []
    return record(
        component="Current load average",
        status="available",
        severity="info",
        message=", ".join(f"{value:.2f}" for value in values) if values else "unavailable",
        details={"load_average": values},
    )


def collect_current_timestamp() -> dict[str, Any]:
    timestamp = iso_now()
    return record(
        component="Current timestamp",
        status="available",
        severity="info",
        message=timestamp,
        details={"timestamp": timestamp},
    )


def collect_status() -> dict[str, Any]:
    from doctor.collector import collect_doctor_checks

    doctor_report = collect_doctor_checks()
    components = [
        collect_hermes_gateway(),
        collect_openclaw(),
        collect_systemd_gateway_service(),
        collect_disk_usage(),
        collect_memory(),
        collect_swap(),
        collect_docker_availability(),
        collect_docker_container_count(),
        collect_ssh_client_availability(),
        collect_tailscale_availability(),
        collect_hostname(),
        collect_kernel(),
        collect_operating_system(),
        collect_current_user(),
        collect_current_uptime(),
        collect_current_load_average(),
        collect_current_timestamp(),
        *doctor_report.get("components", []),
    ]

    overall = overall_status(components)
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "host": {
            "hostname": socket.gethostname(),
            "kernel": platform.release(),
            "operating_system": collect_operating_system()["message"],
            "current_user": os.getenv("USER") or os.getenv("LOGNAME") or os.getenv("USERNAME") or "unknown",
            "uptime": collect_current_uptime()["details"],
            "load_average": collect_current_load_average()["details"],
        },
        "overall": overall,
        "components": components,
    }


def overall_status(components: list[dict[str, Any]]) -> dict[str, Any]:
    severity_rank = max((SEVERITY_ORDER.get(component.get("severity", "unknown"), -1) for component in components), default=-1)
    if severity_rank >= 2:
        status = "fail"
        severity = "critical"
        message = "One or more critical issues require attention"
    elif severity_rank >= 1:
        status = "degraded"
        severity = "warning"
        message = "Some subsystems need attention"
    else:
        status = "healthy"
        severity = "info"
        message = "All collected subsystems are in good shape"
    return record(
        component="Overall",
        status=status,
        severity=severity,
        message=message,
        details={"component_count": len(components)},
    )


def main() -> int:
    report = collect_status()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
