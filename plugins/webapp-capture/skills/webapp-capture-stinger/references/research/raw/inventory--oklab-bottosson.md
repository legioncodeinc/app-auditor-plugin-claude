# A perceptual color space for image processing (Oklab)
- URL: https://bottosson.github.io/posts/oklab/
- Fetched: 2026-09-15
- Source type: canonical article
- Last updated (if shown): unknown (originally published 2020 by Bjorn Ottosson; referenced as the canonical Oklab source by CSS Color Module Level 4)

## Introduction / motivation

Bjorn Ottosson developed Oklab to address shortcomings in existing color spaces for image processing tasks. The color space aims to support operations like "turning an image grayscale, while keeping the perceived lightness the same" and "creating smooth and uniform looking transitions between colors."

## Design requirements

Oklab was built to satisfy these criteria:

- "Should be an opponent color space," similar to CIELAB.
- "Should predict lightness, chroma and hue well," with L, C, and h perceived as orthogonal.
- "Blending two colors should result in even transitions."
- "Should assume a D65 whitepoint."
- "Should behave well numerically," with easy computation and stability.
- "Should assume normal well lit viewing conditions."
- Colors should scale proportionally if exposure changes (scale invariance): "colors should be modelled as if viewed under normal conditions and as if the eye is adapted to roughly the luminance of the color."

## Technical structure

A color in Oklab uses three values: L (perceived lightness), a (green/red axis), and b (blue/yellow axis).

Polar (cylindrical) conversion, matching the OKLCH relationship used by CSS:
- C = sqrt(a^2 + b^2)   (chroma)
- h = atan2(b, a)       (hue angle)

## Conversion: XYZ to Oklab

**Step 1 - LMS transformation:** apply matrix M1 to XYZ coordinates to approximate cone responses (l, m, s).

**Step 2 - Nonlinearity:** "A non-linearity is applied" via cube root: l' = l^(1/3), m' = m^(1/3), s' = s^(1/3).

**Step 3 - Lab transformation:** apply matrix M2 to the cubed values to produce L, a, b.

### Matrices (as commonly published with this article)

M1 (XYZ to LMS, approximate cone response):
```
[+0.8189330101  +0.3618667424  -0.1288597137]
[+0.0329845436  +0.9293118715  +0.0361456387]
[+0.0482003018  +0.2643662691  +0.6338517070]
```

M2 (LMS' to Lab, after cube-root nonlinearity):
```
[+0.2104542553  +0.7936177850  -0.0040720468]
[+1.9779984951  -2.4285922050  +0.4505937099]
[+0.0259040371  +0.7827717662  -0.8086757660]
```

## Direct sRGB conversion

For linear sRGB input, Ottosson provides optimized coefficients that avoid an intermediate XYZ conversion step, with reference C++ code released under a public-domain/MIT-equivalent license, going directly from linear sRGB to LMS to (after cube root) Oklab.

## Derivation methodology

Oklab was optimized using three datasets:
- Colors with constant lightness (varying hue/chroma) from CAM16.
- Colors with constant chroma (varying hue/lightness) from CAM16.
- Uniform perceived hue experimental data.

An error metric using CIEDE2000 color difference evaluated how well each candidate color space preserved these properties. The optimization found that the nonlinearity exponent (gamma) converged to approximately 1/3, which was fixed to exactly 1/3 in the final model (hence the cube-root step above).

## Comparison with existing models

Oklab was evaluated against established color spaces:

- **CIELAB / CIELUV:** "Largest issue is their inability to predict hue. In particular blue hues are predicted badly."
- **CAM16-UCS:** excellent perceptual uniformity but has "bad numerical behavior" and lacks scale invariance.
- **IPT:** "Does a great job modelling hue uniformity" but "Doesn't predict lightness and chroma well."
- **HSV:** "Only on this list because it is widely used. Does not meet any of the requirements."

Oklab combines IPT's computational simplicity with CAM16-UCS's superior lightness and chroma prediction, performing competitively across all three metrics (lightness, chroma, hue prediction) in the article's standardized testing (Munsell chart data, Luo-Rigg datasets, and color-blending analysis).

## Adoption note (context, not from the article body but relevant to why it is cited)

Oklab/OKLCH is the color space referenced normatively by the CSS Color Module Level 4 `oklab()`/`oklch()` functions and by the DTCG Color Module's `oklab`/`oklch` color spaces; Tailwind CSS v4's default palette is also expressed in OKLCH (see `inventory--tailwind-v4-colors.md`).
