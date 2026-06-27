# Latest Health Report

- Hostname: `Atlas runtime`
- Generated at: `2026-06-26T12:30:40.175664+00:00`
- Overall: `degraded`

## Components

- **Hermes Gateway**: `unknown` — systemd service state could not be determined
  - Details: `{"exit_code": 0, "stderr": "", "timed_out": false}`
- **OpenClaw**: `unknown` — systemd service state could not be determined
  - Details: `{"exit_code": 0, "stderr": "", "timed_out": false}`
- **systemd gateway service**: `unknown` — systemd service state could not be determined
  - Details: `{"exit_code": 0, "stderr": "", "timed_out": false}`
- **Disk usage**: `77%` — 77% used on /opt/data/home/control-plane
  - Details: `{"available_bytes": 20582178816, "exit_code": 0, "filesystem": "/dev/nvme0n1p1", "mountpoint": "/", "size_bytes": 85819633664, "stderr": "", "target": "/opt/data/home/control-plane", "timed_out": false, "used_bytes": 65237454848, "used_percent": 77}`
- **Memory**: `61%` — 61% memory used
  - Details: `{"available_bytes": 778514432, "total_bytes": 2006237184, "used_bytes": 1227722752, "used_percent": 61}`
- **Swap**: `32%` — 32% swap used
  - Details: `{"free_bytes": 2927112192, "total_bytes": 4294963200, "used_bytes": 1367851008, "used_percent": 32}`
- **Docker availability**: `available` — docker CLI and daemon are available
  - Details: `{"binary": "/usr/bin/docker", "exit_code": 0, "server_version": "25.0.16", "stderr": "", "timed_out": false}`
- **Docker container count**: `9` — 9 container(s) visible to the daemon
  - Details: `{"binary": "/usr/bin/docker", "count": 9, "exit_code": 0, "stderr": "", "timed_out": false}`
- **SSH client availability**: `available` — ssh client is available
  - Details: `{"binary": "/usr/bin/ssh", "exit_code": 0, "stderr": "OpenSSH_8.7p1, OpenSSL 3.5.5 27 Jan 2026", "timed_out": false, "version": "OpenSSH_8.7p1, OpenSSL 3.5.5 27 Jan 2026"}`
- **Tailscale availability**: `available` — tailscale daemon is running
  - Details: `{"backend_state": "Running", "binary": "/usr/bin/tailscale", "exit_code": 0, "self_host_name": "aws", "self_tailnet_ip": "<overlay-ip>", "stderr": "", "timed_out": false}`
- **Hostname**: `available` — Atlas runtime
  - Details: `{"hostname": "Atlas runtime"}`
- **Kernel**: `available` — redacted
  - Details: `{"kernel": "redacted"}`
- **Operating system**: `available` — Unknown
  - Details: `{"BUG_REPORT_URL=\"https": "//github.com/amazonlinux/amazon-linux-2023\"", "CPE_NAME=\"cpe": "2.3:o:amazon:amazon_linux:2023\"", "DOCUMENTATION_URL=\"https": "//docs.aws.amazon.com/linux/\"", "HOME_URL=\"https": "//aws.amazon.com/linux/amazon-linux-2023/\"", "PLATFORM_ID=\"platform": "al2023\"", "SUPPORT_URL=\"https": "//aws.amazon.com/premiumsupport/\"", "VENDOR_URL=\"https": "//aws.amazon.com/\""}`
- **Current user**: `available` — atlas-admin
  - Details: `{"user": "atlas-admin"}`
- **Current uptime**: `available` — 13d 4h 21m
  - Details: `{"uptime_human": "13d 4h 21m", "uptime_seconds": 1138891}`
- **Current load average**: `available` — 0.20, 0.17, 0.17
  - Details: `{"load_average": [0.2, 0.17, 0.17]}`
- **Current timestamp**: `available` — 2026-06-26T12:30:40.175635+00:00
  - Details: `{"timestamp": "2026-06-26T12:30:40.175635+00:00"}`
- **Google ADC**: `pass` — Google ADC credentials file exists and an access token can be obtained
  - Metadata: Confidence: High | Reasoning: The token request succeeded in the same service context used by hermes-gateway.service. | Evidence: 2026-06-26T12:30:34.191628+00:00 | Last checked: 2026-06-26T12:30:34.191628+00:00
  - Details: `{"credential_file": "~/.config/gcloud/application_default_credentials.json", "credential_file_exists": true, "gcloud_present": true, "service_environment_home": null, "service_environment_source": "hermes-gateway.service", "service_home": "~", "service_logname": "atlas-admin", "service_user": "atlas-admin", "token_request_exit_code": 0}`
- **Vertex AI**: `pass` — Vertex AI provider is discovered from live runtime config and the API is reachable
  - Metadata: Confidence: High | Reasoning: The active provider and endpoint were discovered from the live model config and the readiness probe succeeded. | Evidence: 2026-06-26T12:30:35.983044+00:00 | Last checked: 2026-06-26T12:30:35.983044+00:00
  - Details: `{"api_readiness_check": "success", "api_readiness_http_status": 200, "config_file": "<config-dir>/.hermes/config.yaml", "config_file_exists": true, "discovered_base_url": "https://aiplatform.googleapis.com/v1/projects/project-91c7cf5c-8b55-4f82-a17/locations/global/endpoints/openapi", "discovered_default_model": "google/gemini-3.1-pro-preview", "discovered_provider": "custom", "x_goog_user_project_present": true}`
- **Telegram**: `pass` — Telegram gateway is running and no recent authentication or polling failures were found
  - Metadata: Confidence: Medium | Reasoning: The gateway is active and the post-restart log window does not contain Telegram failures, but no explicit success entry was observed. | Evidence: 2026-06-26T12:30:20+0000 | Last checked: 2026-06-26T12:30:39.968811+00:00
  - Details: `{"current_process_count": 1, "current_processes": [{"cmd": "<install-path>/hermes-agent/venv/bin/python -m hermes_cli.main gateway run", "pid": 686277}], "duplicate_polling_detected": false, "gateway_running": true, "gateway_service": "hermes-gateway.service", "log_window_start": "Fri 2026-06-26 12:29:34 UTC", "recent_auth_errors": false, "recent_polling_failures": false, "recent_successful_polling_activity": false, "restart_timestamp": "Fri 2026-06-26 12:29:34 UTC", "service_home": "~", "service_user": "atlas-admin"}`

## Overall
- **Status**: `degraded`
- **Severity**: `warning`
- **Message**: Some subsystems need attention
