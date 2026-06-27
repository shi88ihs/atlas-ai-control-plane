# GitHub Setup Discovery

## Purpose
Assess the deployment environment's readiness for Git integration, identifying existing SSH key material, authentication state, and configuration artifacts to plan a safe onboarding sequence.

## Summary
The discovery phase identified that while basic Git binaries were installed, the environment lacked the specific authentication material and CLI utilities (`gh`) necessary for automated, secure synchronization with GitHub. The assessment concluded that a dedicated deploy key and a strict SSH config were required to proceed without conflicting with existing local keys.

## Architecture
- **Version Control:** `git` (verified present)
- **Credential Storage:** SSH (`~/.ssh/`)
- **CLI Utility:** GitHub CLI (`gh`) (targeted for installation)
- **Target Remote:** `github.com`

## Implementation
1. **Binary Check:** Validated the presence and version of the Git executable.
2. **Key Material Audit:** Scanned `~/.ssh/` for existing keys. Found a legacy local key, dictating the need for a distinct identity (e.g., `github_ed25519`) specifically for repository interactions.
3. **Connectivity Test:** Attempted anonymous connection to GitHub, confirming the network path is open but properly restricts unauthenticated access (`Permission denied (publickey)`).
4. **Tooling Assessment:** Determined that the GitHub CLI (`gh`) was not installed, which is required to securely bootstrap device-flow authentication and key upload without exposing passwords to the shell.

## Outcome
A precise action plan was generated. The plan specified the exact sequence required to install the GitHub CLI, generate a new Ed25519 keypair, configure the SSH `config` file for discrete identity matching, and authorize the environment using OAuth device flow.

## Lessons Learned
- Blindly generating SSH keys on production infrastructure can overwrite existing operational credentials. A rigorous discovery phase prevents destructive overwrites and ensures multi-key environments are handled elegantly using `IdentitiesOnly`.