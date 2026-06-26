# Path Repair Copy Report

## Scope

- Canonical root: `/opt/data/home/control-plane`
- Non-canonical root: `/opt/data/control-plane`
- Action requested: copy Phase 3 framework files from non-canonical root into canonical root
- Constraints honored: copy only, no delete, no move, no symlinks, no config/service changes

## Discovery result

The requested non-canonical source tree does **not** exist on this host:

- `/opt/data/control-plane` → missing

Because the source root was absent, no Phase 3 framework files were available to copy.

## Files copied

- None

## Directories created

- None

## Files skipped

- All expected Phase 3 source files were skipped because the source directory `/opt/data/control-plane` was not present

## Backups made

- None

## Conflicts

- Source path conflict: requested source root was missing, so the copy operation could not proceed
- No canonical-file overwrite conflicts occurred because no source files were available

## Verification status

- Canonical control-plane root exists: `/opt/data/home/control-plane`
- No files were copied from `/opt/data/control-plane`
- No canonical files were changed by this operation
- Final verification status: **copy not possible; source root absent**

## Notes

- No deletion, movement, symlink creation, or configuration changes were performed
- No service restarts were performed
- No SSH, Tailscale, or Docker changes were performed
