# color-named | Stylelint

- URL: https://stylelint.io/user-guide/rules/color-named/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## Rule Name and Purpose

The `color-named` rule requires or disallows named colors in CSS where applicable: "Require (where possible) or disallow named colors."

## Primary Options

### `"always-where-possible"`

This setting mandates using named colors whenever possible. The rule will flag hex codes (3, 4, 6, and 8 digit), `rgb()`, `rgba()`, `hsl()`, `hsla()`, `hwb()`, and `gray()` color values that have named equivalents.

Invalid patterns:
```css
a { color: #000; }
a { color: rgb(0, 0, 0); }
a { color: rgba(0, 0, 0, 0); }
a { color: hsl(0, 0%, 0%); }
```

Valid patterns:
```css
a { color: black; }
a { color: rgb(10, 0, 0); }
```

### `"never"`

This setting prohibits named colors entirely. All color values must use hex, rgb, or functional notation instead.

Invalid patterns:
```css
a { color: black; }
a { color: white; }
```

Valid patterns:
```css
a { color: #000; }
a { color: rgb(0, 0, 0); }
```

## Secondary Options

- `ignore`: Excludes colors inside functions from evaluation
- `ignoreFunctions`: Specifies functions where named colors should be ignored
- `ignoreProperties`: Allows named colors in specified properties

## Additional Notes

The rule supports up to two message arguments and ignores Sass (`$sass`) and Less (`@less`) variable syntaxes.
