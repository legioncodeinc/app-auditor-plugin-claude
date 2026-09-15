# Node.compareDocumentPosition() - MDN Web Docs
- URL: https://developer.mozilla.org/en-US/docs/Web/API/Node/compareDocumentPosition
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): March 20, 2026

## Syntax

```javascript
compareDocumentPosition(otherNode)
```

## Parameters

- **`otherNode`**: the `Node` for which position should be reported, relative to the node on which the method is called.

## Return value

An integer value representing `otherNode`'s position relative to the calling node as a bitmask combining the following constants, or `0` if `otherNode` is the same as the node:

| Constant | Value | Meaning |
|----------|-------|---------|
| `Node.DOCUMENT_POSITION_DISCONNECTED` | `1` | Both nodes are in different documents or different trees in the same document |
| `Node.DOCUMENT_POSITION_PRECEDING` | `2` | `otherNode` precedes the node in pre-order depth-first traversal (ancestor, previous sibling, or descendant of previous sibling) |
| `Node.DOCUMENT_POSITION_FOLLOWING` | `4` | `otherNode` follows the node in pre-order depth-first traversal (descendant, following sibling, or descendant of following sibling) |
| `Node.DOCUMENT_POSITION_CONTAINS` | `8` | `otherNode` is an ancestor of the node |
| `Node.DOCUMENT_POSITION_CONTAINED_BY` | `16` | `otherNode` is a descendant of the node |
| `Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC` | `32` | Result relies on implementation-specific behavior |

## Example

```javascript
const head = document.head;
const body = document.body;

if (head.compareDocumentPosition(body) & Node.DOCUMENT_POSITION_FOLLOWING) {
  console.log("Well-formed document");
} else {
  console.error("<head> is not before <body>");
}
```

Note: use the bitwise AND operator (`&`) to check specific bits in the bitmask result.

## Browser compatibility

Baseline, widely available since July 2015 across all major browsers.
