URL: https://replicate.com/xai/grok-imagine-video/llms.txt
Fetched: 2026-10-11T00:24:07.128995+00:00
Source type: official model card and schema

## Basic model info

Model name: xai/grok-imagine-video
Model description: Generate videos using xAI's Grok Imagine Video model


## Model inputs

- prompt (required): Text prompt for video generation (string)
- image (optional): Input image to generate video from (image-to-video). Supports jpg, jpeg, png, webp. (string)
- video (optional): Input video to edit (video editing mode). Must be a direct link, max 8.7 seconds. Supports mp4, mov, webm. (string)
- duration (optional): Duration of the video in seconds (1-15). Ignored when editing a video. (integer)
- aspect_ratio (optional): Aspect ratio of the video. For text-to-video, defaults to 16:9. For image-to-video, defaults to the input image's native aspect ratio. Ignored when editing a video. (string)
- resolution (optional): Resolution of the video. Ignored when editing a video. (string)


## Model output schema

{
  "type": "string",
  "title": "Output",
  "format": "uri"
}

If the input or output schema includes a format of URI, it is referring to a file.


## Example inputs and outputs

Use these example outputs to better understand the types of inputs the model accepts, and the types of outputs the model returns:

### Example (https://replicate.com/p/4n4ee65zbhrmr0cw6j69hm8758)

#### Input

```json
{
  "prompt": "a penguin walks away from the camera, towards a large snowy mountaintop in the distance",
  "duration": 5,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}
```

#### Output

```json
"https://replicate.delivery/xezq/WfcfRkCE0xhGSEwerEeKl9GP9IoiaPHmCfot7a2LGNTig9nwC/tmpxqdftsp7.mp4"
```


### Example (https://replicate.com/p/3174ybmrf9rmt0cw6jb82h29rc)

#### Input

```json
{
  "image": "https://replicate.delivery/pbxt/OXkJpAQAIbwcBCpqV5USf14PGOhQpTzdTdtl2yhrrBqqde5E/replicate-prediction-px6n3hq8zhrmr0cw6jasjwafew.jpg",
  "prompt": "the camera zooms in on to the man as he lifts both arms up in celebration",
  "duration": 6,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}
```

#### Output

```json
"https://replicate.delivery/xezq/sLEF7eoQEsysUiYzyrwb72Y2CTBSdXSQvr7S0O7Ys6CF7fEWA/tmpauhg97d5.mp4"
```


### Example (https://replicate.com/p/v4c7k8ey4srmy0cw6jgt9cwwz8)

#### Input

```json
{
  "video": "https://replicate.delivery/pbxt/OXkTI3ZJUr8zZFJvAuK1X6TPTQLHH0L4QQtq7A9GKry350X0/replace-bird-1.mp4",
  "prompt": "replace the arm with a branch",
  "duration": 6,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}
```

#### Output

```json
"https://replicate.delivery/xezq/UuvdAxexRpShfUb0cPSO2jPzYwyrxP2gofGSGUve3wqXJAUYB/tmpd07rncv1.mp4"
```


## Model readme

> # Grok Imagine Video
> 
> Turn images into cinematic videos with synchronized audio using xAI's Video model.
> 
> Grok Imagine Video takes a static image and brings it to life with realistic motion, object interactions, and automatically generated sound. Upload a portrait, a product photo, or any illustration, and watch it transform into a video complete with background music, sound effects, and ambient audio that matches the visual content.
> 
> ## What it does
> 
> This model animates still images into short videos with synchronized audio. It handles both the visual generation and audio synthesis in one pass, so you get videos with sound that actually fits what's happening on screen, no separate audio editing needed.
> 
> The model understands different types of content and adapts accordingly. It can animate cartoon characters with exaggerated expressions, turn product photos into 360-degree showcases, or add natural motion to portraits while maintaining the original style and composition of your image.
> 
> ## How it works
> 
> Grok Imagine Video uses xAI's Aurora model, an autoregressive mixture-of-experts architecture trained on billions of examples from the internet. The model predicts image tokens sequentially, which gives tight control over generation and helps maintain visual consistency across frames.
> 
> The audio generation happens natively alongside the video creation. Rather than adding sound in post-production, the model generates background music, sound effects, and ambient audio that's synchronized with the visual content from the start. For animations with characters, it can even handle lip-sync for dialogue and singing.
> 
> The model processes images through multiple specialized networks that work together to optimize different aspects of video generation—one handles motion physics, another manages temporal consistency to prevent flickering or artifacts, and others focus on style preservation and audio-visual coherence.
> 
> ## What you can make
> 
> **Product showcases**: Transform static product photography into dynamic demonstrations. A watch photo becomes a luxury ad with an elegant wrist turn. A sneaker shot gets a 360-degree rotation with dramatic lighting.
> 
> **Character animation**: Turn illustrated characters into smooth animations. The model understands cartoon physics and exaggerated motion, creating professional-quality animation that would typically require an entire animation team.
> 
> **Portrait videos**: Animate professional headshots into video introductions with natural human motion. The model handles realistic facial expressions, head turns, and body language.
> 
> **Creative projects**: Bring concept art to life, animate historical photos, or turn memes into short video clips with appropriate sound effects and music.
> 
> ## Generation modes
> 
> The model offers different creative modes that affect how it interprets your prompt:
> 
> **Normal mode** produces balanced, professional results with realistic motion and consistent quality. This works well for most use cases where you want reliable, high-quality output.
> 
> **Fun mode** adds more dynamic and creative elements to the generation. The results are more playful and whimsical, with exaggerated motion and stylized interpretations.
> 
> **Custom mode** gives you more precise control over specific aspects of the generation when you need fine-tuned adjustments.
> 
> ## Prompt guide
> 
> The most reliable way to write prompts for Grok Imagine Video is to think like a director. Structure your prompt around these elements:
> 
> **Subject + Action + Setting + Camera + Lighting/Mood**
> 
> The model expands your prompt internally, so you don't need to describe every detail — but you do need to give it clear direction about what matters. Write natural sentences, not keyword lists.
> 
> ### Text-to-video prompts
> 
> When generating video from text, your prompt carries all the scene information.
> 
> **Cinematic portrait:**
> ```
> Close-up shot of a young woman turning her head to look at the camera,
> golden hour light casting warm shadows across her face, gentle wind
> moving through her hair, slow camera push-in, nostalgic mood,
> shallow depth of field, 50mm lens feel, photoreal natural light.
> ```
> 
> **Action scene:**
> ```
> Tracking shot of a cloaked thief sprinting through a medieval castle
> courtyard at dusk, dust kicking up, torches flickering on stone walls,
> camera at shoulder height following the action, dramatic lighting,
> crisp motion, cinematic pacing.
> ```
> 
> **Nature/landscape:**
> ```
> 8-second wide establishing shot of a mountain trail at sunrise,
> golden light spilling over the ridge, wind moving grass subtly,
> distant birds gliding across the sky, slow stabilized pan,
> warm color grade, natural realism, gentle film grain.
> ```
> 
> **Product showcase:**
> ```
> Close-up of a luxury watch on a marble surface, camera slowly
> orbiting 360 degrees, soft studio lighting with subtle reflections
> on the metal case, clean minimal background, commercial ad style.
> ```
> 
> ### Image-to-video prompts
> 
> When animating a still image, the model already has the scene. Focus your prompt on **motion, not description**.
> 
> - **Don't re-describe what's in the image.** The model sees it. Tell it what should change — the action, the camera movement, the atmosphere.
> - **Don't contradict the image.** If there's a man in the photo, don't write "a woman dances." Match your prompt to what's actually there.
> - **Be specific about motion.** The model can't infer the degree of motion from a still image. "Car passing" is vague — "car racing past at high speed" gives the model something to work with.
> - **Mention prominent features** to anchor the subject: "the old man wearing glasses" or "the woman in the red jacket."
> - **Negative prompts don't work.** The model ignores them. Describe what you want instead.
> 
> **Portrait animation:**
> ```
> The woman slowly turns her head to the right and smiles,
> soft breeze moving her hair, gentle camera push-in.
> ```
> 
> **Product animation:**
> ```
> The sneaker rotates smoothly on the pedestal, camera orbiting
> at eye level, dramatic spotlight sweeping across the surface.
> ```
> 
> ### Camera movements
> 
> The model understands standard cinematic camera language:
> 
> - **Pan left/right** — camera rotates horizontally to reveal a scene
> - **Tilt up/down** — camera rotates vertically for dramatic reveals
> - **Zoom in/out** — lens zooms closer or further
> - **Dolly in/out** — camera physically moves forward or backward (more cinematic than zoom)
> - **Tracking/follow shot** — camera follows a moving subject
> - **Orbit/surround** — camera circles around the subject
> - **Aerial/drone** — elevated bird's-eye perspective
> - **Handheld** — natural shake for documentary feel or urgency
> - **Slow push-in** — gradual forward movement to build tension
> - **Static/tripod** — no camera movement for stable, formal compositions
> 
> You can describe multiple shots in sequence using "camera switch" or "cut to" as a transition cue:
> 
> ```
> Close-up of a kitten eating from a bowl. Camera switch.
> Close-up of the cat food showing the texture and detail.
> ```
> 
> ### Audio prompts
> 
> The model generates audio natively alongside the video. Influence it by mentioning sound in your prompt:
> 
> - **Background music:** "with upbeat electronic music" or "dramatic orchestral score"
> - **Sound effects:** "footsteps on gravel," "wind howling," "engine revving"
> - **Ambient audio:** "quiet café ambience," "forest sounds with birdsong"
> - **Short dialogue:** "a quiet whisper: 'We made it.'" or "urgent shout: 'Stop him!'"
> 
> You can add an `AUDIO:` section at the end of your prompt for clarity:
> 
> ```
> 8-second close-up of hands pulling apart a warm cinnamon roll,
> steam rising, soft morning window light, slow camera push-in,
> cozy kitchen mood.
> AUDIO: soft room tone, faint kettle hiss, gentle pastry tear sound,
> a quiet satisfied whisper: 'Perfect.'
> ```
> 
> ### Multiple actions
> 
> The model handles multi-beat sequences well. List actions in order:
> 
> ```
> The athlete crouches at the starting line, then explodes forward,
> legs alternating rapidly, arms pumping powerfully. After crossing
> the finish line, the crowd erupts in cheers. Follow-shot perspective.
> ```
> 
> You can also describe actions for multiple subjects:
> 
> ```
> The teacher in the background lectures angrily while the student
> in the foreground slowly turns away. Camera rack-focuses from
> student to teacher.
> ```
> 
> ### Intensity and adverbs
> 
> The model responds to intensity modifiers. Without them, it fills in its own interpretation, which may be more subtle than you want. Exaggerate slightly to match your intent:
> 
> - "car passing" → "car racing past at high speed"
> - "man roaring" → "man roaring wildly"
> - "wings flapping" → "wings flapping with massive amplitude"
> 
> ### Style keywords
> 
> Embed these naturally in your prompts rather than stacking them as tags:
> 
> - **Photorealistic:** "photoreal detail," "natural lighting," "lifelike textures," "documentary feel"
> - **Cinematic:** "volumetric lighting," "film grain," "dynamic shadows," "anamorphic lens"
> - **Anime:** "vibrant cel-shading," "expressive linework," "bright anime palette"
> - **Painterly:** "oil-painting texture," "lush brushstrokes," "impressionist glow"
> - **Surreal:** "dreamlike distortion," "ethereal glow," "otherworldly hues"
> - **Retro:** "1970s color film," "VHS grain," "faded Polaroid tones"
> - **Commercial:** "clean studio lighting," "product photography," "premium feel"
> 
> ### Video editing prompts
> 
> When editing an existing video, describe what to change. The model preserves everything you don't mention.
> 
> - **Add:** "Add a silver necklace to the woman."
> - **Remove:** "Remove the bee from the scene."
> - **Swap:** "Replace the bird with a small dragon."
> - **Restyle:** "Restyle this as cyberpunk anime with neon-charged lines."
> - **Scene change:** "Change the setting to autumn with falling leaves and warm golden light."
> - **Color change:** "Change the woman's outfit from blue to red."
> 
> Editing input videos can be up to 8.7 seconds. The output matches the input's duration, aspect ratio, and resolution.
> 
> ### Common mistakes
> 
> - **Re-describing the image in image-to-video mode.** The model already sees it. Focus on motion.
> - **Contradicting the source image.** Match your prompt to what's actually in the photo.
> - **Tag stacking** ("knight, castle, epic, 8K, cinematic"). Write a natural sentence with intent instead.
> - **Too many simultaneous actions.** Keep it to one subject, one action, one camera move.
> - **No camera direction.** Always specify a shot type and camera movement.
> - **Vague motion** ("the thing moves"). Use specific verbs with intensity modifiers.
> - **Using negative prompts.** They're ignored. Describe what you want instead.
> 
> ### Tips for better results
> 
> - **Keep it simple.** One main subject + one primary action + one camera move.
> - **Iterate in small steps.** Change one thing at a time — lighting, camera, action, or mood.
> - **Use the two-step approach.** Generate a great still image first, then animate it with image-to-video for more control.
> - **Describe lighting and time of day.** "Morning window light," "golden hour," "overcast," "candlelight."
> - **Use specific verbs.** "Surges," "unfurls," "shatters," "drifts" create better motion than "moves" or "goes."
> - **Shorter clips are more stable.** 5–8 seconds is the sweet spot. 15-second clips work but are more likely to have artifacts.
> - **Match aspect ratio to your platform.** 16:9 for YouTube, 9:16 for Reels/TikTok, 1:1 for social media thumbnails.
> 
> ## Technical details
> 
> - **Video duration**: 1-15 seconds
> - **Resolution**: 480p or 720p
> - **Aspect ratios**: 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3
> - **Audio**: Automatically generated and synchronized with video
> - **Architecture**: Autoregressive mixture-of-experts (Aurora model)
> - **Capabilities**: Text-to-video, image-to-video, and video editing with native audio-video synthesis
> - **Editing input limit**: 8.7 seconds (output matches input duration/ratio/resolution)
> 
> ## Try it yourself
> 
> You can run this model and experiment with different images and prompts on the Replicate Playground at replicate.com/playground

