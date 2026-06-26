"""Telegram gateway authentication health check."""

from __future__ import annotations

import re
import shutil

from .common import (
    gateway_restart_timestamp,
    gateway_service_context,
    gateway_service_running,
    iso_now,
    record,
    run_command,
    truncate,
)

GATEWAY_SERVICE = "hermes-gateway.service"
SUCCESS_PATTERNS = [
    r"telegram.*polling.*started",
    r"telegram.*polling.*resumed",
    r"telegram.*polling.*succeeded",
    r"telegram.*poll.*successful",
    r"telegram.*update.*received",
    r"telegram.*received.*update",
    r"telegram.*update.*processed",
    r"telegram.*handled.*update",
]
AUTH_ERROR_PATTERNS = [
    r"telegram.*401",
    r"telegram.*403",
    r"telegram.*unauth",
    r"telegram.*invalid token",
    r"telegram.*bot token",
    r"telegram.*authenticationerror",
]
FAILURE_PATTERNS = [
    r"telegram.*conflict",
    r"terminated by other getupdates request",
    r"only one bot instance is running",
    r"telegram.*polling.*error",
    r"telegram.*polling.*failed",
]


def _gateway_processes() -> list[dict[str, object]]:
    ps = shutil.which("ps")
    if not ps:
        return []
    proc = run_command([ps, "-eo", "pid=,args="], timeout=10)
    if proc is None or proc.returncode != 0:
        return []

    processes: list[dict[str, object]] = []
    for line in proc.stdout.splitlines():
        raw = line.strip()
        if not raw:
            continue
        parts = raw.split(None, 1)
        if len(parts) != 2:
            continue
        pid_text, cmd = parts
        if "hermes_cli.main gateway run" not in cmd and "hermes gateway run" not in cmd:
            continue
        try:
            pid = int(pid_text)
        except ValueError:
            continue
        processes.append({"pid": pid, "cmd": truncate(cmd, 180)})
    return processes


def _journal_since_restart() -> tuple[str, str]:
    journal = shutil.which("journalctl")
    since = gateway_restart_timestamp()
    if not journal or not since:
        return "", since
    proc = run_command(
        [journal, "--user", "-u", GATEWAY_SERVICE, "--since", since, "--no-pager", "-o", "short-iso"],
        timeout=30,
    )
    if proc is None:
        return "", since
    return proc.stdout or "", since


def _match_any(text: str, patterns: list[str]) -> list[str]:
    matches: list[str] = []
    for line in text.splitlines():
        hay = line.lower()
        for pattern in patterns:
            if re.search(pattern, hay):
                matches.append(truncate(line, 260))
                break
    return matches


def _latest_timestamp(text: str, fallback: str) -> str:
    for line in reversed([line for line in text.splitlines() if line.strip()]):
        token = line.split()[0]
        if token:
            return token
    return fallback


def check() -> dict[str, object]:
    checked_at = iso_now()
    context = gateway_service_context()
    running = gateway_service_running()
    processes = _gateway_processes()
    restart_timestamp = gateway_restart_timestamp()
    log_text, since = _journal_since_restart()
    success_matches = _match_any(log_text, SUCCESS_PATTERNS)
    auth_error_matches = _match_any(log_text, AUTH_ERROR_PATTERNS)
    failure_matches = _match_any(log_text, FAILURE_PATTERNS)

    details: dict[str, object] = {
        "gateway_service": GATEWAY_SERVICE,
        "gateway_running": running,
        "service_user": context.get("user"),
        "service_home": context.get("home"),
        "restart_timestamp": restart_timestamp,
        "log_window_start": since,
        "current_process_count": len(processes),
        "current_processes": processes,
        "recent_successful_polling_activity": bool(success_matches),
        "recent_auth_errors": bool(auth_error_matches),
        "recent_polling_failures": bool(failure_matches),
    }
    if success_matches:
        details["success_evidence"] = success_matches[:3]
    if auth_error_matches:
        details["auth_error_evidence"] = auth_error_matches[:3]
    if failure_matches:
        details["failure_evidence"] = failure_matches[:3]

    evidence_timestamp = _latest_timestamp(log_text, restart_timestamp or checked_at)

    if not running:
        details["recommended_action"] = "Restore the canonical Hermes gateway service before expecting Telegram polling."
        details["estimated_impact"] = "Telegram polling is unavailable while the gateway is not running."
        return record(
            component="Telegram",
            status="fail",
            severity="critical",
            message="Hermes gateway is not running",
            details=details,
            confidence="High",
            reasoning="The canonical gateway service is not active.",
            evidence_timestamp=evidence_timestamp,
            last_checked=checked_at,
        )

    if len(processes) > 1:
        details["duplicate_polling_detected"] = True
        details["recommended_action"] = "Ensure only one Hermes gateway process is running."
        details["estimated_impact"] = "Duplicate pollers can trigger Telegram long-poll conflicts and message loss."
        return record(
            component="Telegram",
            status="fail",
            severity="critical",
            message="Multiple Hermes gateway processes are running",
            details=details,
            confidence="High",
            reasoning="More than one live gateway process was detected in the local process table.",
            evidence_timestamp=evidence_timestamp,
            last_checked=checked_at,
        )

    if auth_error_matches or failure_matches:
        details["duplicate_polling_detected"] = bool(failure_matches)
        details["recommended_action"] = "Investigate the post-restart Telegram polling errors in the live gateway logs."
        details["estimated_impact"] = "Telegram polling may be unavailable until the underlying failure is resolved."
        return record(
            component="Telegram",
            status="fail",
            severity="critical",
            message="Recent Telegram auth or polling failures were detected after the latest restart",
            details=details,
            confidence="High",
            reasoning="The log window was restricted to entries newer than the latest restart and still contains Telegram failures.",
            evidence_timestamp=evidence_timestamp,
            last_checked=checked_at,
        )

    details["duplicate_polling_detected"] = False
    if success_matches:
        return record(
            component="Telegram",
            status="pass",
            severity="info",
            message="Telegram gateway is running and recent polling activity looks healthy",
            details=details,
            confidence="High",
            reasoning="The gateway is active, the log window is post-restart only, and no auth or polling failures were found.",
            evidence_timestamp=evidence_timestamp,
            last_checked=checked_at,
        )

    return record(
        component="Telegram",
        status="pass",
        severity="info",
        message="Telegram gateway is running and no recent authentication or polling failures were found",
        details=details,
        confidence="Medium",
        reasoning="The gateway is active and the post-restart log window does not contain Telegram failures, but no explicit success entry was observed.",
        evidence_timestamp=evidence_timestamp,
        last_checked=checked_at,
    )
