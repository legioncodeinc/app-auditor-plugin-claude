#!/usr/bin/env python3
"""Finish a Webapp Capture demo: optional intro in front, one voiceover clip per caption
cue placed at its start time, captions shifted by the intro, one final MP4.

Run from the unzipped handoff folder (Python 3.9+, ffmpeg and ffprobe on PATH):
  python3 finish_video.py                       # demo plus voiceover, no intro
  python3 finish_video.py --intro intro/intro.mp4
Voiceover files go in narration/audio/ with the names listed in narration/tts-manifest.json.
Outputs go in finished/; existing outputs are never overwritten.
Designed by Legion Code Inc.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

VIDEO_ARGS = ["-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps=30,format=yuv420p",
              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "slow", "-r", "30"]


def run(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ERROR: {' '.join(args[:3])} failed: {result.stderr.strip()[-600:]}")
    return result.stdout


def duration_ms(path):
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip()
    try:
        return round(float(out) * 1000)
    except ValueError:
        raise SystemExit(f"ERROR: could not read the length of {path}")


def shift_vtt(text, offset_ms):
    """Move every cue later by offset_ms (the intro length)."""
    def stamp(match):
        h, m, s, ms = (int(x) for x in match.groups())
        total = ((h * 60 + m) * 60 + s) * 1000 + ms + offset_ms
        return f"{total // 3600000:02d}:{total // 60000 % 60:02d}:{total // 1000 % 60:02d}.{total % 1000:03d}"
    return re.sub(r"(\d{2}):(\d{2}):(\d{2})\.(\d{3})", stamp, text)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dir", default=".", help="unzipped handoff folder (default: current folder)")
    parser.add_argument("--intro", help="intro video to put in front of the demo (any size; normalized to 1080p)")
    parser.add_argument("--allow-missing-audio", action="store_true", help="leave cues without an audio file silent")
    parser.add_argument("--allow-overrun", action="store_true", help="accept voiceover clips longer than their cue window")
    args = parser.parse_args()
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise SystemExit(f"ERROR: {tool} is not installed")

    root = Path(args.dir).resolve()
    demo = root / "video" / "demo-silent.mp4"
    manifest = json.loads((root / "narration" / "tts-manifest.json").read_text())
    out = root / "finished"
    if out.exists():
        raise SystemExit(f"ERROR: {out} already exists. Move it aside; earlier output is never overwritten.")
    if not demo.is_file():
        raise SystemExit(f"ERROR: missing {demo}")

    # 1) Check every voiceover clip before doing any work.
    clips, problems = [], []
    for clip in manifest["clips"]:
        audio = root / "narration" / "audio" / clip["audioFile"]
        if not audio.is_file():
            if not args.allow_missing_audio:
                problems.append(f"missing narration/audio/{clip['audioFile']} (cue {clip['cue']}, scene {clip['scene']})")
            continue
        length = duration_ms(audio)
        if length > clip["maxMs"] + 250 and not args.allow_overrun:
            problems.append(f"narration/audio/{clip['audioFile']} is {length / 1000:.1f}s but cue {clip['cue']} has {clip['maxMs'] / 1000:.1f}s; shorten the line or regenerate it faster")
        clips.append((audio, clip["startMs"]))
    if problems:
        raise SystemExit("ERROR: voiceover is not ready:\n  - " + "\n  - ".join(problems))

    out.mkdir()
    work = out / "work"
    work.mkdir()

    # 2) Intro, normalized to the same stream settings as the demo so concat can copy.
    intro_ms = 0
    joined = demo
    if args.intro:
        intro = (root / args.intro).resolve() if not Path(args.intro).is_absolute() else Path(args.intro)
        if not intro.is_file():
            raise SystemExit(f"ERROR: intro not found: {intro}")
        run(["ffmpeg", "-v", "error", "-n", "-i", str(intro), *VIDEO_ARGS, "-an", str(work / "intro-1080p.mp4")])
        intro_ms = duration_ms(work / "intro-1080p.mp4")
        (work / "join.txt").write_text(f"file '{(work / 'intro-1080p.mp4').as_posix()}'\nfile '{demo.as_posix()}'\n")
        joined = work / "joined.mp4"
        run(["ffmpeg", "-v", "error", "-n", "-f", "concat", "-safe", "0", "-i", str(work / "join.txt"), "-c", "copy", str(joined)])
    total_ms = duration_ms(joined)

    # 3) Voiceover track: each clip delayed to its cue start, plus the intro length.
    narration = work / "narration.wav"
    if clips:
        inputs, filters = [], []
        for i, (audio, start) in enumerate(clips):
            inputs += ["-i", str(audio)]
            delay = start + intro_ms
            filters.append(f"[{i}:a]aresample=48000,adelay={delay}|{delay}[a{i}]")
        mix = "".join(f"[a{i}]" for i in range(len(clips))) + f"amix=inputs={len(clips)}:normalize=0:duration=longest,apad[out]"
        run(["ffmpeg", "-v", "error", "-n", *inputs, "-filter_complex", ";".join(filters + [mix]), "-map", "[out]", "-t", f"{total_ms / 1000:.3f}", "-ac", "2", str(narration)])
    else:
        run(["ffmpeg", "-v", "error", "-n", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{total_ms / 1000:.3f}", str(narration)])

    # 4) Captions shifted by the intro, then the final file with soft captions and faststart.
    captions = work / "captions.vtt"
    captions.write_text(shift_vtt((root / "captions.vtt").read_text(), intro_ms))
    final = out / "demo-final.mp4"
    run(["ffmpeg", "-v", "error", "-n", "-i", str(joined), "-i", str(narration), "-i", str(captions),
         "-map", "0:v", "-map", "1:a", "-map", "2", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text",
         "-movflags", "+faststart", str(final)])
    print(json.dumps({"final": str(final.relative_to(root)), "seconds": round(duration_ms(final) / 1000, 2), "introSeconds": intro_ms / 1000, "voiceoverClips": len(clips)}))


if __name__ == "__main__":
    sys.exit(main())
