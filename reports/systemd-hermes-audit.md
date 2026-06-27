# Systemd Hermes Service Audit Report

**Date:** `2026-06-26`
**Status:** `Completed`

## 1. Executive Summary

This report details the configuration of the `systemd` user service responsible for running the active Hermes gateway. The audit confirms a clear and canonical set of paths for this installation, distinct from the now-disabled Docker deployment. The `systemd` service is correctly configured, enabled, and is the authoritative process for handling messaging.

## 2. Service Inspection

- **Systemd Unit:** `hermes-gateway.service` is the only Hermes-related unit found for the current user.
- **Unit File Path:** `/home/atlas-admin/.config/systemd/user/hermes-gateway.service`
- **Override File:** An override is present at `/home/atlas-admin/.config/systemd/user/hermes-gateway.service.d/override.conf`.

### Unit File Configuration (`systemctl cat`)

```ini
[Unit]
Description=Hermes Agent Gateway - Messaging Platform Integration
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/home/atlas-admin/hermes-agent/venv/bin/python -m hermes_cli.main gateway run
WorkingDirectory=/home/atlas-admin/.hermes
Environment="HERMES_HOME=/home/atlas-admin/.hermes"
EnvironmentFile=-/home/atlas-admin/.hermes/.env
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

- **ExecStart:** The gateway is run from a Python virtual environment in `/home/atlas-admin/hermes-agent/venv/`.
- **WorkingDirectory:** The working directory is `/home/atlas-admin/.hermes`.
- **Environment:** The service loads environment variables from `/home/atlas-admin/.hermes/.env` (if it exists).
- **Restart Policy:** The service is set to `Restart=always`.
- **Enabled:** The service is enabled and starts at login (`WantedBy=default.target`).
- **Dependencies:** The service waits for the network to be online.

## 3. Journald Logs

- **Log Command:** `journalctl --user -u hermes-gateway.service`
- **Analysis:** The logs clearly showed the repeating `Telegram polling conflict` error. Crucially, **these errors stopped immediately** after the Docker containers were stopped at approximately `09:00 UTC`, confirming the conflict has been resolved.

## 4. Authoritative Path Determination

Based on this audit, the following paths are considered canonical for the active Hermes installation:

- **Canonical Installation Directory:**
  - `/home/atlas-admin/hermes-agent/` (Contains the application code and Python venv)
- **Canonical Python Virtual Environment:**
  - `/home/atlas-admin/hermes-agent/venv/`
- **Authoritative Configuration Directory:**
  - `/home/atlas-admin/.hermes/` (Working directory, `HERMES_HOME`, and location of the `.env` file)
- **Authoritative Log Source:**
  - `journald` (as per the `systemd` service configuration)

## 5. Recommendations

The environment is now stable, with the `systemd` service operating as the single gateway. The following files and entities from the old Docker deployment are now obsolete and can be cleaned up to prevent future confusion.

- **Obsolete Files/Directories:**
  - **Docker Compose File:** The file at `/home/atlas-admin/hermes-agent/docker-compose.yml` which defines the conflicting Docker services.
  - **Docker Containers:** The stopped containers `hermes` and `hermes-dashboard`.
  - **Docker Image:** The `hermes-agent` image used by the containers.

- **Cleanup Opportunities (To be run in a future maintenance session):**
  1.  **Remove the Docker Compose file:** `rm /home/atlas-admin/hermes-agent/docker-compose.yml`
  2.  **Remove the stopped Docker containers:** `docker rm hermes hermes-dashboard`
  3.  **(Optional) Prune unused Docker images:** `docker image prune`
