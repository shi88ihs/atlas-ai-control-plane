# Phase 6.3 — Doctor Calibration Report

## Summary

The authentication Doctor was recalibrated to reflect the live Hermes runtime instead of the earlier assumption-based probes.

Validation after patching shows:

- **Google ADC** now reports **PASS** using the same gateway service home/context.
- **Vertex AI** now probes the **live configured provider** and reports the actual runtime result.
- **Telegram** now ignores stale pre-restart conflict logs and reports **PASS** when the post-restart log window is clean.
- `control-plane doctor`, `control-plane status`, and `control-plane report` all run successfully with the calibrated checks.

The current runtime-state outcome is:

- Google ADC: pass
- Vertex AI: fail (HTTP 401 from the live provider probe)
- Telegram: pass
- Overall: fail, which matches the live runtime because Vertex AI still rejects the authenticated probe

## Patches Applied

### Shared doctor helpers

- `doctor/common.py`
  - Added gateway service context discovery from `hermes-gateway.service`
  - Added gateway service environment reconstruction for read-only subprocess probes
  - Extended `record()` to carry:
    - `confidence`
    - `reasoning`
    - `evidence_timestamp`
    - `last_checked`

### Google ADC

- `doctor/google_adc.py`
  - Switched token acquisition to use the same gateway service home/context
  - Uses the service-derived HOME, USER, LOGNAME, HERMES_HOME, PATH, and CLOUDSDK_CONFIG values
  - Reports only success/failure, without printing tokens
  - Adds confidence and freshness metadata

### Vertex AI

- `doctor/vertex_ai.py`
  - Removed the assumption that Vertex should be tested via the older sidecar/provider path
  - Discovers the live Hermes runtime provider from `<config-dir>/.hermes/config.yaml`
  - Probes the configured provider endpoint directly
  - Returns `INFO` when provider discovery is unavailable instead of incorrectly failing
  - Adds confidence and freshness metadata

### Telegram

- `doctor/telegram.py`
  - Restricts log inspection to entries newer than the latest gateway restart
  - Ignores historical duplicate-polling conflict logs
  - Checks current gateway processes before deciding on duplicate polling
  - Returns `PASS` when the gateway is running and no recent auth/poll failures exist
  - Adds confidence and freshness metadata

### Human-readable output

- `doctor/renderer_terminal.py`
- `status/renderer_terminal.py`
- `status/renderer_markdown.py`
  - Display the new confidence/freshness fields in the rendered output
  - Preserve the recommended-action / estimated-impact guidance on failures

### Status collector alignment

- `status/collector.py`
  - Corrected the canonical service unit names to include the `.service` suffix

## Before / After Behavior

### Google ADC

**Before**
- Reported a failure in the audit path even though the gateway service context could successfully obtain a token.
- The check was not consistently aligned to the live gateway credential context.

**After**
- Runs in the same service home/context used by `hermes-gateway.service`.
- Token acquisition now succeeds.
- Reported result is a true **PASS**.

### Vertex AI

**Before**
- Used the older/provider-assumption path and could misclassify the runtime as healthy.
- Produced a false-positive style result against the wrong backend.

**After**
- Discovers the active provider from the live runtime config.
- Probes the configured provider directly.
- Current result is a real **FAIL** with HTTP 401, which matches the live runtime behavior.
- If discovery is unavailable, it now returns **INFO** instead of a misleading fail.

### Telegram

**Before**
- Treated historical duplicate polling conflicts as current failures.
- Could surface stale pre-cleanup logs as if they were live runtime problems.

**After**
- Only inspects logs after the latest gateway restart.
- Ignores historical conflict noise.
- Current result is **PASS**, because the gateway is running and the post-restart window shows no auth or polling failures.

## Validation

Executed successfully:

- `control-plane doctor`
- `control-plane status`
- `control-plane report`

Observed results:

- Google ADC: pass
- Vertex AI: fail (HTTP 401 from the live provider probe)
- Telegram: pass
- Overall: fail

This matches the live runtime state we are calibrating against.

## Remaining Limitations

- The broader status layer still has some host-overview probe gaps unrelated to the auth checks, including systemd/OS rows that can show as `unknown` in the current environment.
- Vertex AI remains a live runtime failure until the configured bearer token/endpoint becomes valid again.
- Telegram confidence is only `Medium` when no explicit post-restart success line is present, even if the post-restart failure window is clean.

## Future Improvement Ideas

- Add a dedicated provider-discovery helper that can resolve more Hermes provider shapes without hardcoding a single config structure.
- Emit explicit post-restart success markers from the gateway so Telegram can report `High` confidence more often.
- Normalize the broader host probes so systemd and OS metadata always resolve cleanly in `control-plane status`.
- Add a small unit-test fixture set for the three doctor checks using captured config/log samples.
- Consider a compact machine-readable doctor schema for downstream automation and dashboards.
