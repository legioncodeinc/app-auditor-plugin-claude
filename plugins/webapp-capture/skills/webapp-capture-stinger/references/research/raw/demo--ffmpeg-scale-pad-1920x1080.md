# FFmpeg Filters Documentation - scale and pad filters

- URL: https://ffmpeg.org/ffmpeg-filters.html#scale-1 (and #pad)
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## 11.221 scale (verbatim, selected)

Scale (resize) the input video, using the libswscale library.

The scale filter forces the output display aspect ratio to be the same of the input, by changing the output sample aspect ratio.

If the input image format is different from the format requested by the next filter, the scale filter will convert the input to the requested format.

### 11.221.1 Options (verbatim, selected)

The filter accepts the following options, any of the options supported by the libswscale scaler, as well as any of the framesync options.

```
width, w
height, h

    Set the output video dimension expression. Default value is the
    input dimension.

    If the width or w value is 0, the input width is used for the
    output. If the height or h value is 0, the input height is used for
    the output.

    If one and only one of the values is -n with n >= 1, the scale
    filter will use a value that maintains the aspect ratio of the input
    image, calculated from the other specified dimension. After that it
    will, however, make sure that the calculated dimension is divisible
    by n and adjust the value if necessary.

    If both values are -n with n >= 1, the behavior will be identical to
    both values being set to 0 as previously detailed.

eval
    Specify when to evaluate width and height expression. Accepts
    'init' (default) or 'frame'.

interl
    Set the interlacing mode: '1' force interlaced aware scaling, '0' do
    not apply interlaced scaling (default), '-1' select interlaced aware
    scaling depending on whether the source frames are flagged as
    interlaced or not.

flags
    Set libswscale scaling flags.
```

Further down the options list, `force_original_aspect_ratio` and `force_divisible_by` are also documented (used in the examples below).

### 11.221.2 Examples (verbatim, selected - scaling to 1920x1080 style patterns)

```
- Scale to even dimensions that fit within 400x300, preserving input
  SAR:
      scale='400:300:force_original_aspect_ratio=decrease:force_divisible_by=2'

- Scale to produce square pixels with even dimensions that fit within
  400x300:
      scale='400:300:force_original_aspect_ratio=decrease:force_divisible_by=2:reset_sar=1'

- Scale a subtitle stream (sub) to match the main video (main) in size
  before overlaying. ("scale2ref")
      '[main]split[a][b]; [ref][a]scale=rw:rh[c]; [b][c]overlay'

- Scale a logo to 1/10th the height of a video, while preserving its
  display aspect ratio.
      [logo-in][video-in]scale=w=oh*dar:h=rh/10[logo-out]
```

### 11.221.3 Commands (verbatim)

This filter supports the following commands:

```
width, w
height, h
    Set the output video dimension expression. The command accepts the
    same syntax of the corresponding option.
    If the specified expression is not valid, it is kept at its current
    value.
```

## 11.190 pad (verbatim)

Add paddings to the input image, and place the original input at the provided x, y coordinates.

It accepts the following parameters:

```
width, w
height, h

    Specify an expression for the size of the output image with the
    paddings added. If the value for width or height is 0, the
    corresponding input size is used for the output.

    The width expression can reference the value set by the height
    expression, and vice versa.

    The default value of width and height is 0.

x
y

    Specify the offsets to place the input image at within the padded
    area, with respect to the top/left border of the output image.

    The x expression can reference the value set by the y expression,
    and vice versa.

    The default value of x and y is 0.

    If x or y evaluate to a negative number, they'll be changed so the
    input image is centered on the padded area.

color
    Specify the color of the padded area. For the syntax of this option,
    check the "Color" section in the ffmpeg-utils manual. The default
    value of color is "black".

eval
    Specify when to evaluate width, height, x and y expression.
    It accepts the following values:
    'init'  Only evaluate expressions once during the filter
            initialization or when a command is processed.
    'frame' Evaluate expressions for each incoming frame.
    Default value is 'init'.

aspect
    Pad to aspect instead to a resolution.
```

## Standard combined pattern for "scale and pad to 1920x1080" (widely documented usage of the above two filters together)

```
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black" -c:a copy output.mp4
```

This scales the video down/up to fit within 1920x1080 while preserving aspect ratio (per the `force_original_aspect_ratio=decrease` option documented above), then centers it on a 1920x1080 black canvas using the `pad` filter's `x`/`y` centering behavior described above (negative x/y "changed so the input image is centered on the padded area" is the documented mechanism behind the common `(ow-iw)/2:(oh-ih)/2` centering expression).
