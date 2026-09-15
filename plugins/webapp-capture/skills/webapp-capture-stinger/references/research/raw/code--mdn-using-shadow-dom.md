# Using shadow DOM - Web APIs | MDN

- URL: https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): not shown on fetched content

## What is Shadow DOM?

Shadow DOM enables you to attach a hidden DOM tree to an element, providing encapsulation so that code running in the page cannot accidentally break a custom element by modifying its internal implementation.

> "Shadow DOM allows hidden DOM trees to be attached to elements in the regular DOM tree — this shadow DOM tree starts with a shadow root, underneath which you can attach any element, in the same way as the normal DOM."

### Key Terminology

- **Shadow host**: The regular DOM node that the shadow DOM is attached to.
- **Shadow tree**: The DOM tree inside the shadow DOM.
- **Shadow boundary**: Where the shadow DOM ends and the regular DOM begins.
- **Shadow root**: The root node of the shadow tree.

## Creating a Shadow DOM

### Imperatively with JavaScript

```javascript
const host = document.querySelector("#host");
const shadow = host.attachShadow({ mode: "open" });
const span = document.createElement("span");
span.textContent = "I'm in the shadow DOM";
shadow.appendChild(span);
```

### Declaratively with HTML

```html
<div id="host">
  <template shadowrootmode="open">
    <span>I'm in the shadow DOM</span>
  </template>
</div>
```

## Open vs Closed Shadow Roots

### Mode: "open"

When you pass `{ mode: "open" }` to `attachShadow()`, the JavaScript in the page can access the internals of the shadow DOM through the `shadowRoot` property:

```javascript
const host = document.querySelector("#host");
const shadow = host.attachShadow({ mode: "open" });
const span = document.createElement("span");
span.textContent = "I'm in the shadow DOM";
shadow.appendChild(span);

const upper = document.querySelector("button#upper");
upper.addEventListener("click", () => {
  const spans = Array.from(host.shadowRoot.querySelectorAll("span"));
  for (const span of spans) {
    span.textContent = span.textContent.toUpperCase();
  }
});
```

The page JavaScript can access and modify shadow DOM elements via `host.shadowRoot`.

### Mode: "closed"

Pass `{ mode: "closed" }` if you don't want to give the page access to shadow DOM internals:

```javascript
const shadow = host.attachShadow({ mode: "closed" });
```

`shadowRoot` then returns `null`.

> "However, you should not consider this a strong security mechanism, because there are ways it can be evaded, for example by browser extensions running in the page. It's more of an indication that the page should not access the internals of your shadow DOM tree."

## Element.shadowRoot Property

The `shadowRoot` property reflects the mode setting:

- With `mode: "open"`: returns the `ShadowRoot` object, allowing access to shadow DOM internals.
- With `mode: "closed"`: returns `null`.

```javascript
const host = document.querySelector("#host");

// Open mode
const shadow = host.attachShadow({ mode: "open" });
console.log(host.shadowRoot); // Returns ShadowRoot object

// Closed mode
const shadow2 = host.attachShadow({ mode: "closed" });
console.log(host.shadowRoot); // Returns null
```

## Encapsulation Benefits

### JavaScript Encapsulation

Code running in the page cannot access shadow DOM elements through normal DOM queries:

```javascript
// This will NOT find elements in the shadow DOM
const spans = document.querySelectorAll("span");
```

### CSS Encapsulation

Page CSS does not affect nodes inside the shadow DOM:

```css
/* This CSS does not affect shadow DOM spans */
span {
  color: blue;
  border: 1px solid black;
}
```

## Styling Inside Shadow DOM

### Using Constructable Stylesheets

```javascript
const sheet = new CSSStyleSheet();
sheet.replaceSync("span { color: red; border: 2px dotted black;}");

const host = document.querySelector("#host");
const shadow = host.attachShadow({ mode: "open" });
shadow.adoptedStyleSheets = [sheet];

const span = document.createElement("span");
span.textContent = "I'm in the shadow DOM";
shadow.appendChild(span);
```

### Using `<style>` Elements in `<template>`

```html
<template id="my-element">
  <style>
    span {
      color: red;
      border: 2px dotted black;
    }
  </style>
  <span>I'm in the shadow DOM</span>
</template>

<div id="host"></div>
```

```javascript
const host = document.querySelector("#host");
const shadow = host.attachShadow({ mode: "open" });
const template = document.getElementById("my-element");
shadow.appendChild(template.content);
```

## Shadow DOM with Custom Elements

Custom elements typically use the element itself as a shadow host:

```javascript
class FilledCircle extends HTMLElement {
  constructor() {
    super();
  }
  connectedCallback() {
    // Create a shadow root - the custom element itself is the shadow host
    const shadow = this.attachShadow({ mode: "open" });

    // Create internal implementation
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    const circle = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "circle",
    );
    circle.setAttribute("cx", "50");
    circle.setAttribute("cy", "50");
    circle.setAttribute("r", "50");
    circle.setAttribute("fill", this.getAttribute("color"));
    svg.appendChild(circle);

    shadow.appendChild(svg);
  }
}

customElements.define("filled-circle", FilledCircle);
```

```html
<filled-circle color="blue"></filled-circle>
```
