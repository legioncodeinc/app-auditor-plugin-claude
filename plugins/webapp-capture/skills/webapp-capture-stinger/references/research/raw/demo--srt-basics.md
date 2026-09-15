# SRT (SubRip) Subtitle File Format

- URL: https://docs.fileformat.com/video/srt/
- Fetched: 2026-09-15
- Source type: community article
- Last updated (if shown): unknown

## File structure

An SRT file contains sequential subtitle entries, each comprising four components:

1. **Sequence number** - a numeric counter identifying the subtitle's position
2. **Timecode line** - start and end timestamps separated by `-->`
3. **Subtitle text** - one or more lines of content
4. **Blank line** - delimiter marking the entry's end

## Timestamp format

Format: `hours:minutes:seconds,milliseconds` (`00:00:00,000`). The comma serves as the millisecond separator, distinguishing SRT from some other subtitle formats (like WebVTT) that use a period instead.

Example timecode structure:
```
00:05:00,400 --> 00:05:15,300
```

## Sample SRT content (verbatim from page)

```
1
00:05:00,400 --> 00:05:15,300
This is an example of
a subtitle.

2
00:05:16,400 --> 00:05:25,300
This is an example of
a subtitle - 2nd subtitle.
```

## Formatting support

SRT files support HTML-derived tags including `<b>`, `<i>`, `<u>` for text styling and `<font color="">` for color specification.

## Key operational detail

Media players automatically synchronize SRT files with video content when filenames match (e.g., `movie.mp4` paired with `movie.srt`).

## Note on source authority

SRT (SubRip Text) has no single formal owner or W3C-style specification body; it originated from the SubRip DVD-ripping tool. This page (fileformat.com) was used as a concise, structurally accurate community reference for the format's syntax rules since no canonical spec page exists. The timestamp/structure rules above are consistent across all mainstream descriptions of the format (also corroborated by the Library of Congress's digital-preservation format description at https://www.loc.gov/preservation/digital/formats/fdd/fdd000569.shtml, seen during research but not separately archived).
