# Network Architecture Discovery

## Purpose
Document the network topology, active interfaces, and listener boundaries of the Atlas deployment environment to establish a baseline for secure operations.

## Summary
The deployment environment utilizes a multi-interface network architecture combining a primary cloud VPC interface, a Tailscale VPN overlay for secure administrative access, and several Docker bridge networks for containerized workloads. Outbound access is verified, and critical services are bound strictly to loopback or the Tailscale interface.

## Architecture
- **Primary Transport:** Cloud provider VPC (`ens5`) for outbound connectivity.
- **Secure Overlay:** Tailscale (`tailscale0`) for encrypted, identity-aware administrative access and internal web dashboards.
- **Container Networking:** Docker bridge networks for isolated workload execution.
- **Service Binding:** Critical Atlas services bind exclusively to `127.0.0.1` and are exposed selectively via reverse proxies or Tailscale.

## Implementation
1. **Interfaces:** Evaluated using standard IP tooling (`ip a`).
   - Loopback (`lo`): Local service coordination.
   - Primary VPC (`ens5`): `<private-vpc-subnet>`
   - Tailscale Overlay (`tailscale0`): `<overlay-ip>/32`
   - Docker Bridges: Subnets allocated in the `<docker-bridge-subnet>` - `<docker-bridge-subnet>` range.
2. **Listening Services:** Evaluated using socket statistics (`ss -ltnup`).
   - **Atlas Gateways:** Bound to `127.0.0.1` (Ports 8080, 8090).
   - **Control Plane HTTPS:** Bound exclusively to the Tailscale interface (`<overlay-ip>:443`).
   - **SSH Access:** Standard host SSH server present, supplemented by a local tunneling endpoint (`127.0.0.1:8022`).
3. **Egress & DNS:** 
   - Primary DNS routing uses local resolver (`169.254.169.254`) with public fallbacks (`1.1.1.1`, `8.8.8.8`).
   - Outbound HTTPS traffic (e.g., to cloud API providers) is fully operational and unblocked.

## Outcome
The baseline network discovery confirms that the deployment environment adheres to the principle of least privilege regarding network exposure. No unauthenticated public listeners were discovered, and the Tailscale overlay successfully isolates management traffic.

## Lessons Learned
- Explicitly mapping socket bindings ensures that internal orchestrators (like Atlas) do not unintentionally expose sensitive data to the wider VPC subnet.