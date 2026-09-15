# pixelmatch (mapbox) README
- URL: https://github.com/mapbox/pixelmatch (README fetched via https://raw.githubusercontent.com/mapbox/pixelmatch/master/README.md)
- Fetched: 2026-09-15
- Source type: README
- Last updated (if shown): unknown (raw README, no date shown; package actively used as of 2026)

## Description

Pixelmatch is a "small, simple and fast JavaScript pixel-level image comparison library, originally created to compare screenshots in tests." It detects "accurate anti-aliased pixels" and employs "perceptual color difference metrics." The library requires no dependencies, operates on raw typed arrays, and functions across Node.js and browser environments.

## Installation

Node/npm:
```
npm install pixelmatch
```

Browser via CDN (ESM):
```js
import pixelmatch from 'https://esm.run/pixelmatch'
```

## API Signature

```js
pixelmatch(img1, img2, output, width, height[, options])
```

Parameters:
- `img1`, `img2` — Image data (Buffer, Uint8Array, or Uint8ClampedArray); dimensions must match.
- `output` — Diff image data buffer, or `null` if you don't need a diff image.
- `width`, `height` — Shared dimensions for all three images.

Returns: the number of mismatched pixels (or, in windowed mode, the maximum diff-pixel density in an N×N window).

## Options Object

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `threshold` | number | 0.1 | Matching threshold, ranges from 0 to 1. Smaller values make the comparison more sensitive. |
| `includeAA` | boolean | false | If true, disables detecting and ignoring anti-aliased pixels. |
| `alpha` | number | 0.1 | Blending factor of unchanged pixels in the diff output. Ranges from 0 (white) to 1 (set to original image). |
| `aaColor` | [R,G,B] | [255,255,0] | The color of anti-aliased pixels in the diff output. |
| `diffColor` | [R,G,B] | [255,0,0] | The color of differing pixels in the diff output. |
| `diffColorAlt` | [R,G,B] | null | An alternative color to use for dark-on-light differences to differentiate between "added" vs "removed" content, i.e. text. |
| `diffMask` | boolean | false | Draw the diff over a transparent background (a mask), rather than over the original image. |
| `checkerboard` (implementation notes vary by version) | boolean | true | Blends semi-transparent pixels against a checkerboard pattern in the diff output. |

## Usage Examples

Node.js (with `pngjs`):
```js
const diff = new PNG({width, height});
pixelmatch(img1.data, img2.data, diff.data, width, height, {threshold: 0.1});
```

Browser (with canvas ImageData):
```js
pixelmatch(img1.data, img2.data, diff.data, width, height, {threshold: 0.1});
diffContext.putImageData(diff, 0, 0);
```

## Notes for webapp-capture-stinger

- Return value is a pixel count, not a ratio — divide by `width * height` to get a mismatch ratio comparable to Playwright's `maxDiffPixelRatio`.
- Anti-aliasing detection (`includeAA: false` default) avoids false positives on font/edge rendering differences across runs — relevant when comparing captures taken at different times or on different machines.
- `output` diff image visually highlights differences in `diffColor`, useful for generating human-reviewable diff artifacts in the capture pipeline.
