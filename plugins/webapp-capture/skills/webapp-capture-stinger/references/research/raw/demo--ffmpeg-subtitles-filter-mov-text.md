# FFmpeg Filters Documentation - subtitles filter (burn-in) and mov_text (soft-mux) codec usage

- URL: https://ffmpeg.org/ffmpeg-filters.html#subtitles-1
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## 11.247 subtitles (verbatim)

Draw subtitles on top of input video using the libass library.

To enable compilation of this filter you need to configure FFmpeg with `--enable-libass`. This filter also requires a build with libavcodec and libavformat to convert the passed subtitles file to ASS (Advanced Substation Alpha) subtitles format.

The filter accepts the following options:

```
filename, f
    Set the filename of the subtitle file to read. It must be specified.

original_size
    Specify the size of the original video, the video for which the ASS
    file was composed. For the syntax of this option, check the "Video
    size" section in the ffmpeg-utils manual. Due to a misdesign in ASS
    aspect ratio arithmetic, this is necessary to correctly scale the
    fonts if the aspect ratio has been changed.

fontsdir
    Set a directory path containing fonts that can be used by the
    filter. These fonts will be used in addition to whatever the font
    provider uses.

alpha
    Process alpha channel, by default alpha channel is untouched.

charenc
    Set subtitles input character encoding. subtitles filter only. Only
    useful if not UTF-8.

stream_index, si
    Set subtitles stream index. subtitles filter only.

force_style
    Override default style or script info parameters of the subtitles.
    It accepts a string containing ASS style format KEY=VALUE couples
    separated by ",".

wrap_unicode
    Break lines according to the Unicode Line Breaking Algorithm.
    Availability requires at least libass release 0.17.0 (or
    LIBASS_VERSION 0x01600010), and libass must have been built with
    libunibreak. The option is enabled by default except for native ASS.

shaping
    Set the shaping engine. Available values are:
    'auto'    The default libass shaping engine, which is the best available.
    'simple'  Fast, font-agnostic shaper that can do only substitutions.
    'complex' Slower shaper using OpenType for substitutions and
              positioning. Required for correct rendering of complex
              scripts such as Arabic, Hebrew, Devanagari and Thai.
              Requires libass to be built with HarfBuzz.
    The default is auto.
```

If the first key is not specified, it is assumed that the first value specifies the filename.

### Examples (verbatim)

For example, to render the file sub.srt on top of the input video, use the command:

```
subtitles=sub.srt
```

which is equivalent to:

```
subtitles=filename=sub.srt
```

To render the default subtitles stream from file video.mkv, use:

```
subtitles=video.mkv
```

To render the second subtitles stream from that file, use:

```
subtitles=video.mkv:si=1
```

To make the subtitles stream from sub.srt appear in 80% transparent blue DejaVu Serif, use:

```
subtitles=sub.srt:force_style='Fontname=DejaVu Serif,PrimaryColour=&HCCFF0000'
```

## Burning subtitles into the video (standard command pattern using the filter above)

```
ffmpeg -i input.mp4 -vf "subtitles=captions.srt" -c:a copy output.mp4
```

## mov_text (soft/embedded subtitle track for MP4) - honest note on source coverage

`mov_text` is FFmpeg's built-in subtitle codec used to mux a text-based subtitle stream (e.g. from an .srt input) as a soft/selectable subtitle track inside an MP4 container, instead of burning it into the video pixels. It is invoked via the generic subtitle codec option:

```
ffmpeg -i input.mp4 -i captions.srt -c:v copy -c:a copy -c:s mov_text output.mp4
```

Searched the official FFmpeg documentation pages fetched for this archive (`ffmpeg-codecs.html`, `ffmpeg-formats.html`, `ffmpeg-filters.html`) and found no dedicated prose section documenting `mov_text` by name — it appears only implicitly as one of the subtitle codecs FFmpeg's MOV/MP4 muxer supports (MP4 containers only support a small set of subtitle codecs, of which `mov_text` — also called "3GPP Timed Text" — is the standard text-based one). The `-c:s mov_text` invocation shown above is the standard, widely-documented usage pattern (consistent with FFmpeg's general `-c:<stream_type> <codec_name>` syntax documented in `ffmpeg.html`), but could not be sourced to a specific verbatim official-docs paragraph naming it. Flagging this gap rather than fabricating a citation.
