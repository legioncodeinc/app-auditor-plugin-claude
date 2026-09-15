# Supported secret scanning patterns - GitHub Docs

- URL: https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): not shown on fetched content (page is continuously updated by GitHub)

## Alert Types

GitHub's secret scanning identifies three alert types:
- **User alerts**: reported to users in the Security tab of the repository when a supported secret is detected
- **Push protection alerts**: reported when a contributor bypasses push protection
- **Partner alerts**: sent directly to secret providers that are part of secret scanning's partner program; not reported in the Security tab

## Pattern Categories

Patterns fall into three groups:

1. **Generic patterns**: "Secrets not tied to a specific provider, such as private keys and database connection strings," detected via regex-based matching. Sample generic patterns: `rsa_private_key`, `ec_private_key`, `openssh_private_key`, `mongodb_connection_string`, `postgres_connection_string`, all marked with high precision.

2. **AI-detected patterns**: "Passwords and other unstructured secrets detected using AI models." These support user alerts but lack push protection and validity checks.

3. **Provider patterns**: "Secrets tied to a specific service provider (such as AWS, Azure, Stripe)," identified via regex-based detection. Provider patterns typically offer the broadest support: partner notifications, default push protection, validity checks, extended metadata, and some Base64 format handling.

## Sample Supported Patterns (representative rows from the full table)

| Provider | Secret | Push Protection | Validity Check |
|----------|--------|-----------------|-----------------|
| 1Password | 1Password Service Account Token | Yes | No |
| Adafruit | Adafruit IO Key | Yes | Yes |
| Amazon AWS | Amazon AWS Access Key ID | Yes | Yes |
| Anthropic | Anthropic API Key | Yes | Yes |
| Azure | Azure OpenAI Key | Yes | No |
| Discord | Discord Bot Token | Yes | Yes |
| GitHub | GitHub Personal Access Token | Yes | Yes |
| Google | Google Cloud Service Account Credentials | Yes | Yes |
| Mailgun | Mailgun API Key | Yes | Yes |
| OpenAI | OpenAI API Key | Yes | Yes |
| Slack | Slack API Token | Yes | Yes |
| Stripe | Stripe API Key | Yes | Yes |
| Twilio | Twilio API Key | Yes | No |
| Vercel | Vercel Personal Access Token | Yes | No |
| Yandex | Yandex.Cloud API Key | Yes | Yes |

(This is a representative subset; the full table on the live page lists many more providers and token types, plus "Token versions" for patterns supporting multiple token formats across providers like GitHub, AWS, and Google.)

## Relevance to redaction regexes

These categories (generic private-key/connection-string patterns, and named provider token patterns like `sk-...` for OpenAI, `xox[baprs]-...` for Slack, AWS `AKIA...` access key IDs, etc.) are a useful grounding reference when building redaction regexes for a capture tool: at minimum, redact anything matching a private key block, a database connection string, or a named provider token pattern before it is written to a screenshot, log, or report.
