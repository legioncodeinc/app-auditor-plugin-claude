# declaration-property-value-allowed-list | Stylelint

- URL: https://stylelint.io/user-guide/rules/declaration-property-value-allowed-list/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## Purpose

This rule enforces that only specified property-value combinations are permitted within CSS declarations. It specifies a list of allowed property and value pairs within declarations.

## Configuration Format

The rule accepts an object mapping property names to arrays of allowed values:

```
{ "property-name": ["array", "of", "values", "/regex/"] }
```

A regex can also be used for a property name, such as `{ "/^animation/": [] }`.

## Key Features

- Supports regex patterns for both property names (e.g. `"/^animation/"`) and values
- When a property name is found in the object, only its listed values are allowed, and the rule complains about all non-matching values
- If the property name is not included in the object, anything goes

## Important Regex Consideration

A regular expression value is matched against the entire value of the declaration, not specific parts of it. For example, a value like `"10px solid rgba( 255 , 0 , 0 , 0.5 )"` will not match `/^solid/` but will match `/\s+solid\s+/` or `/\bsolid\b/`.

Be careful with regex matching not to accidentally match quoted string values and `url()` arguments.

## Example Configuration

```json
{
  "declaration-property-value-allowed-list": {
    "/^(-webkit-)?transform$/": ["/scale/"],
    "whitespace": ["nowrap"],
    "/color/": ["/^green/"]
  }
}
```

## Valid CSS

```css
a { whitespace: nowrap; }
a { transform: scale(1, 1); }
a { color: green; }
```

## Invalid CSS

```css
a { whitespace: pre; }
a { transform: translate(1, 1); }
a { color: pink; }
```
