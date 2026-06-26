# Auth Health Check Accuracy Audit

## Scope

Discovery-only audit of the new authentication health checks:

- `doctor/google_adc.py`
- `doctor/vertex_ai.py`
- `doctor/telegram.py`

Rules honored:

- no credential changes
- no credential refreshes initiated for repair
- no service restarts
- no config changes
- no file moves or deletions

## Live runtime facts

- `hermes-gateway.service` is running as the `ec2-user` account.
- Service environment shows:
  - `HOME=/home/ec2-user`
  - `USER=ec2-user`
  - `LOGNAME=ec2-user`
  - `HERMES_HOME=/home/ec2-user/.hermes`
- The gateway has a single live process:
  - `652338 /home/ec2-user/hermes-agent/venv/bin/python -m hermes_cli.main gateway run`
- Latest gateway restart was at:
  - `2026-06-26T10:14:22+0000`

## Google ADC accuracy check

### What was checked

- ADC credential file path:
  - `/home/ec2-user/.config/gcloud/application_default_credentials.json`
- Same-user token acquisition test in the service home context:
  - `HOME=/home/ec2-user ... gcloud auth application-default print-access-token`
  - result: success (`rc=0`)

### Conclusion

- **Current health-check result:** false positive in the audit shell context
- **Reason:** the check depends on the environment it is executed in. When forced into the gateway service home context (`HOME=/home/ec2-user`), token acquisition succeeds.

### Notes

- The service home is correct.
- The ADC path is correct.
- The check should be executed in the gateway service environment, not the Hermes audit shell environment, to avoid skew.

## Vertex AI accuracy check

### What was checked

The live Hermes config shows:

- top-level model provider: `custom`
- top-level model default: `google/gemini-3.1-pro-preview`
- top-level model base URL:
  - `https://aiplatform.googleapis.com/v1/projects/project-91c7cf5c-8b55-4f82-a17/locations/global/endpoints/openapi`
- top-level model has its own `api_key`
- a separate `providers.vertex-ai` block also exists:
  - `https://us-central1-aiplatform.googleapis.com/v1beta1/projects/project-91c7cf5c-8b55-4f82-a17/locations/us-central1/endpoints/openapi`
  - default model `google/gemini-2.5-flash`

The current doctor check probes the separate `providers.vertex-ai` block and validates ADC-based access.

### Runtime evidence

Post-restart gateway logs still show authentication failures on the active runtime backend:

- `provider=custom`
- `base_url=https://aiplatform.googleapis.com/v1/projects/project-91c7cf5c-8b55-4f82-a17/locations/global/endpoints/openapi`
- `model=google/gemini-3.1-pro-preview`
- `HTTP 401`
- `ACCESS_TOKEN_TYPE_UNSUPPORTED`

### Conclusion

- **Current health-check result:** false positive as a runtime health indicator
- **Reason:** the check is not testing the same backend Hermes actually uses. It is probing the separate `providers.vertex-ai` path, while the live gateway is using the top-level `custom` model config.
- The live runtime still has a real auth failure on the active backend, so the check is misleading even though it can pass in isolation.

## Telegram accuracy check

### What was checked

- Current gateway PID list:
  - one process only
- Post-restart log window:
  - `journalctl --since '2026-06-26 10:14:22 UTC'`

### Findings

- No Telegram log lines were found after the latest restart.
- Duplicate polling conflict lines exist, but they are from **before** the latest restart:
  - e.g. `Jun 25 16:35:10` and neighboring entries
- There is no post-restart evidence of duplicate polling.
- There is also no post-restart evidence of successful Telegram message handling in the current log slice.

### Conclusion

- **Current health-check result:** stale-log false positive
- **Reason:** the check scans a broad historical journal window and picks up pre-restart Telegram conflict logs instead of limiting itself to the post-restart window.

## True failures

- The active live Vertex AI backend still shows post-restart authentication failures in the gateway logs.
- Telegram health is not proven healthy after the latest restart because no post-restart Telegram handling logs were observed.

## False positives

- **Google ADC:** false positive in the audit shell context; same-service-home token acquisition succeeds.
- **Vertex AI:** false positive as a health check; it tests the wrong backend and can disagree with the live runtime.
- **Telegram:** false positive from stale pre-restart logs.

## Stale log detections

- Telegram duplicate polling conflicts are historical, not post-restart.
- No Telegram log entries were found after the latest restart.
- The audit shell environment differs from the gateway service environment, which can skew ADC results if the check does not normalize the subprocess environment.

## Exact recommended patch list

### 1) `doctor/google_adc.py`

- Force the token-acquisition subprocess to run with the gateway service home context.
- Set `HOME=/home/ec2-user` and related identity variables for the `gcloud` subprocess, or derive the target home from the gateway service environment.
- Keep token output suppressed.
- Preserve the existing success/failure-only reporting.

### 2) `doctor/vertex_ai.py`

- Stop probing the separate `providers.vertex-ai` block when the live runtime is using the top-level `model` config.
- Resolve the active backend from:
  - `model.provider`
  - `model.default`
  - `model.base_url`
  - `model.api_key`
  - `model.default_headers`
- Probe the same endpoint/model/auth source the gateway actually uses.
- If the active backend cannot be resolved, report `unknown` instead of passing a different backend.

### 3) `doctor/telegram.py`

- Limit journal scanning to logs **after** the latest `hermes-gateway.service` restart.
- Use the service’s `ActiveEnterTimestamp` or equivalent to set `journalctl --since`.
- Do not classify pre-restart conflicts as current failures.
- If there are no Telegram log lines after restart, return `unknown` or a low-confidence warning rather than `fail`.
- Separate duplicate-process detection from historical polling conflict detection.

### 4) Shared helper hardening

- Add a service-context helper in the doctor package if needed so checks can consistently discover the canonical gateway home and restart boundary.
- This should avoid shell-context skew when the control-plane audit is run from the Hermes CLI environment.

## Bottom line

- **Google ADC:** the current failure is not reproducible in the gateway service home context; treat the audit-shell failure as a false positive.
- **Vertex AI:** the check is not aligned to the live backend; treat the check result as a false positive, while also noting the live runtime still shows a real auth failure on the active backend.
- **Telegram:** the current failure is stale and should be ignored until the post-restart log window is used.
