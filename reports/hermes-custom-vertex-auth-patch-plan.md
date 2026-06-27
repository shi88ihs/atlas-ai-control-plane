# Hermes Custom Vertex Provider Auth Patch Plan

## Summary

Hermes is currently routing the configured `custom` Google model path through generic API-key plumbing.
The live config points at the Vertex AI OpenAI-compatible endpoint:

- `https://aiplatform.googleapis.com/v1/projects/.../locations/global/endpoints/openapi`

The runtime then forwards the configured secret as a plain bearer string, but there is no dedicated Vertex/ADC auth helper in the custom-provider path.
That makes the Vertex route depend on a static token in config instead of a live Google OAuth 2 access token from Application Default Credentials.

## Discovery findings

### Where the custom provider is resolved

- `hermes_cli/runtime_provider.py`
  - `_get_named_custom_provider()` reads `providers:` / `custom_providers:` entries and returns a runtime dict with `api_key` taken directly from config or env.
  - `_try_resolve_from_custom_pool()` also returns a runtime dict with `api_key` from `runtime_api_key` or `access_token`.

### Where the request auth header is built

- `agent/auxiliary_client.py`
  - `resolve_provider_client()` / `_get_cached_client()` build `OpenAI(api_key=api_key, base_url=base_url, ...)` for generic providers.
  - For the custom Vertex route, this means the runtime is using the generic bearer-token path with no Google ADC refresh step.

- `run_agent.py`
  - `_swap_credential()` also treats provider credentials as `runtime_api_key` / `access_token` and swaps them directly into the agent.

- `hermes_cli/auth.py`
  - Generic provider request code sends `Authorization: Bearer <access_token>`
  - There is no Vertex-specific code path that fetches/refreshes a Google OAuth 2 access token before constructing the header.

### Live config shape that confirms the route

- `model.provider: custom`
- `model.default: google/gemini-3.1-pro-preview`
- `model.base_url: https://aiplatform.googleapis.com/v1/projects/.../locations/global/endpoints/openapi`
- `model.default_headers.x-goog-user-project` is set
- `providers.vertex-ai` is also configured with a Vertex endpoint and a static bearer value

## Exact bug

The custom Vertex path is not using a dedicated Google ADC credential refresh flow.
It is using the generic custom-provider bearer-token plumbing, which expects the caller to already supply a valid OAuth 2 access token.
That is brittle for Vertex AI because:

- the token can expire,
- no refresh happens automatically,
- the custom path does not call `google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])`,
- and the current behavior can mix Vertex AI with generic OpenAI-style auth assumptions.

The symptom matches the live failure:

- HTTP 401
- `ACCESS_TOKEN_TYPE_UNSUPPORTED`

## Proposed fixed behavior

Implement a Vertex-specific auth resolution step for custom Google Vertex endpoints:

- Detect Vertex AI base URLs such as `aiplatform.googleapis.com`.
- Resolve credentials from ADC at runtime.
- Refresh the credential before use.
- Pass the live OAuth 2 access token as:

  `Authorization: Bearer <access_token>`

- Preserve existing `x-goog-user-project` headers.
- Keep all non-Vertex custom providers on the current generic path.


## Likely files to change

Primary candidates:

- `agent/auxiliary_client.py`
  - add Vertex-specific credential resolution before constructing the OpenAI client for custom endpoints.

- `run_agent.py`
  - make `_swap_credential()` or the surrounding credential plumbing aware of Vertex-specific runtime auth so the main agent also uses refreshed ADC tokens.

- `hermes_cli/runtime_provider.py`
  - detect Vertex AI custom endpoints and return a runtime credential object that is backed by ADC rather than a static config token.

Potential helper addition:

- `hermes_cli/auth.py` or `agent/google_oauth.py`
  - add a small reusable helper that returns a refreshed ADC access token for Vertex AI.

## Smallest safe implementation direction

1. Add a tiny Google ADC helper that:
   - calls `google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])`
   - refreshes the credential with `google.auth.transport.requests.Request()`
   - returns the access token only

2. Wire that helper into the Vertex custom-provider path only.

3. Leave all other providers unchanged.

This keeps the blast radius small and avoids changing behavior for non-Google providers.

## Rollback plan

If the patch causes regressions:

- restore the backed-up copies of any edited files
- revert the Vertex-specific helper call
- fall back to the current generic custom-provider bearer-token path

Before editing, make backups of every touched file, for example:

- `agent/auxiliary_client.py`
- `run_agent.py`
- `hermes_cli/runtime_provider.py`
- any new helper file if added

## Validation command

After patching, validate locally without restarting Hermes:

- `python3 -m py_compile /home/atlas-admin/hermes-agent/agent/auxiliary_client.py /home/atlas-admin/hermes-agent/run_agent.py /home/atlas-admin/hermes-agent/hermes_cli/runtime_provider.py`
- `control-plane doctor`
- `control-plane status`
- `control-plane report`

Expected result:

- Google ADC: PASS
- Telegram: PASS
- Vertex AI: PASS
- no token values printed

## Approval gate

No code changes were made in this step.
Waiting for approval before editing.
