# GitHub Repo Health Audit Report

**Repository:** `legioncodeinc/app-auditor-plugin-claude`
**Audit date:** 2026-09-22
**Data collection mode:** Local clone + `gh` CLI with authenticated repository and workflow read access
**Coverage gaps:** GitHub returned repository settings and branch-protection state. Organization-level default community files and organization rulesets were not audited.
**Audited by:** github-repo-health-wasp-drone

---

## Overall Score: 30/100

| # | Dimension | Raw Score | Weight | Weighted |
|---|---|---:|---:|---:|
| 1 | Branch protection / rulesets | 2/10 | 20% | 4.0 |
| 2 | Commit quality (Conventional Commits) | 3/10 | 15% | 4.5 |
| 3 | CODEOWNERS coverage | 0/10 | 15% | 0.0 |
| 4 | CI workflow density | 0/10 | 15% | 0.0 |
| 5 | Docs presence | 8/10 | 10% | 8.0 |
| 6 | Repository settings | 3/10 | 10% | 3.0 |
| 7 | Issue/PR templates | 10/10 | 8% | 8.0 |
| 8 | .gitignore coverage | 8/10 | 7% | 5.6 |
| | **Total** | | | **30.1** |

---

## Branching Strategy (qualitative)

**Observed strategy:** GitHub Flow. The only remote branch is `main`; the prior launch feature was squash-merged through PR #2 and its remote branch was deleted manually.
**Documented:** No branch strategy or naming convention is stated in `CONTRIBUTING.md`.
**Branch inventory:** 1 remote branch, 0 open pull requests, 0 stale remote branches.
**Assessment:** Practice is clean and short-lived, but enforcement and documentation are absent.

---

## Branch Protection / Rulesets (Score: 2/10)

**Enforcement mechanism:** None. `GET /rulesets` returned an empty array and the legacy protection endpoint returned `404 Branch not protected`.

| Rule | Status | Notes |
|---|---|---|
| `required_pull_request` | ❌ Disabled | Settings > Rules > Rulesets |
| `required_status_checks` | ❌ Disabled | No CI workflow currently exists |
| `non_fast_forward` | ❌ Disabled | Force-push prevention is not enforced |
| `dismiss_stale_reviews` | ❌ Disabled | No review rule exists |
| `required_linear_history` | ❌ Disabled | |
| `required_signatures` | ❌ Disabled | |

---

## Commit Quality - Conventional Commits (Score: 3/10)

| Metric | Value |
|---|---|
| CC-adherent commits | 1/4 (25%) |
| Average subject line length | 35 characters |
| Generic/noise commits | 1 (`Initial commit`) |
| Breaking changes documented | 0 |
| `commitlint` in CI | No |

The history is small. Future commits should use `feat:`, `fix:`, `docs:`, `test:`, `chore:`, or another Conventional Commits type.

---

## CODEOWNERS (Score: 0/10)

**Location:** Not present at `CODEOWNERS`, `.github/CODEOWNERS`, or `docs/CODEOWNERS`.
**Syntax errors:** Not applicable.
**Coverage:** 0% enforced ownership.
**Ownership type:** None.

---

## CI Workflow Density (Score: 0/10)

No `.github/workflows/*.yml` or `.yaml` file exists. Tests, syntax checks, archive builds, checksum verification, lockfile review, and security checks currently depend on a local operator.

| Workflow | Triggers | Quality | Type | Test | Build | Security | Timeout | In required checks |
|---|---|---|---|---|---|---|---|---|
| None | N/A | ❌ | N/A | ❌ | ❌ | ❌ | N/A | ❌ |

CI architecture is outside this audit. Hand off workflow design to `ci-release-wasp-drone`.

---

## Docs Presence (Score: 8/10)

| File | Present | Notes |
|---|---|---|
| `README.md` | ✅ | Quick start, downloads, requirements, safety, contribution, and license sections |
| `LICENSE.md` | ✅ | AGPL-3.0-or-later |
| `CONTRIBUTING.md` | ✅ | Setup, tests, validation, artifact rebuild, and PR expectations |
| `SECURITY.md` | ✅ | Responsible-disclosure guidance |
| `SUPPORT.md` | ✅ | Support and reproducible-report guidance |
| `CODE_OF_CONDUCT.md` | ❌ | Recommended community-health file is absent |

---

## Repository Settings (Score: 3/10)

| Setting | Status |
|---|---|
| Auto-delete head branches | ❌ Disabled |
| Allow merge commits | ✅ Enabled |
| Allow squash merging | ✅ Enabled |
| Allow rebase merging | ✅ Enabled |
| Allow auto-merge | ❌ Disabled |
| Secret scanning | ❌ Disabled |
| Push protection | ❌ Disabled |
| Dependabot security updates | ❌ Disabled |

These are external GitHub settings. This audit made no setting change.

---

## Issue/PR Templates (Score: 10/10)

| Item | Present | Substantive? |
|---|---|---|
| Bug report template | ✅ | ✅ Reproduction, expected/actual, runtime, OS, command, logs, safety checks |
| Feature request template | ✅ | ✅ Problem, outcome, use case, alternatives, privacy check |
| PR template | ✅ | ✅ Motivation, related issue, change type, verification, compatibility and safety |

The initial pass found `.github/ISSUE_TEMPLATE/bug_report.yml:14` still showing `1.0.0`; it was corrected to `1.1.0` before the final verification.

---

## .gitignore Coverage (Score: 8/10)

**Detected stack:** Node.js ESM browser-automation scripts with generated release archives intentionally tracked under `dist/`.
**Secret patterns:** Capture sessions, `auth.json`, `.session.json`, `.env`, and `.env.test` are covered. Broader `.env.*`, `*.pem`, and `*.key` patterns are not listed.
**Build artifacts:** `node_modules/`, caches, coverage, logs, and TypeScript build metadata are covered. `dist/` is intentionally tracked as the product distribution.
**Accidentally tracked files:** None detected.

---

## Prioritized Remediation Plan

| Priority | Finding | Impact | Effort | Action |
|---:|---|---:|---:|---|
| 1 | No default-branch protection | 5 | 1 | Create an active `main` ruleset under Settings > Rules > Rulesets after CI checks exist |
| 2 | Secret scanning and push protection disabled | 4 | 1 | Enable both under Settings > Security > Code security; security finding interpretation belongs to `security-wasp-drone` |
| 3 | No CODEOWNERS | 4 | 1 | Add `.github/CODEOWNERS` with a catch-all owner and explicit ownership for manifests, distributions, and future workflows |
| 4 | No CI workflow | 4 | 2 | Hand off test, syntax, build, checksum, archive, and dependency checks to `ci-release-wasp-drone` |
| 5 | Auto-delete merged branches disabled | 3 | 1 | Enable Settings > General > Pull Requests > Automatically delete head branches |
| 6 | All merge strategies enabled | 3 | 1 | Disable merge commits and retain squash, with rebase optional |
| 7 | Incomplete generic secret ignores | 3 | 1 | Add `.env.*` exceptions for examples plus `*.pem` and `*.key` to `.gitignore` |
| 8 | No documented branch or commit convention | 2 | 1 | Add GitHub Flow and Conventional Commits guidance to `CONTRIBUTING.md` |
| 9 | Missing code of conduct | 2 | 1 | Add `CODE_OF_CONDUCT.md` if the project wants public-community participation |

**Handoffs to other Drones:**

- `ci-release-wasp-drone`: CI workflow architecture and required-check names.
- `security-wasp-drone`: interpretation of any future secret-scanning or Dependabot alerts.
- `readme-writing-wasp-drone`: no handoff required; README structure is complete.

---

*Report generated by `github-repo-health-wasp-drone` using `github-repo-health-stinger`.*
