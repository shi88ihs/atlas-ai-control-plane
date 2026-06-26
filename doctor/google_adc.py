"""Google ADC authentication health check."""

from __future__ import annotations

import shutil
from pathlib import Path

from .common import (
    gateway_service_context,
    iso_now,
    record,
    run_command,
    service_env_for_gateway,
    truncate,
)


def check() -> dict[str, object]:
    checked_at = iso_now()
    context = gateway_service_context()
    service_home = context["home"]
    adc_path = Path(service_home) / ".config" / "gcloud" / "application_default_credentials.json"
    details: dict[str, object] = {
        "credential_file": str(adc_path),
        "credential_file_exists": adc_path.exists(),
        "service_home": service_home,
        "service_user": context.get("user"),
        "service_logname": context.get("logname"),
        "service_environment_home": context.get("environment", {}).get("HOME"),
        "service_environment_source": "hermes-gateway.service",
    }

    if not adc_path.exists():
        details["recommended_action"] = "Create Google Application Default Credentials in the gateway service home context."
        details["estimated_impact"] = "Vertex AI authentication cannot succeed until ADC exists."
        return record(
            component="Google ADC",
            status="fail",
            severity="critical",
            message="Google ADC credentials file is missing",
            details=details,
            confidence="High",
            reasoning="The credential file is absent at the gateway service home path.",
            evidence_timestamp=checked_at,
            last_checked=checked_at,
        )

    gcloud = shutil.which("gcloud")
    details["gcloud_present"] = bool(gcloud)
    if not gcloud:
        details["recommended_action"] = "Expose the gcloud CLI so ADC tokens can be requested locally."
        details["estimated_impact"] = "ADC token retrieval is unavailable, so Vertex AI auth checks cannot complete."
        return record(
            component="Google ADC",
            status="fail",
            severity="critical",
            message="gcloud is not available to obtain an ADC access token",
            details=details,
            confidence="High",
            reasoning="The required gcloud binary is unavailable in the local runtime.",
            evidence_timestamp=checked_at,
            last_checked=checked_at,
        )

    proc = run_command(
        [gcloud, "auth", "application-default", "print-access-token"],
        timeout=20,
        env=service_env_for_gateway(),
    )
    if proc is None:
        details["recommended_action"] = "Retry ADC token acquisition from the gateway service environment."
        details["estimated_impact"] = "ADC token acquisition is currently unavailable."
        return record(
            component="Google ADC",
            status="fail",
            severity="critical",
            message="Unable to obtain a Google ADC access token",
            details=details,
            confidence="Medium",
            reasoning="The token command could not be executed or timed out.",
            evidence_timestamp=checked_at,
            last_checked=checked_at,
        )

    details["token_request_exit_code"] = proc.returncode
    if proc.returncode == 0 and proc.stdout.strip():
        return record(
            component="Google ADC",
            status="pass",
            severity="info",
            message="Google ADC credentials file exists and an access token can be obtained",
            details=details,
            confidence="High",
            reasoning="The token request succeeded in the same service context used by hermes-gateway.service.",
            evidence_timestamp=checked_at,
            last_checked=checked_at,
        )

    details["stderr"] = truncate(proc.stderr)
    details["recommended_action"] = "Refresh Google ADC outside this check path if token acquisition is failing."
    details["estimated_impact"] = "Vertex AI authentication cannot be validated until ADC token retrieval succeeds."
    return record(
        component="Google ADC",
        status="fail",
        severity="critical",
        message="Google ADC token acquisition failed",
        details=details,
        confidence="High",
        reasoning="The token request ran in the live gateway service context and returned a failure.",
        evidence_timestamp=checked_at,
        last_checked=checked_at,
    )
