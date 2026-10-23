URL: https://replicate.com/alibaba/wan-3/llms.txt
Fetched: 2026-10-11T00:24:07.163654+00:00
Source type: official model card and schema

## Basic model info

Model name: alibaba/wan-3
Model description: Wan 3.0 generates video from a text prompt or a starting image, with cinematic motion and support for 480p, 720p, and 1080p output up to 30 seconds.


## Model inputs

- prompt (required): Text prompt for video generation (string)
- image (optional): Optional first-frame image to animate into a video (jpg/png/bmp/webp, ≤10MB). When provided, the video is generated from this image guided by the prompt. (string)
- negative_prompt (optional): Negative prompt — describes content that should not appear in the video (string)
- resolution (optional): Output video resolution (string)
- aspect_ratio (optional): Aspect ratio of the generated video. 'adaptive' lets the model choose the best ratio for the prompt. Ignored when an image is provided (the input image's aspect ratio is used). (string)
- duration (optional): Duration of the generated video in seconds (integer)
- enable_prompt_expansion (optional): Automatically expand and optimize the prompt for better results. Improves quality for short prompts but increases latency. (boolean)
- seed (optional): Random seed for reproducible generation. Range: 0-2147483647 (integer)


## Model output schema

{
  "type": "string",
  "title": "Output",
  "format": "uri"
}

If the input or output schema includes a format of URI, it is referring to a file.


## Example inputs and outputs

Use these example outputs to better understand the types of inputs the model accepts, and the types of outputs the model returns:

### Example (https://replicate.com/p/xgx1epgvtdrmy0d06mwafqr6j0)

#### Input

```json
{
  "prompt": "a turtle swimming through a library, 35mm film ",
  "duration": 5,
  "resolution": "1080p",
  "aspect_ratio": "adaptive",
  "negative_prompt": "",
  "enable_prompt_expansion": true
}
```

#### Output

```json
"https://replicate.delivery/xezq/oeKJ5kG2szVZZij9ejo1zt1dXHslnPnPr0VrzwksOslizkGXA/tmps3b3c9bp.mp4"
```


## Model readme

> # Wan 3.0
> 
> Wan 3.0 is Alibaba's video model. Give it a prompt and it generates a short video with cinematic motion and camera movement. You can also provide a starting image to animate.
> 
> ## What it's good at
> 
> - **Text to video.** Turn a description into a video clip.
> - **Image to video.** Provide a first-frame image and the model animates it, guided by your prompt.
> - **Multiple resolutions.** Choose 480p, 720p, or 1080p.
> - **Long clips.** Generate up to 30 seconds.
> - **Adaptive framing.** Let the model pick the best aspect ratio for your prompt, or set one explicitly.
> 
> ## Inputs
> 
> - `prompt` — describe the video you want.
> - `image` — optional first-frame image to animate (jpg/png/bmp/webp). When provided, the video is generated from this image.
> - `resolution` — 480p, 720p, or 1080p.
> - `aspect_ratio` — adaptive (model chooses) or an explicit ratio (16:9, 9:16, 1:1, 4:3, 3:4). Ignored when an image is provided.
> - `duration` — length of the video in seconds, 2 to 30.
> - `negative_prompt` — content to avoid.
> - `enable_prompt_expansion` — automatically expand and optimize short prompts.
> - `seed` — set for reproducible results.
> 
> ## Pricing
> 
> Priced per second of output video:
> 
> - 480p: $0.05 per second
> - 720p: $0.10 per second
> - 1080p: $0.20 per second

