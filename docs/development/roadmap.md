# Commercial Roadmap

Atlas is actively evolving from a single-node coordination layer into a comprehensive, fleet-wide AI operations platform. 

## Phase 1: Stabilization (Current)
- [x] Unify deployment under user-level `systemd`.
- [x] Establish GitOps tracking for infrastructure reports.
- [x] Implement read-only diagnostics (Atlas Doctor).

## Phase 2: Fleet Management
- [ ] **Multi-Node Telemetry:** Aggregate health metrics from geographically dispersed AI nodes into a single control plane.
- [ ] **Remote Command Execution:** Safely deploy configuration updates to fleets of agents via structured, signed payloads.
- [ ] **Global Dashboard:** A web-based visual interface for tracking the active tasks and resource consumption of all managed runtimes.

## Phase 3: Policy and Compliance
- [ ] **Automated Guardrails:** Pre-execution dry-runs that predict the impact of an AI's proposed action on the host environment.
- [ ] **Audit Export:** Compliance-ready logging exports for enterprise security review.
- [ ] **Identity Federation:** Integration with enterprise SSO (OIDC/SAML) for dashboard access.

## Phase 4: Auto-Scaling
- [ ] **Ephemeral Worker Pools:** Allow primary orchestrator agents to dynamically spin up short-lived, isolated compute instances to parallelize tasks.
- [ ] **Cost-Aware Scheduling:** Automatically route expensive LLM inference tasks to the most cost-effective provider available in the environment.