# Core Features

## 1. Unified Health Monitoring (Atlas Doctor)
Atlas continuously monitors the deployment environment, offering real-time insights into system health, API reachability, memory usage, and Docker availability. It achieves this entirely through read-only probes, guaranteeing zero state drift during observation.

## 2. Secure Execution Boundaries
Atlas relies on native Linux user-space separation (`systemd --user`) rather than complex virtualization. This enforces strict privilege boundaries, preventing AI runtimes from escalating to root while still allowing them to manage their own ephemeral Docker containers.

## 3. Deployment Verification & Reporting
Every operational change or environmental discovery is recorded in structured Markdown reports. This creates an immutable, human-readable audit trail that tracks infrastructure evolution over time.

## 4. GitOps-Native Workflow
The entire control plane—including scripts, reports, and templates—lives in a Git repository. Atlas treats documentation as code, allowing operators to peer review infrastructure changes and roll back operational state seamlessly.

## 5. Overlay Networking Integration
Atlas natively understands secure overlay networks (like Tailscale), ensuring that sensitive management endpoints and diagnostic dashboards are never exposed to the public internet.