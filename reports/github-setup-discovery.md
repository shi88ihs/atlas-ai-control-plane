# GitHub Setup Discovery

## Git Repository Status
- **Current branch:** `master`
- **Current remotes:** None configured.
- **Number of tracked files:** 46
- **Ignored files:** 
  - `logs/`
  - `backups/`
  - `sessions/`
  - `pycache/`
  - `__pycache__/`
  - `*.pyc`
  - `*.db`
  - `*.db-wal`
  - `*.db-shm`
  - `.env`
  - `auth.json`
  - `*.pem`
  - `*.key`
  - `reports/health-report-*.md`
  - `reports/latest-health-report.md`
  - `reports/doctor-*.md`

## Tooling & Identity
- **Git:** Installed (`git version 2.50.1`)
- **GitHub CLI (`gh`):** Not installed.
- **SSH:** Installed (`OpenSSH_8.7p1`)
- **Git Identity:** Not configured (`user.name` and `user.email` are empty).

## SSH & Connectivity
- **Existing SSH Keys:** Found `/home/atlas-admin/.ssh/hermes_local_pc_ed25519` (Private and Public). 
- **GitHub Connectivity:** Failing (`git@github.com: Permission denied (publickey)`).

## Recommended Safest Setup Path

To safely set up GitHub access without overwriting existing keys, exposing tokens, or messing up current configurations, follow these steps:

1. **Install GitHub CLI (`gh`) & Set Git Identity:**
   Install `gh` using the package manager, then configure your Git identity.
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **GitHub CLI browser/device login:**
   Run the following command to authenticate securely without generating manual tokens.
   ```bash
   gh auth login
   ```
   - **Account:** `GitHub.com`
   - **Protocol:** `SSH`
   - **Authenticate:** Choose **Login with a web browser** (device code).

3. **SSH key upload:**
   During the `gh auth login` setup, it will ask if you want to generate a new SSH key. 
   - Answer **Yes**. 
   - **Important:** Ensure it creates a *new* key (e.g., `id_ed25519` or `github_ed25519`). Do **not** overwrite the existing `/home/atlas-admin/.ssh/hermes_local_pc_ed25519` key. The CLI will automatically upload the newly generated public key to your GitHub account.

4. **Remote creation:**
   Once authenticated, create the remote repository directly from the server.
   ```bash
   cd /opt/data/home/control-plane
   gh repo create control-plane --private --source=. --remote=origin
   ```

5. **First push:**
   Push your initial commit to GitHub.
   ```bash
   git push -u origin master
   ```