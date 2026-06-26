"""Collector for authentication doctor checks."""

from __future__ import annotations

from typing import Any

from .common import iso_now, record
from .google_adc import check as check_google_adc
from .telegram import check as check_telegram
from .vertex_ai import check as check_vertex_ai

SCHEMA_VERSION = "1.0"
SEVERITY_ORDER = {"info": 0, "warning": 1, "critical": 2, "unknown": -1}


def overall_status(components: list[dict[str, Any]]) -> dict[str, Any]:
    severity_rank = max((SEVERITY_ORDER.get(component.get("severity", "unknown"), -1) for component in components), default=-1)
    if severity_rank >= 2:
        status = "fail"
        severity = "critical"
        message = "One or more authentication checks require attention"
    elif severity_rank >= 1:
        status = "degraded"
        severity = "warning"
        message = "Some authentication checks need attention"
    else:
        status = "healthy"
        severity = "info"
        message = "All authentication checks passed"
    return record(
        component="Authentication overall",
        status=status,
        severity=severity,
        message=message,
        details={"component_count": len(components)},
    )


def collect_doctor_checks() -> dict[str, Any]:
    components = [
        check_google_adc(),
        check_vertex_ai(),
        check_telegram(),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": iso_now(),
        "components": components,
        "overall": overall_status(components),
    }


def main() -> int:
    import json

    print(json.dumps(collect_doctor_checks(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
