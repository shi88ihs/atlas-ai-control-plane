# Docker Hermes Decommission Report

**Date:** `2026-06-26`
**Status:** `Completed`

## Summary

As approved, the conflicting Docker-based Hermes installation was successfully decommissioned. This action has resolved the "Telegram bot token already in use" error. The primary `systemd`-managed Hermes gateway was not affected and remains online and functional.

## Actions Taken

1.  **Disable Auto-Restart:** The restart policy for the `hermes` and `hermes-dashboard` Docker containers was set to `no` to prevent them from starting automatically on reboot.
    *   **Command:** `docker update --restart no hermes hermes-dashboard`
2.  **Stop Containers:** The `hermes` and `hermes-dashboard` containers were gracefully stopped.
    *   **Command:** `docker stop hermes hermes-dashboard`

## Verification Checklist

- [x] **Docker Containers Stopped:** `docker ps -a` confirms both `hermes` and `hermes-dashboard` have a status of `Exited`.
- [x] **Restart Policy Disabled:** `docker inspect` confirms the restart policy for both containers is `no`.
- [x] **Primary Gateway Active:** The `systemd`--user managed Hermes gateway (PID `570025`) is still running.
- [x] **Telegram/OpenClaw Responsive:** This connection remains active and responsive.
- [x] **No Competing Processes:** No duplicate `hermes gateway` processes were found.
- [x] **Dashboard Offline:** The web dashboard previously on `127.0.0.1:9119` is confirmed to be down, as expected.

## Next Steps

The immediate conflict is resolved. It is recommended to schedule a maintenance window to fully remove the now-disabled Docker-based Hermes artifacts (e.g., the `docker-compose.yml` file) to prevent this issue from recurring.
