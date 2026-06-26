# Roadmap

## Phase 5
- Build a minimal, durable control-plane foundation for fleet operations.
- Keep the phase documentation-first and read-only by default.

## Milestones
- SSH client setup
  - Define the approved client-side SSH posture for managed machines.
  - Keep host daemon configuration out of scope.
- Fleet inventory
  - Create a structured inventory model for current and future machines.
  - Seed it with the canonical Hermes host.
- Desktop onboarding
  - Document the workflow for bringing a new desktop under management.
  - Capture transport, approval level, and recovery expectations.
- Health monitoring
  - Define the standard health report fields and evidence requirements.
  - Keep the format consistent across Hermes, OpenClaw, and future hosts.
- Daily reports
  - Produce regular human-readable summaries of health and drift.
  - Store them in the reports directory.
- Remote maintenance
  - Define approved remote maintenance boundaries and verification steps.
  - Prefer safe, reversible actions and explicit evidence.
- Automation library
  - Build reusable scripts and playbooks for common read-only operations.
  - Keep the library in user-space and versioned in the control plane.
