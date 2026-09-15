# FFmpeg Filters Documentation - palettegen and paletteuse (GIF generation)

- URL: https://ffmpeg.org/ffmpeg-filters.html#palettegen-1 (and #paletteuse)
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## 11.191 palettegen (verbatim)

Generate one palette for a whole video stream.

It accepts the following options:

```
max_colors
    Set the maximum number of colors to quantize in the palette. Note:
    the palette will still contain 256 colors; the unused palette
    entries will be black.

reserve_transparent
    Create a palette of 255 colors maximum and reserve the last one for
    transparency. Reserving the transparency color is useful for GIF
    optimization. If not set, the maximum of colors in the palette will
    be 256. You probably want to disable this option for a standalone
    image. Set by default.

transparency_color
    Set the color that will be used as background for transparency.

stats_mode
    Set statistics mode. It accepts the following values:
    'full'    Compute full frame histograms.
    'diff'    Compute histograms only for the part that differs from
              previous frame. This might be relevant to give more
              importance to the moving part of your input if the
              background is static.
    'single'  Compute new histogram for each frame.
    Default value is full.
```

The filter also exports the frame metadata `lavfi.color_quant_ratio` (nb_color_in / nb_color_out) which you can use to evaluate the degree of color quantization of the palette. This information is also visible at info logging level.

### 11.191.1 Examples (verbatim)

- Generate a representative palette of a given video using ffmpeg:
```
ffmpeg -i input.mkv -vf palettegen palette.png
```

## 11.192 paletteuse (verbatim)

Use a palette to downsample an input video stream.

The filter takes two inputs: one video stream and a palette. The palette must be a 256 pixels image.

It accepts the following options:

```
dither
    Select dithering mode. Available algorithms are:
    'bayer'            Ordered 8x8 bayer dithering (deterministic)
    'heckbert'         Dithering as defined by Paul Heckbert in 1982
                       (simple error diffusion). Note: this dithering is
                       sometimes considered "wrong" and is included as a
                       reference.
    'floyd_steinberg'  Floyd and Steingberg dithering (error diffusion)
    'sierra2'          Frankie Sierra dithering v2 (error diffusion)
    'sierra2_4a'       Frankie Sierra dithering v2 "Lite" (error diffusion)
    'sierra3'          Frankie Sierra dithering v3 (error diffusion)
    'burkes'           Burkes dithering (error diffusion)
    'atkinson'         Atkinson dithering by Bill Atkinson at Apple
                       Computer (error diffusion)
    'none'             Disable dithering.
    Default is sierra2_4a.

bayer_scale
    When bayer dithering is selected, this option defines the scale of
    the pattern (how much the crosshatch pattern is visible). A low
    value means more visible pattern for less banding, and higher value
    means less visible pattern at the cost of more banding.
```

(Additional documented options on this filter include `diff_mode` and `alpha_threshold`, per the official page; not fully captured in this extraction pass.)

## Standard two-pass GIF workflow (widely documented usage combining the two filters above)

Two separate commands (palette written to disk, then reused):
```
ffmpeg -i input.mp4 -vf palettegen palette.png
ffmpeg -i input.mp4 -i palette.png -lavfi paletteuse output.gif
```

Single-command equivalent using `filter_complex` with `split`, generating and applying the palette in one pass (common pattern built from the two filters documented above, combined with the `fps` and `scale` filters for GIF-appropriate framerate/size):
```
ffmpeg -i input.mp4 -filter_complex "[0:v] fps=15,scale=480:-1,split [a][b];[a] palettegen [p];[b][p] paletteuse" output.gif
```
