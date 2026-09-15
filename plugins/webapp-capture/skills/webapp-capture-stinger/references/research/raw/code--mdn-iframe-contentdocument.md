# HTMLIFrameElement: contentDocument property | MDN

- URL: https://developer.mozilla.org/en-US/docs/Web/API/HTMLIFrameElement/contentDocument
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): Baseline widely available; feature available across browsers since July 2015

## Description

The `contentDocument` property provides access to the Document object of an iframe's nested browsing context. Access is restricted by the same-origin policy for security reasons.

## Same-Origin Requirement

If the iframe and the iframe's parent document are same origin, the property returns a `Document` object (the active document in the inline frame's nested browsing context). If they are cross-origin, it returns `null`.

## Return Values

- **Same-origin iframe**: Returns a `Document` object representing the iframe's content.
- **Cross-origin iframe**: Returns `null`.

## Syntax

```javascript
const iframeDocument = iframeElement.contentDocument;
```

## Example Code

```javascript
const iframeDocument = document.querySelector("iframe").contentDocument;

iframeDocument.body.style.backgroundColor = "blue";
// This would turn the iframe blue.
```

## Browser Compatibility

Baseline: Widely available. This feature is well established and works across many devices and browser versions. It has been available across browsers since July 2015.

## Specification

HTML Standard - dom-iframe-contentdocument: https://html.spec.whatwg.org/multipage/iframe-embed-object.html#dom-iframe-contentdocument

## Relevance to capture-tool design

A capture tool can only read/traverse into an iframe's DOM (for inventorying components or taking targeted screenshots) when the iframe is same-origin; cross-origin iframes will yield `null` from `contentDocument` and must be treated as an opaque region (screenshot only, no DOM introspection).
