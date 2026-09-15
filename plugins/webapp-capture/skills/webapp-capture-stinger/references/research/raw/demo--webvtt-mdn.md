# WebVTT API - MDN Web Docs

- URL: https://developer.mozilla.org/en-US/docs/Web/API/WebVTT_API
- Fetched: 2026-09-15
- Source type: official docs
- Last updated (if shown): February 11, 2026 (page's "Last Modified" date)

## What is WebVTT

Web Video Text Tracks (WebVTT) is a format for defining time-aligned text tracks that accompany video or audio content. The WebVTT API provides functionality to define and manipulate these text tracks, primarily used for:
- Displaying subtitles or captions overlaid with video content
- Providing chapter information for navigation
- Associating generic metadata with audio/video content

## Core concepts

### Text tracks

A text track is a container for time-aligned text data that plays in parallel with video/audio. Tracks can be of different kinds:
- `captions`
- `descriptions`
- `chapters`
- `subtitles`
- `metadata`

### Cues

Individual time-aligned units of text data within a track, each containing:
- Start time
- End time
- Textual payload
- Optional cue settings (display region, position, alignment, size)
- Optional label (for CSS styling)

## WebVTT file format basics

### File header

```
WEBVTT
```

### Cue structure - timestamp format

```
HH:MM:SS.mmm --> HH:MM:SS.mmm
Text content
```

### Example VTT file content (verbatim from page)

```
WEBVTT

00:00.000 --> 00:00.900
Hildy!

00:01.000 --> 00:01.400
How are you?

00:01.500 --> 00:02.900
Tell me, is the lord of the universe in?

00:03.000 --> 00:04.200
Yes, he's in - in a bad humor

00:04.300 --> 00:06.000
Somebody must've stolen the crown jewels
```

## HTML integration with the `<track>` element

### Basic usage

```html
<video controls src="video.webm">
  <track default kind="captions" src="captions.vtt" srclang="en" />
</video>
```

### Multiple-track example

```html
<video controls src="video.webm">
  <track default kind="captions" src="captions.vtt" srclang="en" />
  <track kind="subtitles" src="subtitles.vtt" srclang="en" />
  <track kind="descriptions" src="descriptions.vtt" srclang="en" />
  <track kind="chapters" src="chapters_de.vtt" srclang="de" />
  <track kind="subtitles" src="subtitles_en.vtt" srclang="en" />
</video>
```

Key attributes:
- `kind`: Type of track (captions, subtitles, descriptions, chapters, metadata)
- `src`: Path to WebVTT file
- `srclang`: Language code (required when kind is specified)
- `default`: Indicates which track plays if user preferences don't specify a language/kind (only one per video)

## WebVTT API interfaces

| Interface | Purpose |
|-----------|---------|
| `VTTCue` | Represents a cue (text displayed at specific time) |
| `VTTRegion` | Represents a video region where cues render |
| `TextTrack` | Container holding list of cues for a media element |
| `TextTrackCue` | Abstract base class for cue types |
| `TextTrackCueList` | Array-like list of TextTrackCue objects |
| `TextTrackList` | List of all text tracks for a media element |

## JavaScript API usage example

```javascript
let video = document.querySelector("video");
let track = video.addTextTrack("captions", "Captions", "en");
track.mode = "showing";
track.addCue(new VTTCue(0, 0.9, "Hildy!"));
track.addCue(new VTTCue(1, 1.4, "How are you?"));
track.addCue(new VTTCue(1.5, 2.9, "Tell me, is the <u>lord of the universe</u> in?"));
track.addCue(new VTTCue(3, 4.2, "Yes, he's in - in a bad humor"));
track.addCue(new VTTCue(4.3, 6, "Somebody must've <b>stolen</b> the crown jewels"));
console.log(track.cues);
```

## CSS styling with the `::cue` pseudo-element

```css
/* Style all cues */
video::cue {
  font-size: 1.5rem;
  background-image: linear-gradient(to bottom, yellow, lightyellow);
  color: red;
}

/* Style specific markup within cues */
video::cue(u) {
  color: green;
}

video::cue(b) {
  color: purple;
}

/* Style by class */
video::cue(.myclass) {
  color: lightblue;
}

/* Style by attribute */
video::cue([lang="en"]) {
  color: lightgreen;
}

video::cue(v[voice="Bob"]) {
  color: orange;
}
```

Note: `::cue-region` pseudo-element is defined in the specification but not supported by any browsers (per the page).
