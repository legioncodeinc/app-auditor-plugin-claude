# Replicate Character Video

Use this skill to direct character performances, animated scenes, cinematic sequences, and music-video shots through the accompanying video-only MCP server.

Start with [production workflow](guides/produce-character-scenes.md), then read the selected model guide:

- [Wan 3](guides/wan-3.md)
- [Runway Gen-4.5](guides/gen-4.5.md)
- [Veo 3.1](guides/veo-3.1.md)
- [Seedance 2.0](guides/seedance-2.0.md)
- [Seedance 2.5](guides/seedance-2.5.md)
- [Kling Video 3.0](guides/kling-v3-video.md)
- [Grok Imagine Video](guides/grok-imagine-video.md)

[Research distillation](references/research/distilled-replicate-video.md) records exact schemas, source conflicts and wrapper choices. [Related skill map](references/related-skills.md) identifies authoring and protocol specialists. The standalone skill can be packaged for all four harnesses; the local server runs over stdio on macOS/Linux and requires Python 3.11+ and ffprobe for media references. Cowork supports this server through a local plugin on the same Mac. A custom remote connector is a separate mechanism that requires an authenticated HTTP deployment. Current guidance: [local MCP in plugins](https://support.claude.com/en/articles/13837440-use-plugins-in-claude).
