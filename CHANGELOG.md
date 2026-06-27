# Changelog

All notable changes to the Atlas AI Control Plane will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Fleet Management dashboard placeholder.
- Multi-node telemetry integration.

## [1.0.0] - Planned
### Added
- **Public Preview Release**
- Full documentation suite (`docs/architecture`, `docs/deployment`, etc.).
- Stabilized `control-plane` CLI wrapper.
- Structured Markdown reporting for deployment verification.
- Read-only diagnostics via Atlas Doctor.

## [0.9.1] - 2026-06-27
**Infrastructure Stabilization Release**

This release hardens the deployment environment and prepares the final production web cutover. For full details, see the [v0.9.1 Release Notes](docs/releases/v0.9.1.md).

### Added
- Mission Control dashboard foundation.
- AWS Manager skill draft.
- Memory optimization profile.
- Backup and release workflow.
- Production web stack (Caddy, Vaultwarden, static site) prepared.

### Changed
- Atlas documentation restructured to portfolio-grade open-source standards.
- Legacy Docker runtimes deprecated in favor of native systemd user services.
- Tightened GitOps security boundaries and `.gitignore` policies.

### Known Outstanding Work
- Final Caddy production cutover (pending DNS).
- HTTPS certificate verification.
- Public website deployment completion.
- Vultr retirement after monitoring.

## [0.9.0] - 2026-06-27
### Added
- **Internal Development Release**
- Migrated from legacy Docker containers to native `systemd` user services.
- Added `status` engine to collect read-only telemetry.
- Introduced `doctor` module to verify Google ADC and Vertex AI paths.
- Bootstrapped initial Git repository and `.gitignore` constraints.