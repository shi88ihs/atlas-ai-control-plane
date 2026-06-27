"""Shared helpers for read-only control-plane doctor checks."""

from __future__ import annotations

import os
import shlex
import subprocess
import getpass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path("/opt/data/home/control-plane")
DEFAULT_HOME = Path.home()
GATEWAY_SERVICE = "hermes-gateway.service"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def record(
    component: str,
    status: str,
    severity: str,
    message: str,
    details: dict[str, Any] | None = None,
    *,
    confidence: str | None = None,
    reasoning: str | None = None,
    evidence_timestamp: str | None = None,
    last_checked: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "component": component,
        "status": status,
        "severity": severity,
        "message": message,
        "details": details or {},
        "timestamp": iso_now(),
    }
    if confidence is not None:
        payload["confidence"] = confidence
    if reasoning is not None:
        payload["reasoning"] = reasoning
    if evidence_timestamp is not None:
        payload["evidence_timestamp"] = evidence_timestamp
    if last_checked is not None:
        payload["last_checked"] = last_checked
    return payload


def run_command(
    args: list[str],
    timeout: int = 15,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=env,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def truncate(text: str, limit: int = 280) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def _systemctl_show(service: str, properties: list[str]) -> dict[str, str]:
    systemctl = os.environ.get("SYSTEMCTL") or "systemctl"
    args = [systemctl, "--user", "show", service]
    for prop in properties:
        args.extend(["-p", prop])
    proc = run_command(args, timeout=10)
    if proc is None or proc.returncode != 0:
        return {}
    values: dict[str, str] = {}
    for line in proc.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _parse_environment(value: str) -> dict[str, str]:
    if not value:
        return {}
    raw = value
    if raw.startswith("Environment="):
        raw = raw[len("Environment=") :]
    env: dict[str, str] = {}
    try:
        parts = shlex.split(raw)
    except ValueError:
        parts = raw.split()
    for item in parts:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        env[key] = value
    return env


def gateway_service_context(service: str = GATEWAY_SERVICE) -> dict[str, Any]:
    data = _systemctl_show(
        service,
        [
            "ActiveState",
            "SubState",
            "MainPID",
            "ActiveEnterTimestamp",
            "ActiveEnterTimestampMonotonic",
            "User",
            "FragmentPath",
            "Environment",
        ],
    )
    environment = _parse_environment(data.get("Environment", ""))
    home = environment.get("HOME") or str(DEFAULT_HOME)
    user = environment.get("USER") or environment.get("LOGNAME") or getpass.getuser()
    logname = environment.get("LOGNAME") or user
    hermes_home = environment.get("HERMES_HOME") or str(Path(home) / ".hermes")
    path = environment.get("PATH") or os.environ.get("PATH") or "/usr/bin:/bin"
    return {
        "service": service,
        "active_state": data.get("ActiveState", "unknown"),
        "sub_state": data.get("SubState", "unknown"),
        "main_pid": int(data.get("MainPID", "0") or 0),
        "active_enter_timestamp": data.get("ActiveEnterTimestamp", ""),
        "active_enter_timestamp_monotonic": data.get("ActiveEnterTimestampMonotonic", ""),
        "service_user": data.get("User", ""),
        "fragment_path": data.get("FragmentPath", ""),
        "environment": environment,
        "home": home,
        "user": user,
        "logname": logname,
        "hermes_home": hermes_home,
        "path": path,
    }


def service_env_for_gateway(service: str = GATEWAY_SERVICE) -> dict[str, str]:
    context = gateway_service_context(service)
    env = dict(context.get("environment", {}))
    env.update(
        {
            "HOME": context["home"],
            "USER": context["user"],
            "LOGNAME": context["logname"],
            "HERMES_HOME": context["hermes_home"],
            "PATH": context["path"],
            "XDG_CONFIG_HOME": str(Path(context["home"]) / ".config"),
            "CLOUDSDK_CONFIG": str(Path(context["home"]) / ".config" / "gcloud"),
        }
    )
    return env


def gateway_restart_timestamp(service: str = GATEWAY_SERVICE) -> str:
    context = gateway_service_context(service)
    return context.get("active_enter_timestamp", "")


def gateway_service_running(service: str = GATEWAY_SERVICE) -> bool:
    context = gateway_service_context(service)
    return context.get("active_state") == "active"
