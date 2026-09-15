# OWASP Secrets Management Cheat Sheet

- URL: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): not shown on fetched content

## What Constitutes a Secret

The guide identifies secrets as sensitive credentials requiring protection, including:
- API keys and database credentials
- Identity and Access Management (IAM) permissions
- SSH keys and certificates
- Authentication tokens
- Encryption keys
- Connection strings and passwords

## Fundamental Management Principles

**Centralization and standardization**: Organizations must consolidate secrets management through dedicated solutions rather than scattering them across configuration files. "Standardize and centralize the secrets management solution with care."

**Never hardcode or log secrets**: "Secrets must never be retrievable by everyone and everything." Plaintext storage in source code, configuration files, or logs creates unacceptable exposure risks.

**Access control via least privilege**: "Engineers should not have access to all secrets," requiring fine-grained permissions at individual secret levels rather than blanket access.

## Secret Detection and Prevention

The guide recommends:
- Pre-commit hooks and IDE-level detection to prevent secrets from entering repositories
- Tools like Yelp Detect Secrets for signature-based scanning
- Shift-left DevSecOps practices catching secrets before commit
- Multiple detection utilities to reduce false negatives

## Lifecycle Management

- **Rotation**: Regular automated rotation ensures compromised credentials have limited usability windows. Automation reduces human error.
- **Immediate revocation**: Upon compromise detection, secrets require rapid de-authorization and replacement through automated processes.
- **Expiration policies**: Secrets should expire after defined periods appropriate to their risk classification.
- **Auditing**: Comprehensive logging tracks who accessed secrets, when, and from where, which is essential for incident response.
