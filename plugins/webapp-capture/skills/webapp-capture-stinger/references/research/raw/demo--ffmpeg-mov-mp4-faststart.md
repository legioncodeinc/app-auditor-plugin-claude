# FFmpeg Formats Documentation - MOV/MPEG-4/ISOMBFF muxers (movflags +faststart)

- URL: https://ffmpeg.org/ffmpeg-formats.html#Options-8
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## 4.4 MOV/MPEG-4/ISOMBFF muxers (verbatim intro)

This section covers formats belonging to the QuickTime / MOV family, including the MPEG-4 Part 14 format and ISO base media file format (ISOBMFF). These formats share a common structure based on the ISO base media file format (ISOBMFF).

The MOV format was originally developed for use with Apple QuickTime. It was later used as the basis for the MPEG-4 Part 1 (later Part 14) format, also known as ISO/IEC 14496-1.

## movflags option, faststart value (verbatim)

From the muxer options list:

```
movflags flags

    Set various muxing switches. The following flags can be used:
```

(selected values, verbatim)

```
    'cmaf'
        write CMAF (Common Media Application Format) compatible
        fragmented MP4 output

    'dash'
        write DASH (Dynamic Adaptive Streaming over HTTP) compatible
        fragmented MP4 output

    'default_base_moof'
        Similarly to the 'omit_tfhd_offset' flag, this flag avoids
        writing the absolute base_data_offset field in tfhd atoms, but
        does so by using the new default-base-is-moof flag instead. This
        flag is new from 14496-12:2012. This may make the fragments
        easier to parse in certain circumstances (avoiding basing track
        fragment location calculations on the implicit end of the
        previous track fragment).

    'delay_moov'
        delay writing the initial moov until the first fragment is cut,
        or until the first fragment flush

    'disable_chpl'
        Disable Nero chapter markers (chpl atom). Normally, both Nero
        chapters and a QuickTime chapter track are written to the file.
        With this option set, only the QuickTime chapter track will be
        written. Nero chapters can cause failures when the file is
        reprocessed with certain tagging programs, like mp3Tag 2.61a and
        iTunes 11.3, most likely other versions are affected as well.

    'faststart'
        Run a second pass moving the index (moov atom) to the beginning
        of the file. This operation can take a while, and will not work
        in various situations such as fragmented output, thus it is not
        enabled by default.

    'frag_custom'
        Allow the caller to manually choose when to cut fragments, by
        calling av_write_frame(ctx, NULL) to write a fragment with the
        packets written so far. (This is only useful with other
        applications integrating libavformat, not from ffmpeg.)

    'frag_discont'
        signal that the next fragment is discontinuous from earlier ones
```

## Related mention elsewhere in the official docs (verbatim, from the ismv/streaming section)

> "...to the start for better playback by adding +faststart to the -movflags, or using the qt-faststart tool)."

## Usage pattern (standard, widely documented alongside this option)

```
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

This moves the moov atom (file index) to the front of the MP4 file so players/browsers can begin playback before the full file has downloaded, which matters for web-hosted demo videos. Per the verbatim doc text above, faststart requires a second pass and "will not work in various situations such as fragmented output."

## Also seen in official docs (segment muxer example using faststart per-segment)

```
ffmpeg -i in.mkv -f segment -segment_time 10 -segment_format_options movflags=+faststart out%03d.mp4
```
