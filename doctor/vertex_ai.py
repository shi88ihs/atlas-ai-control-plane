"""Vertex AI authentication health check."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from .common import iso_now, record, truncate

CONFIG_PATH = Path("/home/ec2-user/.hermes/config.yaml")


def _load_config() -> dict:
    try:
        import yaml  # type: ignore
    except Exception:
        return {}

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception:
        return {}


def _discover_active_provider(cfg: dict) -> dict[str, object] | None:
    model = cfg.get("model") or {}
    provider = str(model.get("provider") or "").strip()
    base_url = str(model.get("base_url") or "").strip()
    default_model = str(model.get("default") or "").strip()
    api_key = str(model.get("api_key") or "").strip()
    default_headers = model.get("default_headers") or {}

    if not provider or not base_url or not default_model:
        return None

    if "aiplatform.googleapis.com" in base_url:
        import subprocess
        import shutil
        from .common import service_env_for_gateway
        try:
            gcloud_bin = shutil.which("gcloud") or "gcloud"
            proc = subprocess.run(
                [gcloud_bin, "auth", "application-default", "print-access-token"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
                env=service_env_for_gateway(),
            )
            api_key = proc.stdout.strip()
        except Exception:
            pass

    if not api_key:
        return None

    return {
        "provider": provider,
        "base_url": base_url,
        "default_model": default_model,
        "api_key": api_key,
        "default_headers": default_headers,
    }


def check() -> dict[str, object]:
    checked_at = iso_now()
    details: dict[str, object] = {
        "config_file": str(CONFIG_PATH),
        "config_file_exists": CONFIG_PATH.exists(),
    }

    cfg = _load_config()
    discovered = _discover_active_provider(cfg)
    if discovered is None:
        details["recommended_action"] = "Verify the live Hermes model configuration so the active provider can be discovered."
        details["estimated_impact"] = "Vertex AI validation was skipped because the provider could not be resolved from runtime config."
        return record(
            component="Vertex AI",
            status="info",
            severity="info",
            message="Vertex AI provider discovery is unavailable; check skipped",
            details=details,
            confidence="Low",
            reasoning="The live runtime provider could not be resolved from the current Hermes configuration.",
            evidence_timestamp=checked_at,
            last_checked=checked_at,
        )

    details.update(
        {
            "discovered_provider": discovered["provider"],
            "discovered_base_url": discovered["base_url"],
            "discovered_default_model": discovered["default_model"],
            "x_goog_user_project_present": bool((discovered.get("default_headers") or {}).get("x-goog-user-project")),
        }
    )

    endpoint = f"{str(discovered['base_url']).rstrip('/')}/chat/completions"
    payload = json.dumps(
        {
            "model": discovered["default_model"],
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 1,
            "temperature": 0,
        }
    ).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {discovered['api_key']}",
        "Content-Type": "application/json",
    }
    if isinstance(discovered.get("default_headers"), dict):
        user_project = discovered["default_headers"].get("x-goog-user-project")
        if user_project:
            headers["x-goog-user-project"] = str(user_project)

    request = urllib.request.Request(endpoint, data=payload, method="POST", headers=headers)

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            details["api_readiness_http_status"] = getattr(response, "status", 200)
            details["api_readiness_check"] = "success"
            return record(
                component="Vertex AI",
                status="pass",
                severity="info",
                message="Vertex AI provider is discovered from live runtime config and the API is reachable",
                details=details,
                confidence="High",
                reasoning="The active provider and endpoint were discovered from the live model config and the readiness probe succeeded.",
                evidence_timestamp=checked_at,
                last_checked=checked_at,
            )
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        details["api_readiness_http_status"] = exc.code
        details["api_readiness_error"] = truncate(body or str(exc))
        details["recommended_action"] = "Check the active runtime model endpoint, model name, and bearer token configured in Hermes."
        details["estimated_impact"] = "Vertex AI requests are not reaching a successful authenticated response."
        return record(
            component="Vertex AI",
            status="fail",
            severity="critical",
            message=f"Vertex AI readiness check returned HTTP {exc.code}",
            details=details,
            confidence="High",
            reasoning="The active provider and endpoint were discovered from the live model config, and the authenticated probe failed.",
            evidence_timestamp=checked_at,
            last_checked=checked_at,
        )
    except Exception as exc:
        details["api_readiness_check"] = "error"
        details["api_readiness_error"] = truncate(str(exc))
        details["recommended_action"] = "Verify local network access to the active Vertex endpoint and retry the non-destructive probe."
        details["estimated_impact"] = "Vertex AI readiness could not be confirmed."
        return record(
            component="Vertex AI",
            status="fail",
            severity="critical",
            message="Vertex AI readiness check could not be executed",
            details=details,
            confidence="Medium",
            reasoning="The active runtime provider was discovered, but the readiness probe could not complete.",
            evidence_timestamp=checked_at,
            last_checked=checked_at,
        )
