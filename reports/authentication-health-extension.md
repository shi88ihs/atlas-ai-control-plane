# Phase 6.1 — Authentication Health Checks

## Summary

The AI Operations Doctor was extended with three new read-only authentication checks:

- `Google ADC`
- `Vertex AI`
- `Telegram`

These checks were wired into both:

- `control-plane doctor`
- `control-plane status`

A refreshed control-plane health report was also generated so the new checks appear in the canonical status output.

## Documents and files updated

### New doctor checks
- `/opt/data/home/control-plane/doctor/google_adc.py`
- `/opt/data/home/control-plane/doctor/vertex_ai.py`
- `/opt/data/home/control-plane/doctor/telegram.py`
- `/opt/data/home/control-plane/doctor/collector.py`
- `/opt/data/home/control-plane/doctor/renderer_terminal.py`
- `/opt/data/home/control-plane/doctor/common.py`
- `/opt/data/home/control-plane/doctor/__init__.py`

### Control-plane command wiring
- `/opt/data/home/control-plane/scripts/doctor`
- `/opt/data/home/control-plane/scripts/control-plane`

### Status/report integration
- `/opt/data/home/control-plane/status/collector.py`
- `/opt/data/home/control-plane/status/renderer_terminal.py`
- `/opt/data/home/control-plane/status/renderer_markdown.py`
- `/opt/data/home/control-plane/status/README.md`
- `/opt/data/home/control-plane/README.md`

### Generated report
- `/opt/data/home/control-plane/reports/latest-health-report.md`
- `/opt/data/home/control-plane/reports/authentication-health-extension.md`

## Validation results

### Google ADC
- Credential file exists at `/home/ec2-user/.config/gcloud/application_default_credentials.json`
- `gcloud auth application-default print-access-token` failed
- Result: **fail**
- Recommended action: refresh Google ADC outside this check path if token acquisition is failing
- Estimated impact: Vertex AI authentication cannot be validated until ADC token retrieval succeeds

### Vertex AI
- Configuration file exists at `/home/ec2-user/.hermes/config.yaml`
- Vertex AI provider block is present
- `x-goog-user-project` is present in the top-level model headers
- ADC token acquisition failed, so API readiness could not be confirmed
- Result: **fail**
- Recommended action: fix Google ADC so Vertex AI can acquire a fresh access token
- Estimated impact: Vertex AI calls will fail until ADC token acquisition succeeds

### Telegram
- Canonical Hermes gateway process is running
- Recent successful polling activity was **not** found in the recent journal slice
- Duplicate polling conflicts were found in the journal
- Recent Telegram auth errors were **not** found in the journal slice
- Result: **fail**
- Recommended action: ensure only one canonical Telegram poller is active and confirm the bot credentials are valid
- Estimated impact: Telegram messages may be delayed, dropped, or unavailable until polling stabilizes

## Remaining gaps

- Google ADC still needs valid token acquisition before Vertex AI can be fully confirmed.
- Vertex AI readiness could not progress past ADC token retrieval.
- Telegram polling still shows conflict evidence, so the gateway is not yet cleanly single-instanced.
- No automatic repair was attempted, per instruction.

## Recommended Phase 5

Phase 5 should focus on operational stabilization:

1. Resolve Google ADC token acquisition from the canonical user account.
2. Re-run the Vertex AI readiness probe after ADC succeeds.
3. Remove duplicate Telegram polling activity and confirm a clean polling cycle.
4. Keep the doctor and status checks in the regular daily report flow.
5. Add a lightweight trend log so future auth regressions can be detected quickly.

## Validation commands run

- `control-plane doctor`
- `control-plane status`
- `control-plane collect`
- `control-plane report`

All checks were executed read-only.
