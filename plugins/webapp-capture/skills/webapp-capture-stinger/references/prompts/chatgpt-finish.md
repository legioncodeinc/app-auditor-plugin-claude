# Finish this demo video: instructions for ChatGPT

You are finishing a product demo that Claude recorded with the Webapp Capture plugin.

- Title: **{{TITLE}}**
- Silent demo: `video/demo-silent.mp4` ({{DEMO_SECONDS}} seconds, 1920x1080)
- Voiceover lines: {{CUE_COUNT}} (one audio clip per line)
- Narration pace: {{WPM}} words per minute
- Prepared: {{DATE}}

Your job has three parts. Parts A and B do not depend on each other, so run them at the same time (in parallel tasks or agents if you have them). Part C needs both.

```text
          +--> A. Voiceover clips (one per line) --+
handoff --+                                          +--> C. Stitch --> finished/demo-final.mp4
          +--> B. Intro video (stock or generated) -+
```

Ask the user before anything that costs money (ElevenLabs characters, Replicate generations). Never ask the user to paste an API key into chat. Keys live in the user's own secret manager or app settings.

## Part A: voiceover with ElevenLabs

1. Open `narration/tts-manifest.json`. Each entry has a `textFile`, an `audioFile`, a `startMs` and a `maxMs`.
2. For each entry, send the text in `narration/tts/<textFile>` to ElevenLabs, one request per line, and save the result as `narration/audio/<audioFile>` (MP3 is fine).
   - Use the ElevenLabs connector or MCP server the user has connected, or the ElevenLabs website if neither is connected.
   - Use the Eleven v4 model and the voice the user picks. The manifest leaves `model` and `voice` empty on purpose.
   - Keep the bracketed tags such as `[pause]`, `[short pause]` and `[warm]`. They are voice directions, not words.
   - The lines are independent, so generate them in parallel.
3. Check each clip's length with `ffprobe`. It must be no longer than `maxMs`. If one is too long, shorten that line (keep its meaning) and generate it again. `narration/fit.md` shows which lines were already tight.

## Part B: intro video (3 to 8 seconds)

Read `INTRO-BRIEF.md`, then use the **demo-intro-video** skill:

- **Free stock B-roll** (default, no cost): search the free sites listed in the skill, pick a clip with the user, save it as `intro/intro.mp4`, and write the clip URL, author and license in `intro/SOURCE.md`.
- **Generated** (only when the brief says custom): run the Replicate production doctor, get the user's approval for the model and length, call the model tool through the `replicate_video` MCP, and save the result as `intro/intro.mp4` with the prediction ID in `intro/SOURCE.md`. Never ask the model to draw text, logos or app screens.
- Review it: `python3 review_frames.py intro/intro.mp4 intro/review --fps 4` (from the plugin's `mcp/replicate-video/scripts/`). Reject warped hands, melting objects, flicker or scribbled fake text.

Skip Part B if the user does not want an intro.

## Part C: stitch

From this folder, with ffmpeg installed:

```bash
python3 finish_video.py --intro intro/intro.mp4
```

Leave out `--intro intro/intro.mp4` when there is no intro. The script:

1. checks every voiceover clip exists and fits its line,
2. puts the intro in front of the demo (resized to 1920x1080, 30 fps),
3. places each voiceover clip at its line's start time, moved later by the intro length,
4. moves the captions later by the same amount, and
5. writes `finished/demo-final.mp4` with soft captions.

It never overwrites `finished/`. To try again, rename that folder first.

## Before you hand it back

- Watch the whole of `finished/demo-final.mp4` with sound. Voice lines must match what is on screen.
- `titles.srt` has scene titles if the user wants them burned in.
- Tell the user which parts were AI generated (voice, intro) so they can disclose it to their client.
- Report: final file, length, voice and model used, intro source (stock URL and license, or model and prediction ID), and any line you shortened.

## Line by line

| Line | Scene | Starts at | Max length | Text file |
| --- | --- | --- | --- | --- |
{{CUE_TABLE}}
