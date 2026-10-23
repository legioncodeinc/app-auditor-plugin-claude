URL: https://replicate.com/google/veo-3.1/llms.txt
Fetched: 2026-10-11T00:24:07.154758+00:00
Source type: official model card and schema

## Basic model info

Model name: google/veo-3.1
Model description: New and improved version of Veo 3, with higher-fidelity video, context-aware audio, reference image and last frame support


## Model inputs

- prompt (required): Text prompt for video generation (string)
- aspect_ratio (optional): Video aspect ratio (string)
- duration (optional): Video duration in seconds (integer)
- image (optional): Input image to start generating from. Ideal images are 16:9 or 9:16 and 1280x720 or 720x1280, depending on the aspect ratio you choose. (string)
- last_frame (optional): Ending image for interpolation. When provided with an input image, creates a transition between the two images. (string)
- reference_images (optional): 1 to 3 reference images for subject-consistent generation (reference-to-video, or R2V). Reference images only work with 16:9 aspect ratio and 8-second duration. Last frame is ignored if reference images are provided. (array)
- negative_prompt (optional): Description of what to exclude from the generated video (string)
- resolution (optional): Resolution of the generated video (string)
- generate_audio (optional): Generate audio with the video (boolean)
- seed (optional): Random seed. Omit for random generations (integer)


## Model output schema

{
  "type": "string",
  "title": "Output",
  "format": "uri"
}

If the input or output schema includes a format of URI, it is referring to a file.


## Example inputs and outputs

Use these example outputs to better understand the types of inputs the model accepts, and the types of outputs the model returns:

### Example (https://replicate.com/p/x3c92sahahrmc0cswyp8srjjy8)

#### Input

```json
{
  "prompt": "The woman is doing standup, she tells a joke about not being real, she escaped the latent space, at a small indoor venue, ending with \"so to prove I am real...\"",
  "duration": 8,
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "generate_audio": true,
  "reference_images": [
    "https://replicate.delivery/pbxt/Nt9eZBPGKh09MdoKxr5Oa0nYicruuunAD6ClxBoZrEbqOf2c/0_1.webp"
  ]
}
```

#### Output

```json
"https://replicate.delivery/xezq/MDBpHsfnFuS2TiCNuXM0QGghQ83rAuHikI5x9heoWs2mqTfqA/tmp62g_gnbr.mp4"
```


### Example (https://replicate.com/p/zmzn6n2e9xrme0cswxpr4z734g)

#### Input

```json
{
  "prompt": "the woman is giving an interview for a podcast, wearing a pink top with the logo, it also neatly says \"Veo 3.1\", she is in a midcentury modern studio with pink lighting, she talks about using Veo 3.1 with reference images to put things into videos you're making, the logo is also in a framed picture against black behind her",
  "duration": 8,
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "generate_audio": true,
  "reference_images": [
    "https://replicate.delivery/pbxt/Nt8bL90QO5In3RDkC82HtqeXqNdITglTVpaicTgrdT8mtjiW/0_1.webp",
    "https://replicate.delivery/pbxt/Nt8bLbk1uz4EIMWhIQ0DyjO8BGJYYeAgQWgEnFUWNMOGEpbU/Screenshot%202025-08-26%20at%205.30.12%E2%80%AFPM.png"
  ]
}
```

#### Output

```json
"https://replicate.delivery/xezq/WoC3evx2EQQHLCHq9vEfjhIq9ZotfQhQWmBEd54iLhvVUleVB/tmpk07h98l4.mp4"
```


### Example (https://replicate.com/p/7a6v7zv0qhrmc0csx22rdrd568)

#### Input

```json
{
  "prompt": "the woman are having a conversation in a coffee shop, with the logo in the background. They talk about using Veo 3.1 with reference images to put things into videos",
  "duration": 8,
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true,
  "reference_images": [
    "https://replicate.delivery/pbxt/Nt8bL90QO5In3RDkC82HtqeXqNdITglTVpaicTgrdT8mtjiW/0_1.webp",
    "https://replicate.delivery/pbxt/NtD2ScQlXJm1TfXrWwoCTmK0HEruTV2kN7jqxK3iZGg42Zir/jennai.jpg",
    "https://replicate.delivery/pbxt/NtD2SwdFhhlwnTQJUGFzoq5VjAbAbLfIIY9jEy1ih2DDXVld/image.png"
  ]
}
```

#### Output

```json
"https://replicate.delivery/xezq/69ok3gifKESec04GfPMaTU2YShWMSL37elrN7dQ3QJmeD56rC/tmpvruiwe2d.mp4"
```


### Example (https://replicate.com/p/aa7d67zht9rm80csx6aa5ncsww)

#### Input

```json
{
  "image": "https://replicate.delivery/pbxt/NtHoGeNdKutBUXk2hhOR4uU2elaEWjoQsnfRRCABujtWCT7k/Screenshot%202025-10-15%20at%203.33.40%E2%80%AFPM.png",
  "prompt": "show what happens in this location",
  "duration": 8,
  "resolution": "1080p",
  "aspect_ratio": "16:9",
  "generate_audio": true,
  "reference_images": []
}
```

#### Output

```json
"https://replicate.delivery/xezq/hpxa0wn2og7aIRife9Xlvu0OGeS1qaz45bl43foW3rL58t9VB/tmpgnyhwssx.mp4"
```


## Model readme

> # Veo 3.1
> 
> Google's state-of-the-art video generation model that creates high-quality videos with synchronized native audio from text prompts or images. Veo 3.1 offers enhanced prompt adherence, improved audiovisual quality, and powerful creative controls for image-to-video generation.
> 
> ## Key Features
> 
> **Synchronized Audio Generation** – Veo 3.1 generates rich native audio automatically, from natural conversations and sound effects to ambient soundscapes, perfectly synchronized with your video content.
> 
> **Enhanced Image-to-Video** – Transform static images into dynamic videos with superior prompt adherence and visual quality. Veo 3.1 excels at maintaining character consistency and understanding your creative vision.
> 
> **Superior Prompt Understanding** – The model demonstrates remarkable comprehension of complex, nuanced prompts including intricate scenes, specific camera movements, and detailed artistic styles that previous models often missed.
> 
> **Realistic Physics and Motion** – Veo 3.1 delivers true-to-life textures, coherent motion across frames, and improved realism capturing natural movement and interactions.
> 
> **Reference Image Support** – Upload up to 3 reference images to guide the appearance, style, and character consistency across your generated video, ensuring visual continuity throughout.
> 
> **Frame-to-Frame Generation** – Provide a starting and ending frame, and Veo 3.1 generates smooth, seamless transitions between them, perfect for creating artful scene transitions.
> 
> **Multiple Output Formats** – Generate videos at 720p or 1080p resolution at 24 FPS, with support for both landscape (16:9) and portrait (9:16) aspect ratios. Choose from 4, 6, or 8-second durations.
> 
> **Cinematic Quality** – Veo 3.1 incorporates enhanced understanding of cinematic styles and narrative control, delivering more polished and professional-looking results.
> 
> ## What You Can Create
> 
> **Text-to-Video** – Describe your vision in natural language and watch it come to life with synchronized audio. From realistic scenes to fantastical concepts, Veo 3.1 translates your words into stunning visuals.
> 
> **Image-to-Video** – Animate your static images with lifelike motion and accompanying audio. Perfect for bringing concept art, photos, or illustrations to life.
> 
> **Character Consistency** – Maintain the same character appearance across multiple video generations using reference images, ideal for storytelling and creating cohesive content series.
> 
> **Cinematic Transitions** – Create smooth scene transitions by defining start and end frames, letting Veo 3.1 generate the motion in between with natural camera movement.
> 
> **Extended Sequences** – Build longer narratives by chaining multiple generations together, with each new clip seamlessly continuing from where the last one ended.
> 
> ## Best Practices
> 
> **Crafting Effective Prompts** – Be specific and descriptive in your text prompts. Include details about camera angles, lighting, mood, and any audio elements you want. For example: "A medium shot of a wise owl circling above a moonlit forest clearing, with wings flapping sounds and a gentle orchestral score."
> 
> **Using Reference Images** – When using reference images for character or style consistency, choose clear, well-lit images that show the subject from the desired angle. You can provide 1-3 images to guide the generation.
> 
> **Image-to-Video Tips** – For best results with image-to-video, use high-quality input images with clear subjects. Your prompt should describe the motion and action you want to see, not just describe what's already in the image.
> 
> **Audio Considerations** – While Veo 3.1 generates synchronized audio automatically, you can guide it by describing desired sounds in your prompt using tags or descriptions like "with bird songs and wind rustling" or "accompanied by upbeat music."
> 
> **Frame Control** – When using start and end frames, ensure they're visually compatible and the transition you're requesting is physically plausible. The model works best with natural motion sequences.
> 
> ## About Veo 3.1
> 
> Veo 3.1 builds on Google's Veo 3 foundation with significant improvements in prompt adherence and audiovisual quality, particularly for image-to-video generation. The model was designed with creative professionals in mind, offering granular control over generated content while maintaining ease of use.
> 
> All videos generated with Veo 3.1 are marked with SynthID, Google's watermarking technology for identifying AI-generated content. The model has been extensively tested for safety and content policy compliance.
> 
> Veo 3.1 also comes in a Fast variant (Veo 3.1 Fast) that offers faster generation times while maintaining high quality, perfect for rapid iteration and experimentation.
> 
> ## Learn More
> 
> For detailed API documentation and the latest updates, visit [Google's Gemini API documentation](https://ai.google.dev/gemini-api/docs).
> 
> ---
> 
> **Try the model yourself on the [Replicate Playground](https://replicate.com/google/nano-banana)** to explore its capabilities and see how it can enhance your creative workflow.

