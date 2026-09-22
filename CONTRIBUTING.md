# Contributing to Audit My App with Claude

Thanks for helping improve the `webapp-capture` plugin.

## Before you start

- Search existing issues before opening a new one.
- Keep changes focused on the plugin, its capture workflow, documentation, or verified compatibility fixes.
- Never commit credentials, saved browser sessions, customer data, or private screenshots.
- Use a synthetic or deliberately public demo app for examples and fixtures.

## Local setup

Requirements:

- Node.js 20.9 or newer
- `zip`
- Claude Code for plugin validation
- Chromium and FFmpeg only for capture or demo-video work

Install the script dependencies:

```bash
cd plugins/webapp-capture/skills/webapp-capture-stinger/scripts
npm ci
```

## Validate and build

From the repository root:

```bash
(cd plugins/webapp-capture/skills/webapp-capture-stinger/scripts && npm test)
claude plugin validate .
claude plugin validate ./plugins/webapp-capture
tools/build-dist.sh
(cd dist && shasum -a 256 -c SHA256SUMS)
```

Run the doctor when a change affects runtime setup:

```bash
node plugins/webapp-capture/skills/webapp-capture-stinger/scripts/doctor.mjs
```

The build script recreates `dist/webapp-capture-plugin-<version>.zip`, `dist/webapp-capture-stinger-<version>.skill`, and `dist/SHA256SUMS`. Do not edit archive contents or checksums by hand. Commit rebuilt distributions only when their source content or release metadata changed.

## Pull requests

- Explain the user-facing problem and the behavior you changed.
- Link the related issue when one exists.
- Include the validation commands you ran and their actual results.
- Update documentation and `plugins/webapp-capture/CHANGELOG.md` when behavior changes.
- Call out compatibility or safety implications.
- Keep unrelated cleanup out of the pull request.

By contributing, you agree that your contribution is licensed under AGPL-3.0-or-later.
