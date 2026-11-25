# Changelog

## Unreleased

### Added

- MkDocs Material documentation site on Read the Docs with installation, command,
  configuration, troubleshooting, development, and changelog pages.

## 1.3.0

### Added

- Unit tests for settings validation, progression maths, and the role reward cog.

### Changed

- Settings validation now rejects invalid Discord IDs and progression values outside
  `(0, 1]`.
- Reward checks validate server availability, role presence, **Manage Roles** permission,
  and role hierarchy before assigning any role.
- Settings are reloaded automatically when the settings row is saved or deleted in the
  Django admin panel.
- The manual command reports detailed counters for eligible, skipped, missing, and failed
  assignments.

## 1.1.0

### Added

- Documented configuration workflow and owner-only manual check.
- Legacy `hello` command alias for older installations.

## Earlier releases

Earlier `1.0.x` releases introduced the initial progression role reward package. For the
complete tag history, see the
[GitHub releases page](https://github.com/seiftheman/ballsdex-role-reward/releases).
