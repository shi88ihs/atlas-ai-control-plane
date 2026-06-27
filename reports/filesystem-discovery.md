# Filesystem Discovery

## Paths investigated

- `/opt/data`
- `/opt/data/home`
- `/opt/data/control-plane`
- `/home`
- `/home/atlas-admin`

## Existence and layout

Observed results:

- `/opt/data` exists
- `/opt/data/home` exists
- `/opt/data/control-plane` does not exist
- `/home` exists
- `/home/atlas-admin` exists

Additional evidence:

- `/opt/data` and `/opt/data/home` are regular directories owned by `root:root`
- `/home/atlas-admin` is owned by `atlas-admin:atlas-admin`
- `/opt/data/home/control-plane` exists and is owned by `atlas-admin:atlas-admin`
- `/home/atlas-admin` is the passwd-defined home directory for `atlas-admin`
- The runtime HOME environment variable points to `/home/atlas-admin/.hermes/home`

## Symlinks and bind mounts

For the inspected paths:

- No symlink behavior was observed
- No separate mountpoints were reported by `findmnt` for the inspected paths
- The paths appear to be ordinary directories on the host filesystem

## Canonical Control Plane root

**Recommended canonical workspace: `/opt/data/home/control-plane/`**

### Why this is the best canonical root

- It already exists and is structured for control-plane work
- It is owned by `atlas-admin`, so the runtime user can work there without host-wide changes
- It cleanly separates user-space control-plane artifacts from the login home directory
- It is specific enough to avoid ambiguity between the host home path and the runtime HOME path

### Why not the other candidates

- `/opt/data/control-plane` — does not exist in this environment
- `/opt/data/home` — too broad; this is just the parent container
- `/home` — host-wide and not specific to the control plane
- `/home/atlas-admin` — too broad; this is the user home, not the control-plane workspace

## Permissions

Observed current permissions:

- `/opt/data/home/control-plane` — `drwxr-xr-x`, owned by `atlas-admin:atlas-admin`
- `/home/atlas-admin` — `drwx------`, owned by `atlas-admin:atlas-admin`
- Existing reports files were normalized to `0644`

## Notes

- This discovery pass did not modify filesystem configuration.
- The control-plane root recommendation is based on the already-established workspace, ownership, and scope separation.
