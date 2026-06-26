#!/usr/bin/env python3
"""Markdown renderer for control-plane status output."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .collector import collect_status

DEFAULT_REPORT_PATH = Path("/opt/data/home/control-plane/reports/latest-health-report.md")


def timestamped_report_path(report: dict[str, Any], reports_dir: Path | None = None) -> Path:
    reports_dir = reports_dir or DEFAULT_REPORT_PATH.parent
    generated_at = report.get("generated_at")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if isinstance(generated_at, str):
        try:
            stamp = datetime.fromisoformat(generated_at.replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        except ValueError:
            pass
    return reports_dir / f"health-report-{stamp}.md"


def render_markdown(report: dict[str, Any]) -> str:
    host = report.get("host", {})
    lines: list[str] = []
    lines.append("# Latest Health Report")
    lines.append("")
    lines.append(f"- Hostname: `{host.get('hostname', 'unknown')}`")
    lines.append(f"- Generated at: `{report.get('generated_at', 'unknown')}`")
    lines.append(f"- Overall: `{report.get('overall', {}).get('status', 'unknown')}`")
    lines.append("")
    lines.append("## Components")
    lines.append("")

    for component in report.get("components", []):
        details = component.get("details") or {}
        lines.append(f"- **{component.get('component', 'Unknown')}**: `{component.get('status', 'unknown')}` — {component.get('message', '')}")
        metadata_bits = []
        for label, key in [("Confidence", "confidence"), ("Reasoning", "reasoning"), ("Evidence", "evidence_timestamp"), ("Last checked", "last_checked")]:
            value = component.get(key)
            if value:
                metadata_bits.append(f"{label}: {value}")
        if metadata_bits:
            lines.append(f"  - Metadata: {' | '.join(metadata_bits)}")
        if details:
            lines.append(f"  - Details: `{json.dumps(details, sort_keys=True)}`")
            if component.get("status") == "fail":
                if details.get("recommended_action"):
                    lines.append(f"  - Recommended action: {details['recommended_action']}")
                if details.get("estimated_impact"):
                    lines.append(f"  - Estimated impact: {details['estimated_impact']}")

    lines.append("")
    lines.append("## Overall")
    overall = report.get("overall", {})
    lines.append(f"- **Status**: `{overall.get('status', 'unknown')}`")
    lines.append(f"- **Severity**: `{overall.get('severity', 'unknown')}`")
    lines.append(f"- **Message**: {overall.get('message', '')}")
    return "\n".join(lines) + "\n"


def write_report(path: Path = DEFAULT_REPORT_PATH) -> Path:
    report = collect_status()
    content = render_markdown(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    timestamped_path = timestamped_report_path(report, path.parent)
    timestamped_path.write_text(content, encoding="utf-8")
    return path


def main() -> int:
    path = write_report()
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
