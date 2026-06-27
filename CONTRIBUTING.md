# Contributing to Atlas AI Control Plane

Thank you for your interest in contributing! Atlas is built to be a robust, professional platform.

## Development Workflow
1. **Fork the Repository:** Create your own fork and branch off `master`.
2. **Local Environment:** You do not need a dedicated cloud host to test changes. The `scripts/control-plane` CLI and read-only diagnostics run safely on local Linux/macOS environments.
3. **Commit Convention:** Use clear, descriptive commit messages. We recommend the Conventional Commits standard (e.g., `feat:`, `fix:`, `docs:`).

## Pull Request Expectations
- **Keep it focused:** Submit PRs that address a single concern, bug, or feature.
- **Pass the Doctor:** Ensure that running `control-plane doctor` locally does not raise new warnings introduced by your change.
- **Explain the "Why":** Provide context in the PR description detailing the problem being solved.

## Coding Standards
- **Python:** Use `black` and `isort` for formatting, and `flake8` for imports. Type hints are highly encouraged.
- **Bash/Shell:** Use `shellcheck` to validate scripts. Avoid Bash-isms if POSIX `sh` is sufficient, though `bash` is acceptable for complex arrays/logic.

## Documentation Expectations
- **Markdown Native:** All operational logs, reports, and architecture specs must be written in Markdown.
- **Sanitize Secrets:** NEVER commit API keys, IP addresses, or internal hostnames. Use `<placeholders>` as demonstrated in `SECURITY_PUBLICATION_CHECKLIST.md`.
- **Update the Changelog:** If you add a feature, please include a note in the `[Unreleased]` section of `CHANGELOG.md`.