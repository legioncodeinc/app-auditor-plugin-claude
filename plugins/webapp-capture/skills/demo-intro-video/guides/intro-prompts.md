# Intro prompts for product demos

An intro shot sets the mood for 3 to 8 seconds, then the product takes over. Keep it simple: one subject, one camera move, brand colors, no words on screen.

## Rules that save money

- **No text, logos or app screens in the prompt.** Video models misspell words and invent fake interfaces. Add the product name with ffmpeg afterward (`drawtext` or a title card).
- **One idea per shot.** "A slow dolly toward a glowing green sphere" works. A five-step story does not.
- **Say the camera move.** Slow push in, slow orbit, gentle drift, locked off.
- **Name the colors.** Use the brand hex colors as words too: "deep green (#18A968) and near black".
- **Match the cut.** Ask for 16:9, 1080p when the model supports it, and a length that ends on a calm frame so the cut to the demo is clean.
- **Draft cheap, finish good.** Try a short or low resolution draft first when the model allows it, show it, then render the final.

## Prompt pattern

```text
[Shot type and camera move]. [Subject and setting]. [Mood and light]. [Brand colors].
[Ending]: ends on a still, uncluttered frame. No text, no logos, no user interface.
```

## Examples

| Product | Prompt |
| --- | --- |
| Scheduling software | Slow push in on a sunlit kitchen table with a coffee cup and a paper calendar, soft morning light, calm and organized mood, warm whites with deep green accents (#18A968). Ends on a still, uncluttered frame. No text, no logos, no user interface. |
| Developer tool | Slow orbit around abstract glowing lines forming a network over a dark background, precise and modern, near black with deep green light (#18A968). Ends on a still frame. No text, no logos, no user interface. |
| Field service app | Locked off wide shot of a work van parked on a quiet suburban street at golden hour, a technician walks out of frame, confident and friendly mood. Ends on an empty street. No text, no logos, no readable signs. |
| Finance dashboard | Gentle drift across a tidy desk with a notebook and a plant at dusk, city lights blurred behind, calm and trustworthy, navy and soft gold. Ends on a still frame. No text, no logos, no user interface. |

## After rendering

1. Run `review_frames.py` and look at every sheet.
2. Reject the clip for warped hands or faces, melting objects, flicker, text-like scribbles, or a watermark.
3. Trim with ffmpeg if only the start or end is bad, rather than paying for a new render.
