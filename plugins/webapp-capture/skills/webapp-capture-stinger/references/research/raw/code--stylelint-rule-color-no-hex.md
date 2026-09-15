# color-no-hex | Stylelint

- URL: https://stylelint.io/user-guide/rules/color-no-hex/
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown

## Rule Name and Purpose

`color-no-hex` - "Disallow hex colors."

Message argument: the rule supports 1 message argument representing the disallowed hex color.

## Incorrect Code Examples

```css
a { color: #333 }
a { color: #000; }
a { color: #fff1aa; }
a { color: #123456aa; }
a { color: #foobar; }
a { color: #0000000000000000; }
```

## Correct Code Examples

```css
a { color: black; }
a { color: rgb(0, 0, 0); }
a { color: rgba(0, 0, 0, 1); }
```

## Configuration Options

Basic:
```json
{ "color-no-hex": true }
```

With secondary options:
```javascript
{
  "color-no-hex": [true, { "ignoreFunctions": ["var", "/^--/"] }]
}
```

The `ignoreFunctions` option allows hex colors within specified functions. For example, with the configuration above, these patterns are acceptable:

```css
a { color: var(--foo, #fff); }
a { color: --foo(#fff); }
```
