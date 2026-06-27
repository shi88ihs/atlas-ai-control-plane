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

## [0.9.0] - 2026-06-27
### Added
- **Internal Development Release**
- Migrated from legacy Docker containers to native `systemd` user services.
- Added `status` engine to collect read-only telemetry.
- Introduced `doctor` module to verify Google ADC and Vertex AI paths.
- Bootstrapped initial Git repository and `.gitignore` constraints.