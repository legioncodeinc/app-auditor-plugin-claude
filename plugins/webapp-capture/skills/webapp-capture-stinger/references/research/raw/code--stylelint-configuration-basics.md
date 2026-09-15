# Configuring | Stylelint

- URL: https://stylelint.io/user-guide/configure/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## What Is a Configuration?

Stylelint requires a configuration object that defines rules and settings for linting CSS. The tool searches upward from the current working directory for a `stylelint.config.js` file by default, though you can specify an alternate location via the `--config` flag.

Supported configuration file formats include:
- `stylelint.config.js`, `stylelint.config.mjs`, `stylelint.config.cjs`, or `stylelint.config.ts`
- Legacy formats: `.stylelintrc.js`, `.stylelintrc.json`, `.stylelintrc.yml`, or `stylelint` property in `package.json`

## Configuration Structure

### Rules Property

The `rules` object contains rule names as keys and their configurations as values. No rules are turned on by default. Each rule accepts:
- `null` (disabled)
- A single value (primary option)
- An array with two values `[primary option, secondary options]`

Example:

```javascript
{
  "rules": {
    "color-no-invalid-hex": true,
    "unit-allowed-list": ["em", "rem", "%", "s"],
    "selector-pseudo-class-no-unknown": [
      true,
      { "ignorePseudoClasses": ["global"] }
    ]
  }
}
```

#### Secondary Options

Rules support several secondary configuration properties:

- `disableFix`: Disables autofix for specific rules
- `message`: Delivers custom violation messages (supports functions with arguments)
- `url`: Provides custom documentation links
- `severity`: Sets level as `"warning"` or `"error"` (can use functions)
- `reportDisables`: Reports `stylelint-disable` comments for enforcement

### Extends Property

Configurations can extend other shared configs, allowing inheritance and overrides:

```javascript
{
  "extends": "stylelint-config-standard",
  "rules": {
    "alpha-value-notation": "number"
  }
}
```

Multiple configs can be extended as an array, with later entries overriding earlier ones. Locators can be npm module names, absolute paths, or relative paths.

### Plugins Property

Plugins add custom rules beyond Stylelint's built-in set:

```javascript
{
  "plugins": ["../special-rule.js"],
  "rules": {
    "plugin-namespace/special-rule": "everything"
  }
}
```

Plugins are declared as an array, then their rules are configured within the `rules` object using their namespaced names. This is the mechanism used by third-party plugins such as `stylelint-declaration-strict-value` (namespace `scale-unlimited`).

### Overrides Property

Apply configuration selectively to file patterns:

```javascript
{
  "rules": { "alpha-value-notation": "number" },
  "overrides": [
    {
      "files": ["*.scss", "**/*.scss"],
      "customSyntax": "postcss-scss"
    },
    {
      "files": ["components/**/*.css"],
      "rules": { "alpha-value-notation": "percentage" }
    }
  ]
}
```

Each override must include a `files` property (glob patterns) and at least one configuration property. Multiple overrides are applied in order, with later blocks taking precedence.

### IgnoreFiles Property

Exclude specific files from linting via glob patterns:

```javascript
{
  "ignoreFiles": ["**/*.js"]
}
```

Note: this method is inefficient for ignoring many files; use `.stylelintignore` instead.

## Additional Key Properties

- `languageOptions`: Customize CSS syntax (at-rules, properties, types, units) and directionality
- `customSyntax`: Specify syntax for non-standard CSS
- `cache`: Store results for changed files only
- `fix`: Enable automatic problem correction
- `maxWarnings`: Set acceptable warning limit
- `defaultSeverity`: Apply default severity to all rules

## Example Configuration

```javascript
/** @type {import('stylelint').Config} */
export default {
  rules: {
    "block-no-empty": true
  }
};
```
