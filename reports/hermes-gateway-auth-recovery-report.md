# Incident Recovery Report: Hermes Gateway Authentication

**Date:** `2026-06-26`
**Status:** `Resolved`

## 1. Incident Summary

At approximately `10:08 UTC`, the Hermes gateway became unresponsive to commands via Telegram. An incident response was initiated to restore service.

## 2. Root Cause Analysis

- **Diagnosis:** The gateway service was `active (running)`, but was unable to process requests requiring AI model interaction.
- **Root Cause:** Journal logs revealed `HTTP 401` errors, indicating that the service's OAuth 2.0 access token for the Google Cloud Vertex AI backend had expired. The gateway was unable to authenticate and therefore could not fulfill user requests.

## 3. Recovery Actions

1.  **Credential Refresh:** A non-interactive refresh of the Google Application Default Credentials (ADC) was successfully triggered.
2.  **Service Restart:** A single, controlled restart of the `systemd` user service was performed to force the gateway to load the newly refreshed authentication token.
    *   **Command:** `systemctl --user restart hermes-gateway.service`

## 4. Post-Recovery Verification

- [x] **Service Active:** `hermes-gateway.service` successfully restarted and is `active`.
- [x] **No Errors in Log:** Journal logs since the restart show no new `AuthenticationError` or `Telegram polling conflict` errors.
- [x] **Connectivity Test:** A `Ping` message was successfully sent via Telegram to confirm end-to-end connectivity.

## 5. Conclusion

The incident has been resolved. The root cause was an expired authentication token for the Google AI backend. The service has been successfully restarted with a valid token, and full functionality is restored.
