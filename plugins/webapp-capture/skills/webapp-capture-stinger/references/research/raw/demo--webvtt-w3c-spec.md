# WebVTT: The Web Video Text Tracks Format - W3C Specification

- URL: https://www.w3.org/TR/webvtt1/
- Fetched: 2026-09-15
- Source type: spec
- Last updated (if shown): May 20, 2026 (W3C Candidate Recommendation Draft, per page)

## Introduction (verbatim/paraphrase of spec intent)

WebVTT (Web Video Text Tracks) is a format for marking up external text track resources with the HTML `<track>` element. Per the spec, it provides "captions or subtitles for video content, and also text video descriptions, chapters for content navigation, and more generally any form of metadata that is time-aligned with audio or video content."

## Basic file structure

### File signature (required)

The file must begin with the literal string `WEBVTT`, optionally preceded by a UTF-8 byte order mark, followed by two or more line terminators.

### Cue timing syntax

Each cue requires a timestamp pair in the format:

```
HH:MM:SS.mmm --> HH:MM:SS.mmm
```

Timestamps consist of hours (optional if zero), minutes (00-59), seconds (00-59), and milliseconds (three digits).

### Cue identifier (optional)

A cue may have an identifier preceding the timing line. The identifier must be unique within the file and cannot contain the substring "-->".

### Cue settings (optional)

Settings follow the timing information, separated by spaces, using the syntax `setting:value`.

## Simple example (verbatim from spec)

```
WEBVTT

00:11.000 --> 00:13.000
<v Roger Bingham>We are in New York City

00:13.000 --> 00:16.000
<v Roger Bingham>We're actually at the Lucern Hotel
```

This demonstrates the basic structure: file header, timing, optional voice tags, and cue text.
