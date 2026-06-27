# Security Philosophy

## Read-Only by Default
The Atlas Control Plane fundamentally distrusts the managed AI runtimes it oversees. It operates on a strict read-only paradigm for diagnostic checks: the system can observe, report, and alert, but it requires explicit external approval to mutate the host.

## Principle of Least Privilege
AI runtimes managed by Atlas execute under a highly restricted user account (`atlas-admin`). They are granted access to essential APIs and ephemeral Docker sockets, but lack the `sudo` privileges required to modify kernel parameters, alter network interfaces, or mutate the host `systemd` daemon.

## Transport Security
Atlas assumes the underlying physical network is hostile. All management access, dashboard routing, and intra-fleet communication are forced over an encrypted identity-aware overlay network (Tailscale/WireGuard). Unauthenticated inbound ports are strictly prohibited.

## Secret Isolation
Atlas actively isolates sensitive material. The core GitOps repository is protected by aggressive `.gitignore` policies designed to trap API keys, OAuth tokens, and private SSH certificates before they can be committed to the tree. Authentication logic relies on localized, ephemeral credential loading rather than hardcoded environment variables.