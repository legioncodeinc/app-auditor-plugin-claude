# FFmpeg Codecs Documentation - libx264, libx264rgb (H.264 encoder)

- URL: https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## Notes on scope

This is the official FFmpeg Documentation page `ffmpeg-codecs.html`, section 9.20 "libx264, libx264rgb". Content below is extracted verbatim (via direct HTML fetch + plain-text conversion, not paraphrased) from that section. This covers encoding WebM (or any input) to H.264 video suitable for MP4 output. The `-pix_fmt yuv420p` flag (needed for broad player/device compatibility since many players cannot handle yuv444p/yuv422p) is a general ffmpeg output option, not a libx264-specific option; it is used alongside `-c:v libx264` on the command line, e.g.:

```
ffmpeg -i input.webm -c:v libx264 -pix_fmt yuv420p -crf 23 -preset medium output.mp4
```

## 9.20 libx264, libx264rgb (verbatim)

This encoder requires the presence of the libx264 headers and library during configuration. You need to explicitly configure the build with `--enable-libx264`.

libx264 supports an impressive number of features, including 8x8 and 4x4 adaptive spatial transform, adaptive B-frame placement, CAVLC/CABAC entropy coding, interlacing (MBAFF), lossless mode, custom quantization matrices, multiple reference and B-frames, multithreading, and more.

Many libx264 encoder options are mapped to FFmpeg global codec options, while unique encoder options are provided through private options. Additionally, the `x264opts` and `x264-params` private options allow one to pass a list of key=value tuples as accepted by the libx264 `x264_param_parse` function.

The `libx264rgb` encoder is the same as libx264, except it accepts packed RGB pixel formats as input instead of YUV.

### Options supported by the libx264 wrapper (verbatim, selected)

```
preset (preset)
    Set the encoding preset.

tune (tune)
    Set tuning of the encoding params.

profile (profile)
    Set profile restrictions.

fastfirstpass
    Enable fast settings when encoding first pass, when set to 1. When
    set to 0, it has the same effect of x264's --slow-firstpass option.

crf (crf)
    Set the quality for constant quality mode.

crf_max (crf-max)
    In CRF mode, prevents VBV from lowering quality beyond this point.

qp (qp)
    Set constant quantization rate control method parameter.

aq-mode (aq-mode)
    Set AQ method. Possible values:
    'none (0)'      Disabled.
    'variance (1)'  Variance AQ (complexity mask).
    'autovariance (2)'  Auto-variance AQ (experimental).

aq-strength (aq-strength)
    Set AQ strength, reduce blocking and blurring in flat and textured
    areas.

psy
    Use psychovisual optimizations when set to 1. When set to 0, it has
    the same effect as x264's --no-psy option.

psy-rd (psy-rd)
    ...
```

### x264opts / x264-params (verbatim)

The argument for both options is a list of key=value couples separated by ":". With x264opts the value can be omitted, and the value 1 is assumed in that case.

For filter and psy-rd options values that use ":" as a separator themselves, use "," instead. They accept it as well since long ago but this is kept undocumented for some reason.

For example, the options might be provided as:

```
level=30:bframes=0:weightp=0:cabac=0:ref=1:vbv-maxrate=768:vbv-bufsize=2000:analyse=all:me=umh:no-fast-pskip=1:subq=6:8x8dct=0:trellis=0
```

For example to specify libx264 encoding options with ffmpeg:

```
ffmpeg -i foo.mpg -c:v libx264 -x264opts keyint=123:min-keyint=20 -an out.mkv
```

To get the complete list of the libx264 options, invoke the command `x264 --fullhelp` or consult the libx264 documentation.

### Additional private options (verbatim)

```
a53cc boolean
    Import closed captions (which must be ATSC compatible format) into
    output. Only the mpeg2 and h264 decoders provide these. Default is 1
    (on).

udu_sei boolean
    Import user data unregistered SEI if available into output. Default
    is 0 (off).

mb_info boolean
    Set mb_info data through AVFrameSideData, only useful when used from
    the API. Default is 0 (off).
```

Encoding ffpresets for common usages are provided so they can be used with the general presets system (e.g. passing the pre option).
