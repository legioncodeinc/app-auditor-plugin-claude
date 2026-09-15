# font-family-no-duplicate-names | Stylelint

- URL: https://stylelint.io/user-guide/rules/font-family-no-duplicate-names/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## Rule Name and Purpose

`font-family-no-duplicate-names` - prevents duplicate font family names from appearing within `font` and `font-family` CSS properties.

## Description

The rule identifies when the same typeface is listed multiple times in a font stack. It applies to both the `font` and `font-family` properties while ignoring Sass, Less, and CSS custom property (`var(--custom-property)`) variable syntaxes.

## Examples of Incorrect Code

```css
a { font-family: 'Times', Times, serif; }
a { font: 1em "Arial", 'Arial', sans-serif; }
a { font: normal 14px/32px -apple-system, BlinkMacSystemFont, sans-serif, sans-serif; }
```

## Examples of Correct Code

```css
a { font-family: Times, serif; }
a { font: 1em "Arial", "sans-serif", sans-serif; }
a { font: normal 14px/32px -apple-system, BlinkMacSystemFont, sans-serif; }
```

## Secondary Option: ignoreFontFamilyNames

Accepts an array allowing specified font names or regex patterns to bypass duplicate detection:

```json
{
  "font-family-no-duplicate-names": [
    true,
    { "ignoreFontFamilyNames": ["/^My Font /", "monospace"] }
  ]
}
```

## Limitations

The rule "will stumble on unquoted multi-word font names and unquoted font names containing escape sequences." Quoting such names resolves detection issues.
