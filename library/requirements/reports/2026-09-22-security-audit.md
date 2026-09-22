# Security audit - 2026-09-22 - webapp-capture 1.1.0

## Executive summary

- Scope: the complete working diff on `main`, with emphasis on onboarding mutations, recursive route discovery, handoff packaging, dependency changes, generated distributions, and credential handling.
- Coverage: reduced coverage. This repository is a Node.js browser-automation plugin rather than the SvelteKit, Neon, WorkOS, Stripe, Vercel, Doppler, and GoHighLevel application stack targeted by `security-stinger`. Applicable secrets, filesystem, browser-side-effect, archive, dependency, and supply-chain surfaces received a full pass.
- Findings before remediation: 0 Critical, 0 High, 3 Medium, 0 Low.
- Findings after remediation: 0 open findings.
- Ship Gate status: cleared to proceed to `quality-stinger`.

## Surface coverage checklist

### SvelteKit attack surface

Not applicable. The repository contains no SvelteKit application routes or configuration.

### Authorization and tenancy (Drizzle / Neon)

Not applicable. The repository contains no database or tenant data layer.

### Secrets and environment

No open finding. No committed `.env` file was found in the working tree or Git history. Credential-pattern scans found no credential value. Onboarding now rejects secret-looking declared values and live fields before filling them.

### Webhooks and third-party intake

Not applicable. The repository contains no webhook handler.

### Dependencies and supply chain

No open finding. The Sharp 0.35.4 lockfile change matches the direct dependency update. Every resolved package URL uses `https://registry.npmjs.org/`, no resolved dependency declares an install script, and `npm audit --package-lock-only --audit-level=high` reported `found 0 vulnerabilities`.

### Headers and transport

Not applicable. The repository does not deploy an HTTP service.

### AI-generated code patterns

Three Medium findings were fixed before this report. The full updated diff was re-evaluated afterward.

### PII and logging hygiene

No open finding. The changed scripts do not add application telemetry or log onboarding field values. Screenshots continue to use configured masks.

## Findings detail

### [MEDIUM] Onboarding environment was advisory only

- **Location:** `plugins/webapp-capture/skills/webapp-capture-stinger/scripts/lib/onboarding.mjs:35`
- **Surface:** AI-generated code patterns and external side effects.
- **Description:** The unfinished implementation required `approved: true` but did not reject a production onboarding plan in code.
- **Evidence:** The prior gate began with `if (plan.approved !== true)` and had no environment validation.
- **Remediation:** `validateOnboardingPlan` now accepts only `local` or `seeded`; any other environment is refused before navigation.
- **Status:** fixed in this session.

### [MEDIUM] Recursive discovery could follow destructive-looking routes

- **Location:** `plugins/webapp-capture/skills/webapp-capture-stinger/scripts/lib/common.mjs:23`
- **Surface:** Browser side effects.
- **Description:** Same-origin filtering and a caller-maintained exclusion list did not protect against a destructive action exposed incorrectly through a GET link.
- **Evidence:** The prior crawler excluded only exact configured paths and the login path.
- **Remediation:** All discovery modes now apply a built-in destructive-route segment denylist in addition to `routes.exclude`.
- **Status:** fixed in this session.

### [MEDIUM] Handoff context accepted arbitrary files

- **Location:** `plugins/webapp-capture/skills/webapp-capture-stinger/scripts/inventory/design-handoff.mjs:130`
- **Surface:** Secrets and artifact packaging.
- **Description:** An explicitly supplied context path could copy a session, credential, key, binary, symlink, or other sensitive file into a handoff archive intended for upload.
- **Evidence:** The prior loop used `fs.copyFileSync(file, path.join(root, "context", path.basename(file)))` after only checking that the source was a file.
- **Remediation:** Context packaging now rejects symlinks, sensitive filenames, non-text formats, duplicate basenames, files over 5 MB, and content matching configured redaction patterns.
- **Status:** fixed in this session.

## Remediation summary

| Severity | Count | Fixed this session | Documented only |
|---|---:|---:|---:|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 3 | 3 | 0 |
| Low | 0 | 0 | 0 |

## Re-evaluation

A full applicable-surface re-evaluation ran after all three fixes. Results: 4 of 4 Node tests passed, all 23 `.mjs` files passed `node --check`, `git diff --check` passed, credential and `.env` history scans were clean, the lockfile registry allowlist passed, no dependency install scripts were present, and npm reported zero known vulnerabilities.

## Next step

Security is cleared. Proceed to `quality-stinger`; no security blocker remains.
