# differenceCiede2000 — culori API docs (CIEDE2000 color difference reference)
- URL: https://culorijs.org/api/#differenceCiede2000
- Fetched: 2026-09-15
- Source type: official docs (library API reference; canonical algorithm reference is G. Sharma et al., "The CIEDE2000 Color-Difference Formula," University of Rochester)
- Last updated (if shown): unknown

## Signature

```javascript
differenceCiede2000(Kl = 1, Kc = 1, Kh = 1)
```

Returns a difference function `(colorA, colorB) => number` that computes the CIEDE2000 ΔE*00 color difference between two colors.

## Parameters

Three optional weighting factors adjust the formula's sensitivity to different color dimensions:
- **Kl** (default 1) — lightness weighting factor.
- **Kc** (default 1) — chroma weighting factor.
- **Kh** (default 1) — hue weighting factor.

These parametric weights let the formula be tuned for specific viewing conditions/applications (e.g., textiles vs. displays) per the original CIE recommendation.

## Functionality

Computes the CIEDE2000 ΔE*00 color difference between colors `a` and `b`, implemented per G. Sharma's reference implementation (University of Rochester). CIEDE2000 is described as a modern advancement over earlier color-difference formulas (CIE76 / ΔE*ab, CIE94), providing improved perceptual uniformity across the color space — i.e., a given ΔE value corresponds more consistently to the same perceived magnitude of difference regardless of where in color space the two colors fall.

## Interpreting ΔE values / perceptibility thresholds

The culori docs themselves state that a smaller returned ΔE value means the two colors appear more similar to human perception, without giving an exact numeric perceptibility table in the API reference. Broader canonical guidance on CIEDE2000 perceptibility thresholds (aggregated from color-science references, e.g. Konica Minolta's "What Is Delta E" explainer and Techkon's "Demystifying the CIE ΔE 2000 Formula"):

- **ΔE₀₀ < 1**: the difference is generally *not* perceptible to the human eye under normal viewing.
- **ΔE₀₀ ≈ 1–2**: a "just noticeable difference" (JND) — perceptible only on close, side-by-side inspection. With the default weighting factors (Kl=Kc=Kh=1), the CIEDE2000 scale is calibrated so that roughly one ΔE unit corresponds to this just-noticeable-difference threshold.
- **ΔE₀₀ ≥ 2**: an increasingly obvious mismatch, the kind of difference that typically fails tight color-tolerance requirements (e.g. brand color matching, print/screen tolerance).

## Notes for webapp-capture-stinger

For detecting "the same design-token color rendered inconsistently across the app" (vs. deliberately different colors), CIEDE2000 is the right perceptual metric rather than raw RGB Euclidean distance or hex-string equality — two colors that are hex-different but visually indistinguishable (ΔE₀₀ < ~1) should generally not be flagged as a drift/inconsistency finding, while ΔE₀₀ above roughly 2 is a reasonable default "flag this" threshold for a design-token consistency audit. culori's `differenceCiede2000()` is a ready-made JS implementation suitable for a Node-based capture/audit pipeline (no need to hand-roll the Lindbloom reference formulas, though Bruce Lindbloom's published equations remain the primary academic citation for the underlying math).
