# FFmpeg Documentation - Stream selection / -map (adding an audio track to a video)

- URL: https://ffmpeg.org/ffmpeg.html#Advanced-options
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## -map option (verbatim)

```
-map [-]input_file_id[:stream_specifier][:view_specifier][:?] | [linklabel] (output)
```

Create one or more streams in the output file. This option has two forms for specifying the data source(s): the first selects one or more streams from some input file (specified with -i), the second takes an output from some complex filtergraph (specified with -filter_complex).

In the first form, an output stream is created for every stream from the input file with the index input_file_id. If stream_specifier is given, only those streams that match the specifier are used (see the Stream specifiers section for the stream_specifier syntax).

A - character before the stream identifier creates a "negative" mapping. It disables matching streams from already created mappings.

An optional view_specifier may be given after the stream specifier, which for multiview video specifies the view to be used. The view specifier may have one of the following formats:

```
view:view_id     select a view by its ID; view_id may be set to 'all' to
                  use all the views interleaved into one stream;
vidx:view_idx     select a view by its index; i.e. 0 is the base view, 1
                  is the first non-base view, etc.
vpos:position     select a view by its display position; position may be
                  left or right
```

The default for transcoding is to only use the base view, i.e. the equivalent of vidx:0. For streamcopy, view specifiers are not supported and all views are always copied.

A trailing ? after the stream index will allow the map to be optional: if the map matches no streams the map will be ignored instead of failing. Note the map will still fail if an invalid input file index is used; such as if the map refers to a non-existent input.

An alternative [linklabel] form will map outputs from complex filter graphs (see the -filter_complex option) to the output file. linklabel must correspond to a defined output link label in the graph.

This option may be specified multiple times, each adding more streams to the output file. Any given input stream may also be mapped any number of times as a source for different output streams, e.g. in order to use different encoding options and/or filters. The streams are created in the output in the same order in which the -map options are given on the commandline.

Using this option disables the default mappings for this output file.

### Examples (verbatim)

**map everything** - To map ALL streams from the first input file to output:
```
ffmpeg -i INPUT -map 0 output
```

**select specific stream** - If you have two audio streams in the first input file, these streams are identified by 0:0 and 0:1. You can use -map to select which streams to place in an output file. For example:
```
ffmpeg -i INPUT -map 0:1 out.wav
```
will map the second input stream in INPUT to the (single) output stream in out.wav.

**create multiple streams** - To select the stream with index 2 from input file a.mov (specified by the identifier 0:2), and stream with index 6 from input b.mov (specified by the identifier 1:6), and copy them to the output file out.mov:
```
ffmpeg -i a.mov -i b.mov -c copy -map 0:2 -map 1:6 out.mov
```

**create multiple streams 2** - To select all video and the third audio stream from an input file:
```
ffmpeg -i INPUT -map 0:v -map 0:a:2 OUTPUT
```

**negative map** - To map all the streams except the second audio, use negative mappings:
```
ffmpeg -i INPUT -map 0 -map -0:a:1 OUTPUT
```

**optional map** - To map the video and audio streams from the first input, and using the trailing ?, ignore the audio mapping if no audio streams exist in the first input:
```
ffmpeg -i INPUT -map 0:v -map 0:a? OUTPUT
```

**map by language** - To pick the English audio stream:
```
ffmpeg -i INPUT -map 0:m:language:eng OUTPUT
```

## Standard pattern: add/replace an audio track on a silent screen-capture video (widely used, built from the documented -map syntax above)

```
ffmpeg -i screen_capture.mp4 -i narration.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -shortest output.mp4
```

This maps the video stream from the first input and the audio stream from the second input into one output file, per the `-map input_file_id:stream_specifier` syntax documented above (`0:v` = all video from input 0, `1:a` = all audio from input 1). `-shortest` (a separate, general ffmpeg output option) stops output at the length of the shortest input stream, which is commonly combined with -map in this scenario but is not part of the -map documentation itself.
