#!/usr/bin/env python3
"""Terminal renderer for control-plane status output."""

from __future__ import annotations

from typing import Any

from .collector import collect_status

STATUS_SYMBOLS = {
    "info": "✓",
    "warning": "⚠",
    "critical": "✖",
    "unknown": "?",
}

OVERALL_SYMBOLS = {
    "healthy": "🟢 HEALTHY",
    "degraded": "🟠 DEGRADED",
    "fail": "🔴 FAIL",
}


def compact_summary(component: dict[str, Any]) -> str:
    details = component.get("details") or {}
    status = str(component.get("status", ""))
    message = str(component.get("message", ""))

    if component.get("component") in {"Disk usage", "Memory", "Swap"} and "used_percent" in details:
        return f"{details['used_percent']}%"
    if component.get("component") == "Docker container count" and status.isdigit():
        count = int(status)
        return f"{count} container(s)"
    if component.get("component") == "Current load average" and message != "unavailable":
        return message
    if component.get("component") == "Current uptime":
        return message
    if component.get("component") in {"Hostname", "Kernel", "Operating system", "Current user", "Current timestamp"}:
        return message
    return message or status


def render_terminal(report: dict[str, Any]) -> str:
    components = report.get("components", [])
    width = max([len(str(component.get("component", ""))) for component in components] + [18])
    lines: list[str] = []
    host = report.get("host", {})
    lines.append(f"Host             {host.get('hostname', 'unknown')}")
    lines.append(f"Generated        {report.get('generated_at', 'unknown')}")
    lines.append("")

    for component in components:
        name = str(component.get("component", ""))
        severity = str(component.get("severity", "unknown"))
        symbol = STATUS_SYMBOLS.get(severity, "?")
        summary = compact_summary(component)
        lines.append(f"{name:<{width}} {symbol} {summary}")
        metadata_bits = []
        for label, key in [("Confidence", "confidence"), ("Reasoning", "reasoning"), ("Evidence", "evidence_timestamp"), ("Last checked", "last_checked")]:
            value = component.get(key)
            if value:
                metadata_bits.append(f"{label}: {value}")
        if metadata_bits:
            lines.append(f"{'':<{width}}   {' | '.join(metadata_bits)}")
        details = component.get("details") or {}
        if component.get("status") == "fail":
            recommendation = details.get("recommended_action")
            impact = details.get("estimated_impact")
            if recommendation:
                lines.append(f"{'':<{width}}   Recommended: {recommendation}")
            if impact:
                lines.append(f"{'':<{width}}   Impact: {impact}")

    overall = report.get("overall", {})
    lines.append("")
    lines.append(f"{'Overall':<{width}} {OVERALL_SYMBOLS.get(overall.get('status'), '⚪ UNKNOWN')}")
    return "\n".join(lines)


def main() -> int:
    report = collect_status()
    print(render_terminal(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
