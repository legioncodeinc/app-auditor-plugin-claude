# unit-allowed-list | Stylelint

- URL: https://stylelint.io/user-guide/rules/unit-allowed-list/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## Rule Name and Purpose

`unit-allowed-list` - "Specify a list of allowed units."

This rule restricts CSS to only designated measurement units, targeting the unit portion of values like `100px` or `5s`. It supports 1 message argument: the disallowed unit. You can also ignore units in the values of declarations with specified properties.

## Primary Option: Array<string>

Configuration accepts an array of permitted units:

```json
{ "unit-allowed-list": ["px", "em", "deg"] }
```

Incorrect patterns:
```css
a { width: 100%; }        /* % not allowed */
a { font-size: 10rem; }   /* rem not allowed */
a { animation: animation-name 5s ease; }  /* s not allowed */
```

Correct patterns:
```css
a { font-size: 1.2em; }
a { line-height: 1.2; }   /* unitless values permitted */
a { height: 100px; }
a { transform: rotate(30deg); }
```

## Secondary Options

### ignoreProperties

Exempts specific units from restrictions within designated properties:

```json
{
  "unit-allowed-list": ["px", "em"],
  "ignoreProperties": {
    "rem": ["line-height", "/^border/"],
    "%": ["width"]
  }
}
```

### ignoreFunctions

Bypasses restrictions for units within specified functions:

```json
{
  "unit-allowed-list": ["px", "em"],
  "ignoreFunctions": ["/^hsl/", "calc"]
}
```
