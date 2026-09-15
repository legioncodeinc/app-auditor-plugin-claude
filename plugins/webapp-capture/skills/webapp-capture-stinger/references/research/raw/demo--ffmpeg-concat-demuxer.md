# FFmpeg Formats Documentation - concat demuxer

- URL: https://ffmpeg.org/ffmpeg-formats.html#concat
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## 3.6 concat (verbatim)

Virtual concatenation script demuxer.

This demuxer reads a list of files and other directives from a text file and demuxes them one after the other, as if all their packets had been muxed together.

The timestamps in the files are adjusted so that the first file starts at 0 and each next file starts where the previous one finishes. Note that it is done globally and may cause gaps if all streams do not have exactly the same length.

All files must have the same streams (same codecs, same time base, etc.).

The duration of each file is used to adjust the timestamps of the next file: if the duration is incorrect (because it was computed using the bit-rate or because the file is truncated, for example), it can cause artifacts. The duration directive can be used to override the duration stored in each file.

### 3.6.1 Syntax (verbatim)

The script is a text file in extended-ASCII, with one directive per line. Empty lines, leading spaces and lines starting with '#' are ignored. The following directive is recognized:

```
file path
```
Path to a file to read; special characters and spaces must be escaped with backslash or single quotes. All subsequent file-related directives apply to that file.

```
ffconcat version 1.0
```
Identify the script type and version. To make FFmpeg recognize the format automatically, this directive must appear exactly as is (no extra space or byte-order-mark) on the very first line of the script.

```
duration dur
```
Duration of the file. This information can be specified from the file; specifying it here may be more efficient or help if the information from the file is not available or accurate. If the duration is set for all files, then it is possible to seek in the whole concatenated video.

```
inpoint timestamp
```
In point of the file. When the demuxer opens the file it instantly seeks to the specified timestamp. Seeking is done so that all streams can be presented successfully at In point. This directive works best with intra frame codecs, because for non-intra frame ones you will usually get extra packets before the actual In point and the decoded content will most likely contain frames before In point too. For each file, packets before the file In point will have timestamps less than the calculated start timestamp of the file (negative in case of the first file), and the duration of the files (if not specified by the duration directive) will be reduced based on their specified In point. Because of potential packets before the specified In point, packet timestamps may overlap between two concatenated files.

```
outpoint timestamp
```
Out point of the file. When the demuxer reaches the specified decoding timestamp in any of the streams, it handles it as an end of file condition and skips the current and all the remaining packets from all streams. Out point is exclusive, which means that the demuxer will not output packets with a decoding timestamp greater or equal to Out point. This directive works best with intra frame codecs and formats where all streams are tightly interleaved. For non-intra frame codecs you will usually get additional packets with presentation timestamp after Out point therefore the decoded content will most likely contain frames after Out point too. If your streams are not tightly interleaved you may not get all the packets from all streams before Out point and you may only will be able to decode the earliest stream until Out point. The duration of the files (if not specified by the duration directive) will be reduced based on their specified Out point.

```
file_packet_metadata key=value
```
Metadata of the packets of the file. The specified metadata will be set for each file packet. You can specify this directive multiple times to add multiple metadata entries. This directive is deprecated, use file_packet_meta instead.

## Standard usage pattern (widely documented alongside this demuxer)

Create a text file (e.g. `list.txt`) listing files to concatenate:

```
file 'clip1.mp4'
file 'clip2.mp4'
file 'clip3.mp4'
```

Then run, with `-safe 0` required when paths are not relative/simple:

```
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

Per the verbatim spec above: "All files must have the same streams (same codecs, same time base, etc.)" for stream-copy (`-c copy`) concatenation to work correctly; otherwise re-encoding is required.
