# Filesystem Discovery

## Paths investigated

- `/opt/data`
- `/opt/data/home`
- `/opt/data/control-plane`
- `/home`
- `/home/ec2-user`

## Existence and layout

Observed results:

- `/opt/data` exists
- `/opt/data/home` exists
- `/opt/data/control-plane` does not exist
- `/home` exists
- `/home/ec2-user` exists

Additional evidence:

- `/opt/data` and `/opt/data/home` are regular directories owned by `root:root`
- `/home/ec2-user` is owned by `ec2-user:ec2-user`
- `/opt/data/home/control-plane` exists and is owned by `ec2-user:ec2-user`
- `/home/ec2-user` is the passwd-defined home directory for `ec2-user`
- The runtime HOME environment variable points to `/home/ec2-user/.hermes/home`

## Symlinks and bind mounts

For the inspected paths:

- No symlink behavior was observed
- No separate mountpoints were reported by `findmnt` for the inspected paths
- The paths appear to be ordinary directories on the host filesystem

## Canonical Control Plane root

**Recommended canonical workspace: `/opt/data/home/control-plane/`**

### Why this is the best canonical root

- It already exists and is structured for control-plane work
- It is owned by `ec2-user`, so the runtime user can work there without host-wide changes
- It cleanly separates user-space control-plane artifacts from the login home directory
- It is specific enough to avoid ambiguity between the host home path and the runtime HOME path

### Why not the other candidates

- `/opt/data/control-plane` — does not exist in this environment
- `/opt/data/home` — too broad; this is just the parent container
- `/home` — host-wide and not specific to the control plane
- `/home/ec2-user` — too broad; this is the user home, not the control-plane workspace

## Permissions

Observed current permissions:

- `/opt/data/home/control-plane` — `drwxr-xr-x`, owned by `ec2-user:ec2-user`
- `/home/ec2-user` — `drwx------`, owned by `ec2-user:ec2-user`
- Existing reports files were normalized to `0644`

## Notes

- This discovery pass did not modify filesystem configuration.
- The control-plane root recommendation is based on the already-established workspace, ownership, and scope separation.
