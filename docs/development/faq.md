# Frequently Asked Questions

### Is Atlas an AI Agent?
No. Atlas is the *infrastructure and operations platform* that manages, monitors, and secures AI agents. Think of Atlas as the Kubernetes for autonomous AI.

### Which agents does Atlas support?
Atlas currently provides deep integration for the Hermes and OpenClaw runtimes, but its architecture is designed to support any process capable of executing on a standard Linux host or within a Docker container.

### Why not just use Kubernetes?
Kubernetes is excellent for stateless microservices but struggles with the unique requirements of autonomous AI agents, which often need direct access to host-level utilities, persistent state, and dynamic networking. Atlas provides a lighter, more targeted abstraction specifically tailored for Agent Ops.

### Can I run Atlas locally?
Yes. While Atlas is designed for remote server deployments, its reliance on standard Linux tools and user-space execution means it can run effectively on local workstations or VMs during the development phase.

### How does Atlas handle secrets?
Atlas does not store secrets in the repository. It expects credentials to be injected via secure local configuration files (`.env`, Google ADC, etc.) that are strictly ignored by version control. The Atlas status engine will verify the presence of these files without reading their contents.