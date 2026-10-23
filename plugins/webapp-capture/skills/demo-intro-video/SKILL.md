---
name: demo-intro-video
description: Make a 3 to 8 second intro or B-roll shot for a product demo, from free stock footage or a Replicate video model through the bundled MCP, then review and stitch it in front of the recorded demo.
license: AGPL-3.0-or-later
compatibility: ChatGPT desktop or Work, Claude Code, Claude Cowork, Codex. Local MCP needs Python 3.11+, ffprobe and ffmpeg on macOS or Linux, and the user's own REPLICATE_API_TOKEN for generation.
metadata:
  author: Legion Code Inc.
  designed-by: Legion Code Inc.
  homepage: https://www.legioncodeinc.com
  domain: demo intro and b-roll video
  version: 2.0.0
  adapted-from: Character Action Studio 1.0.0, replicate-character-video skill (AGPL-3.0-or-later)
---

# Demo Intro Video

Designed and built by [Legion Code Inc.](https://www.legioncodeinc.com)

## Purpose

A recorded product demo starts on a screen. A short intro shot (3 to 8 seconds) in front of it makes the video feel finished: a calm abstract scene in brand colors, a person at a laptop, a city at dawn. This skill gets that shot one of two ways, reviews it frame by frame, and joins it to the demo that the Webapp Capture plugin recorded.

1. **Free stock B-roll** (no cost, fastest). Use when the client does not need anything custom. See `references/free-broll-sources.md` for sites, licenses and APIs.
2. **Generated with a Replicate video model** through the bundled `replicate_video` MCP. Use when the shot must match a brand, color, or idea that stock does not have. Every generation is a paid provider action.

## When to use

- "Add an intro to my demo video", "make a 5 second opener", "find B-roll for the start", "generate an intro clip with Veo or Kling"
- Finishing the handoff zip from `/webapp-capture handoff` in ChatGPT (follow its `CHATGPT-INSTRUCTIONS.md`)

## When not to use

- Recording the product itself: that is the Webapp Capture demo route (`/webapp-capture demo`), which runs in Claude
- Long character stories, music videos or multi-scene films: use the full Character Action Studio plugin
- Voice work beyond one clip per caption line: `elevenlabs-api-stinger`

## Procedure

1. **Read the brief.** In a handoff zip it is `INTRO-BRIEF.md`: product name, audience, brand colors, length, and whether custom footage is required. If there is no brief, ask for those five things in one question.
2. **Pick the path.** Default to free stock B-roll unless the brief says custom, or no stock clip fits after a short search. Tell the user which path and why.
3. **Free stock path.** Search the sites in `references/free-broll-sources.md` (Pexels and Pixabay have APIs). Pick 2 or 3 candidates, show them, and download only the one the user picks. Record the clip page URL, author, license name and license URL, and the download date in `intro/SOURCE.md`. Avoid clips with logos, readable brand names, or identifiable faces used as an endorsement.
4. **Generated path.**
   - Run the doctor first: the `replicate_production_doctor` tool, or `python3 mcp/replicate-video/scripts/production_doctor.py` when the MCP is not connected. It checks the token without printing it.
   - Pick a model from the table below and read its guide in `guides/` (the MCP also serves them as `replicate-video://guides/<model>`).
   - Write the prompt from `guides/intro-prompts.md`. Never ask a video model to draw text, logos or UI: models misspell words and invent interfaces. Titles go on later with ffmpeg.
   - Get the user's approval for the model, length and resolution before calling the tool, because each call costs money. Use a unique `request_key`, record the `prediction_id`, and poll the existing prediction after an uncertain response instead of generating again.
   - Download the output before the provider's temporary link expires. Save it as `intro/intro.mp4` with `intro/SOURCE.md` (model, prediction ID, prompt, date).
5. **Review the actual clip.** `python3 mcp/replicate-video/scripts/review_frames.py intro/intro.mp4 intro/review --fps 4` makes labeled frame sheets. Look at every sheet for warped hands, melted objects, flicker, text-like garbage and watermarks. Regenerate or pick another stock clip if any frame fails.
6. **Stitch.** Follow the stitch section of the handoff's `CHATGPT-INSTRUCTIONS.md`: normalize the intro to 1920x1080 30 fps H.264, join it in front of the demo, shift captions by the intro length, then mix the voiceover.
7. **Report** the final file, the intro's source record, any paid predictions with their IDs, and anything that did not pass review.

## Models for intros

| Need | Tool | Why |
| --- | --- | --- |
| Short cinematic opener with optional ambient sound | `replicate_veo_3_1` | 4, 6 or 8 seconds, 720p or 1080p, optional synchronized audio |
| Polished 1080p shot with precise camera moves | `replicate_kling_v3` | 3 to 15 seconds, pro mode is 1080p, multi-shot timing |
| Longer or flexible length establishing shot | `replicate_wan_3` | 2 to 30 seconds, up to 1080p, one optional starting image |
| Strong camera direction from a single first frame | `replicate_runway_gen_4_5` | Exactly 5 or 10 seconds |
| Quick draft or animating a still | `replicate_grok_imagine_video` | 1 to 15 seconds, 480p or 720p |

Seedance 2.0 and 2.5 are also available for reference-heavy shots; see their guides. Check current pricing on each model's Replicate page before quoting a client.

## References

- `guides/intro-prompts.md`: prompt patterns for product demo intros, with examples
- `guides/MODEL-GUIDES.md` and `guides/<model>.md`: exact fields and limits for each of the seven models (from Character Action Studio)
- `guides/produce-character-scenes.md`: the original scene production workflow
- `references/free-broll-sources.md`: free stock video sites, licenses, APIs and cautions
- `references/research/`: model research distillation and archived primary sources
- `../../mcp/replicate-video/`: the MCP server, its doctor, the frame review script and their tests

## Safety

- The Replicate token lives only in the environment that launches the MCP. Never paste it into chat, a file, or a prompt.
- Uploads and generations follow the user's approval for each provider action. Doctor and guide reads never generate anything.
- Stock clips: keep the license record. Free licenses still forbid some uses (reselling the clip as is, implying a person endorses the product, using trademarks).
- Tell the client that the intro is AI generated when it is, and follow the selling platform's AI disclosure rules.

## Ship Gate

Changes to the bundled MCP server or scripts go through the repository Ship Gate (security, then quality, then repository health) before commit. Routine shot direction creates no repository code and needs no gate.

---

Designed and built by Legion Code Inc. Licensed under AGPL-3.0-or-later. Adapted from the Replicate Character Video skill in Character Action Studio 1.0.0 (Legion Code Inc., AGPL-3.0-or-later).
