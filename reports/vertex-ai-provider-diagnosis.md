# Vertex AI Provider Diagnosis

## Summary

The Vertex AI failure is **not** a Doctor probe mismatch.

The live Hermes runtime and the Doctor are both pointing at the same Vertex-style backend:

- provider: `custom`
- model: `google/gemini-3.1-pro-preview`
- project ID: `project-91c7cf5c-8b55-4f82-a17`
- location: `global`
- config file: `/home/ec2-user/.hermes/config.yaml`

The live gateway logs show repeated **HTTP 401** failures against that same endpoint after the latest restart, with `ACCESS_TOKEN_TYPE_UNSUPPORTED` in the error details. That means the runtime failure is real.

**Diagnosis:** Real runtime failure
**Confidence:** 90%

## 1) Live Hermes provider configuration

### hermes-gateway.service environment

Observed from `systemctl --user show hermes-gateway.service`:

- `MainPID=652338`
- `ExecStart=/home/ec2-user/hermes-agent/venv/bin/python -m hermes_cli.main gateway run`
- `HERMES_HOME=/home/ec2-user/.hermes`
- `PATH` includes the Hermes venv and local node tools
- `User=` is empty in the user unit output, but the runtime context is the `ec2-user` user session
- latest restart timestamp: `Fri 2026-06-26 10:14:22 UTC`

### Live Hermes runtime config

Read from `/home/ec2-user/.hermes/config.yaml`.

Live model block:

- provider: `custom`
- model: `google/gemini-3.1-pro-preview`
- base_url: `https://aiplatform.googleapis.com/v1/projects/project-91c7cf5c-8b55-4f82-a17/locations/global/endpoints/openapi`
- quota project header: `x-goog-user-project: project-91c7cf5c-8b55-4f82-a17`

Additional provider block observed:

- `providers.vertex-ai`
  - name: `Vertex AI`
  - api: `https://us-central1-aiplatform.googleapis.com/v1beta1/projects/project-91c7cf5c-8b55-4f82-a17/locations/us-central1/endpoints/openapi`
  - api_mode: `chat_completions`
  - default_model: `google/gemini-2.5-flash`

### Credential source type

Live runtime credential source appears to be:

- **OAuth 2 access token** stored in the `api_key` field of `/home/ec2-user/.hermes/config.yaml`
- plus the `x-goog-user-project` header for quota/project association

This is the credential source used by the live runtime path shown in the logs.

## 2) Doctor Vertex check vs live Hermes runtime

Doctor file inspected:

- `/opt/data/home/control-plane/doctor/vertex_ai.py`

### Endpoint being tested by the Doctor

The Doctor tests:

- `endpoint = base_url + "/chat/completions"`
- it reads the live `model` block from `/home/ec2-user/.hermes/config.yaml`
- it uses:
  - `provider`
  - `base_url`
  - `default_model`
  - `api_key`
  - `default_headers.x-goog-user-project`

### What it assumes

The Doctor assumes:

- the top-level `model` block is the active runtime provider
- the model block already contains the real Vertex endpoint URL
- the `api_key` field is the bearer token to test

### Does this match live Hermes?

Yes.

The runtime logs show the same provider/model/endpoint shape:

- provider: `custom`
- base_url: `https://aiplatform.googleapis.com/v1/projects/project-91c7cf5c-8b55-4f82-a17/locations/global/endpoints/openapi`
- model: `google/gemini-3.1-pro-preview`

So the Doctor is **not** probing the wrong backend here.

## 3) Safe token checks

Executed in the gateway-style HOME/PATH context, without printing tokens:

- `gcloud auth application-default print-access-token >/dev/null`
  - **PASS**
- `gcloud auth print-access-token >/dev/null`
  - **PASS**

These checks show that token acquisition is possible in the local environment, but they do **not** prove that the token Hermes is actually sending is valid for the Vertex endpoint.

## 4) Vertex API enablement and identity

### Active gcloud account

- `milez667@gmail.com`

### Active gcloud project

- `project-91c7cf5c-8b55-4f82-a17`

### Configured quota project

- `CURRENT_PROJECT`

### Vertex API enablement

Verified enabled for the active project:

- `aiplatform.googleapis.com`
- enabled path returned: `projects/446761255900/services/aiplatform.googleapis.com`

### Identity / access signal

The environment can mint tokens successfully, and the API is enabled, but the live Hermes runtime still gets a 401. That points to an auth/credential problem in the runtime path, not a missing API enablement problem.

## 5) Recent Hermes logs after latest gateway restart

Log window used:

- since `2026-06-26 10:14:22 UTC`

Relevant entries found:

- repeated `AuthenticationError` failures for the live Vertex call
- provider: `custom`
- base_url: `https://aiplatform.googleapis.com/v1/projects/project-91c7cf5c-8b55-4f82-a17/locations/global/endpoints/openapi`
- model: `google/gemini-3.1-pro-preview`
- HTTP 401 with `ACCESS_TOKEN_TYPE_UNSUPPORTED`
- fallback to `google-gemini-cli` also failed because the provider is not configured

No successful Vertex model call was observed in the post-restart log window.

Telegram log review in the same window did **not** show a live post-restart Telegram failure pattern; Telegram remains healthy.

## 6) Diagnosis

### Classification

- **Real runtime failure**

### Why

- The Doctor is matching the live runtime configuration.
- The gateway itself is logging Vertex 401 errors against that same endpoint.
- The error is not limited to the Doctor probe.
- The failure appears to be an authentication/credential problem in the runtime path.

### Confidence

- **90%**

## 7) Recommended recovery steps

Because this is a real runtime failure, the recommended actions are operational recovery steps, not a Doctor patch:

1. Verify the bearer token source Hermes is using in `/home/ec2-user/.hermes/config.yaml`.
2. Replace or refresh that runtime token if it is stale or the wrong token type for Vertex AI Chat Completions.
3. Confirm the `x-goog-user-project` value remains `project-91c7cf5c-8b55-4f82-a17`.
4. If Hermes is intended to use the `providers.vertex-ai` block instead of the top-level `model` block, switch the runtime configuration to that provider path.
5. Re-test the live gateway after the credential/source correction.

## Patch recommendation

- **No Doctor probe patch recommended** for this issue.
- The probe matches the live runtime path, so the failure is in the runtime credential/auth path, not the check logic.
