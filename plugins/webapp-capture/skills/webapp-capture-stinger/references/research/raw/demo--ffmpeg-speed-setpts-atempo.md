# FFmpeg Filters Documentation - setpts (video speed) and atempo (audio speed)

- URL: https://ffmpeg.org/ffmpeg-filters.html#setpts_002c-asetpts (and #atempo)
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): unknown (live single-page doc, no date shown; fetched from the current ffmpeg.org site)

## 20.19 setpts, asetpts (verbatim)

Change the PTS (presentation timestamp) of the input frames.

setpts works on video frames, asetpts on audio frames.

This filter accepts the following options:

```
expr
    The expression which is evaluated for each frame to construct its
    timestamp.

strip_fps (video only)
    Boolean option which determines if the original framerate and frame
    duration metadata is unset. If set to true, be advised that a sane
    frame rate should be explicitly specified if output is sent to a
    constant frame rate muxer. Default is false.
```

The expression is evaluated through the eval API and can contain the following constants (selected):

```
FRAME_RATE, FR   frame rate, only defined for constant frame-rate video
PTS              The presentation timestamp in input
N                The count of the input frame for video or the number of
                 consumed samples, not including the current frame for
                 audio, starting from 0.
STARTPTS         The PTS of the first frame.
STARTT           the time in seconds of the first frame
T                the time in seconds of the current frame
TB               The timebase of the input timestamps.
```

### 20.19.1 Examples (verbatim)

```
- Start counting PTS from zero
      setpts=PTS-STARTPTS
- Apply fast motion effect:
      setpts=0.5*PTS
- Apply slow motion effect:
      setpts=2.0*PTS
- Set fixed rate of 25 frames per second:
      setpts=N/(25*TB)
- Apply a random jitter effect of +/-100 TB units:
      setpts=PTS+randomi(0, -100\,100)
- Set fixed rate 25 fps with some jitter:
      setpts='1/(25*TB) * (N + 0.05 * sin(N*2*PI/25))'
- Apply an offset of 10 seconds to the input PTS:
      setpts=PTS+10/TB
- Generate timestamps from a "live source" and rebase onto the current
  timebase:
      setpts='(RTCTIME - RTCSTART) / (TB * 1000000)'
- Generate timestamps by counting samples:
      asetpts=N/SR/TB
```

### 20.19.2 Commands (verbatim)

Both filters support all above options as commands.

## 8.65 atempo (verbatim)

Adjust audio tempo.

The filter accepts exactly one parameter, the audio tempo. If not specified then the filter will assume nominal 1.0 tempo. Tempo must be in the [0.5, 100.0] range.

Note that tempo greater than 2 will skip some samples rather than blend them in. If for any reason this is a concern it is always possible to daisy-chain several instances of atempo to achieve the desired product tempo.

### 8.65.1 Examples (verbatim)

```
- Slow down audio to 80% tempo:
      atempo=0.8
- To speed up audio to 300% tempo:
      atempo=3
- To speed up audio to 300% tempo by daisy-chaining two atempo
  instances:
      atempo=sqrt(3),atempo=sqrt(3)
```

### 8.65.2 Commands (verbatim)

This filter supports the following commands:

```
tempo
    Change filter tempo scale factor. Syntax for the command is :
    "tempo"
```

## Combined video+audio speed-change pattern (built from the two documented filters above)

To speed a clip up 2x (video and audio together, keeping sync):
```
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4
```

Per the atempo documentation above, its valid single-filter range is [0.5, 2.0] in practice for smooth results at the documented "tempo greater than 2 will skip some samples" caveat — note the option's hard range is stated as [0.5, 100.0], but chaining (`atempo=2.0,atempo=2.0` for 4x) is the documented technique for values outside a single comfortable step.
