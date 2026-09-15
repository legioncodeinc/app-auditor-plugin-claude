# OWASP Logging Cheat Sheet

- URL: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): not shown on fetched content

## Key Principle

"Never log data unless it is legally sanctioned."

## Data That Should NOT Be Recorded Directly In Logs

The cheat sheet lists these items as data that "should usually not be recorded directly in the logs":

- Application source code
- Session identification values (hash instead if needed)
- Access tokens
- Sensitive personal data and PII (health records, government IDs)
- Authentication passwords
- Database connection strings
- Encryption keys and primary secrets
- Bank account or payment card data
- Commercially-sensitive information
- Information users opted out of or did not consent to have collected

## Additional Sensitive Data Needing Special Handling

Items that "may also need to be treated in some special manner":

- File paths
- Internal network names/addresses
- Non-sensitive personal data (names, phone numbers, email addresses)

## Log Injection Prevention

"Perform sanitization on all event data to prevent log injection attacks e.g. carriage return (CR), line feed (LF) and delimiter characters" to prevent attackers from manipulating log structures.

## Handling Sensitive Data When Some Logging Is Required

The guidance advocates using "personal data de-identification techniques such as deletion, scrambling or pseudonymization" when individual identity isn't required for the logging purpose.
