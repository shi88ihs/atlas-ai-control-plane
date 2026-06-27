# Network Discovery

## Interfaces

Observed interfaces:

- `lo` — `127.0.0.1/8`, `::1/128`
- `ens5` — `10.0.0.10/20`, IPv6 link-local present
- `docker0` — `10.1.0.1/16`
- `br-9d2fd27211b3` — `10.3.0.1/16`
- `br-9f7c7db89280` — `10.2.0.1/16`
- `br-88f71d868620` — `10.4.0.1/16`
- `tailscale0` — `10.0.0.11/32`, `fd7a:115c:a1e0::placeholder/128`

## Routes

Default and local routes observed:

- Default route via `10.0.0.1` on `ens5`
- Local VPC route `10.0.0.0/20` on `ens5`
- Docker bridge routes for `10.1.0.0/16`, `10.2.0.0/16`, `10.3.0.0/16`, `10.4.0.0/16`

## DNS configuration

`/etc/resolv.conf` contains:

- `169.254.169.254`
- `1.1.1.1`
- `8.8.8.8`

## Listening services

Notable listeners from `ss -ltnup`:

- `127.0.0.1:8080` — OpenClaw gateway listener
- `127.0.0.1:8090` — Hermes-related listener
- `127.0.0.1:8022` — local SSH tunnel endpoint for the local PC path seen earlier in the session
- `0.0.0.0:22` and `[::]:22` — host SSH server
- `10.0.0.11:443` and `[fd7a:115c:a1e0::placeholder]:443` — tailnet HTTPS listener
- Docker-published application ports including `3000`, `3012`, `8080`, `8081`, `34573`, `37079`, `42741`, `51753`, and `5678`

## localhost services

Verified localhost reachability:

- `http://127.0.0.1:8080` is listening
- `http://127.0.0.1:5678` is listening
- `http://127.0.0.1:8022` is listening

## Outbound Internet access

Verified working:

- `https://example.com` returned `200`
- `https://check.torproject.org` returned `200`

## IMDS status

- AWS Instance Metadata Service (IMDS): **Not Tested (Approval Required)**

## Tailscale presence

- `tailscale0` is present and configured
- Tailscale CLI exists on the runtime path

## Notes

- No network settings were changed.
- This is a read-only snapshot only.
