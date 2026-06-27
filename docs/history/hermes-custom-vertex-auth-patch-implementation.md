# Hermes Custom Vertex Provider Auth Patch Implementation

## Summary

I patched the Hermes custom provider runtime so Vertex AI/Gemini requests use a Google ADC OAuth access token instead of the generic custom-provider API-key/bearer-token path.

This keeps the change narrowly scoped to the custom Vertex path and avoids changing unrelated providers or model configuration.

## What changed

### `hermes_cli/runtime_provider.py`

Added a small Vertex-specific auth helper and routing guard:

- Detects Vertex AI base URLs via `*.aiplatform.googleapis.com`
- Loads Google Application Default Credentials with the `cloud-platform` scope
- Refreshes the credential when needed
- Extracts the OAuth access token
- Uses that token as the runtime `api_key` for custom Vertex requests
- Bypasses the generic credential pool / API-key fallback for Vertex custom endpoints

### `tests/hermes_cli/test_runtime_provider_resolution.py`

Added a regression test that verifies:

- `provider: custom` + Vertex base URL resolves to an ADC token
- the generic pool path is not used
- the resolved runtime keeps `provider: custom`
- the runtime source is marked as Vertex ADC

## Backups

Backups were created before editing:

- `<install-path>/hermes-agent/.backup-20260626-121248/runtime_provider.py`
- `<install-path>/hermes-agent/.backup-20260626-121248/test_runtime_provider_resolution.py`

## Validation

Completed successfully:

- `python3 -m py_compile hermes_cli/runtime_provider.py tests/hermes_cli/test_runtime_provider_resolution.py`
- `pytest -q tests/hermes_cli/test_runtime_provider_resolution.py -k vertex_custom`

Result:

- `1 passed, 129 deselected`

Additional checks:

- Backups confirmed present
- No tokens were printed in validation output
- No credentials were modified

## Remaining gaps

- Hermes was not restarted yet, per instruction
- Live gateway-level end-to-end verification still depends on a restart after approval

## Recommended next step

If you approve, I can restart `hermes-gateway.service` and then verify the Vertex path end-to-end against the live runtime.
