# stylelint-declaration-strict-value

- URL: https://github.com/AndyOGo/stylelint-declaration-strict-value
- Fetched: 2026-09-15
- Source type: README
- Last updated (if shown): unknown

## Purpose

A [stylelint](https://github.com/stylelint/stylelint) plugin that enforces either variables (`$sass`, `namespace.$sass`, `@less`, `var(--cssnext)`, `css-loader @value`), functions or custom CSS values, like keywords (`inherit`, `none`, `currentColor` etc.), colors (`#fff`, `red`, etc.) or numbers incl. units (`0`, `1px`, `100%`, etc.) for CSS longhand and experimental shorthand properties.

## Installation

```bash
npm install stylelint-declaration-strict-value
```

## Basic Setup

Add to your `.stylelintrc`:

```json
{
  "plugins": [
    "stylelint-declaration-strict-value"
  ],
  "rules": {
    "scale-unlimited/declaration-strict-value": "color"
  }
}
```

## Primary Configuration Options

### Single Property

Lint a single property like `"color"` or use regex patterns like `"/color$/"` to match multiple properties (color, background-color, border-color).

### Multiple Properties

Use nested arrays for multiple properties:

```json
"scale-unlimited/declaration-strict-value": [
  ["/color$/", "z-index", "font-size"]
]
```

## Secondary Configuration Options

### ignoreVariables

Disable variable enforcement (enabled by default):

```json
{
  "ignoreVariables": false
}
```

Disable for specific properties:

```json
{
  "ignoreVariables": { "margin": false }
}
```

### ignoreFunctions

Control function allowance (enabled by default):

```json
{
  "ignoreFunctions": false
}
```

### ignoreValues

Whitelist specific values, keywords, or patterns:

Single value:
```json
{
  "ignoreValues": "currentColor"
}
```

Multiple values:
```json
{
  "ignoreValues": ["currentColor", "/^#[0-9a-fA-F]{3,6}$/", "inherit"]
}
```

Property-specific mapping:
```json
{
  "ignoreValues": {
    "/color$/": ["currentColor", "transparent"],
    "fill": ["currentColor", "inherit"],
    "": ["currentColor"]
  }
}
```

### ignoreKeywords (DEPRECATED)

Use `ignoreValues` instead. Functionally similar but deprecated syntax kept for backwards compatibility.

### ignoreAtRules

Skip validation inside specific at-rules like `@font-face` or `@media`:

```json
{
  "ignoreAtRules": "@font-face"
}
```

Property-specific configuration:

```json
{
  "ignoreAtRules": {
    "@font-face": ["font-weight"],
    "/^@media/": "/color$/"
  }
}
```

### expandShorthand

Enable expansion of shorthand properties (disabled by default):

```json
{
  "expandShorthand": true
}
```

With this enabled, `border: 1px solid #FFF;` triggers validation on `border-color` if configured.

### recurseLonghand

Expand each longhand property recursively (useful for the `border` property):

```json
{
  "recurseLonghand": true
}
```

### message

Customize error messages with interpolation:

```json
{
  "message": "Custom expected ${types} for \"${value}\" of \"${property}\""
}
```

### Autofix Configuration

Implement custom autofixing logic:

```javascript
function autoFixFunc(node, validation, root, config) {
  const { value, prop } = node;

  if (prop === 'color') {
    switch (value) {
      case '#fff':
        return '$color-white';
      case 'red':
        node.value = '$color-red';
        break;
      default:
        throw new Error(`Cannot autofix ${prop}: ${value}`);
    }
  }
}

module.exports = {
  "rules": {
    "scale-unlimited/declaration-strict-value": [
      ["/color$/"],
      {
        autoFixFunc: autoFixFunc,
        disableFix: false
      }
    ]
  }
}
```

Or reference an external file:

```json
{
  "autoFixFunc": "./auto-fix-func.js",
  "disableFix": false
}
```

## Usage Examples

Violations:
```css
a { color: #FFF; }
a { color: inherit; }
a { z-index: 1; }
```

Compliant:
```css
a { color: var(--color-white); }
a { color: $color-white; }
a { color: @color-white; }
a { z-index: var(--z-index); }
```
