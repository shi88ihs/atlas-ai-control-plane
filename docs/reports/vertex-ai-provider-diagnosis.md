# Vertex AI Provider Diagnosis

## Purpose
Diagnose and resolve integration constraints between the Hermes runtime provider configuration and Google Cloud's Vertex AI authentication mechanisms.

## Summary
Atlas executed a comprehensive diagnostic pass over the live model routing engine. It successfully mapped the provider resolution logic, identified how the runtime reads endpoint configurations, and confirmed how Google Application Default Credentials (ADC) interact with the gateway service environment.

## Architecture
- **Model Engine:** `hermes_cli.main`
- **Configuration Source:** `config.yaml`
- **Authentication:** Google Application Default Credentials (ADC) or explicit bearer token injection.
- **Endpoint Target:** `https://aiplatform.googleapis.com/v1/projects/...`

## Implementation
1. **Service Profiling:** Extracted the environment variables (`HERMES_HOME`, `PATH`) bound to the live `hermes-gateway.service` unit via systemd introspection.
2. **Logic Tracing:** Identified the exact code path (`hermes_cli/runtime_provider.py`) responsible for injecting API keys and headers into the HTTP request.
3. **Auth Strategy Validation:** Confirmed that when using Vertex AI, the system requires a specific structure of OAuth 2.0 access tokens and quota project headers (`x-goog-user-project`), unlike standard API-key based providers.

## Outcome
A clear understanding of the authentication flow was established. We determined that to reliably authenticate with Vertex AI, the `hermes-gateway.service` must be executed within an environment that successfully resolves the GCP ADC JSON, or the runtime provider must be patched to natively synthesize short-lived bearer tokens via `google-auth`.

## Lessons Learned
- Cloud provider integrations requiring short-lived OAuth tokens (like Vertex AI) necessitate different architectural handling than static API-key providers.
- Integrating diagnostic scripts (like `doctor/vertex_ai.py`) directly into the Atlas Control Plane drastically reduces time-to-resolution for complex authentication failures in production.