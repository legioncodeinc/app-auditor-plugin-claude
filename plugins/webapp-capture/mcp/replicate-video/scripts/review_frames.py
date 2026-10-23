#!/usr/bin/env python3
"""Extract labeled review frames and clustered sheets into a new output folder."""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess


def create_review(video, output, fps=4, start=0, end=None, every_frame=False):
    video = Path(video).expanduser().resolve()
    output = Path(output).expanduser().resolve()
    if not video.is_file() or video.suffix.lower() not in (".mp4", ".mov", ".webm", ".mkv"):
        raise ValueError("Use an existing MP4/MOV/WebM/MKV video file.")
    if output.exists():
        raise ValueError("Review output must be a new folder; existing work is preserved.")
    if not 0 < fps <= 60 or start < 0 or (end is not None and end <= start):
        raise ValueError("Invalid sample rate or review interval.")
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise ValueError("ffmpeg and ffprobe must already be installed.")
    probe = subprocess.run([ffprobe, "-v", "error", "-protocol_whitelist", "file,pipe", "-show_entries", "format=duration:stream=codec_type,avg_frame_rate", "-of", "json", str(video)], capture_output=True, text=True, check=True, timeout=30)
    data = json.loads(probe.stdout)
    duration = float(data["format"]["duration"])
    stop = min(duration, end if end is not None else duration)
    if stop <= start or stop - start > 600:
        raise ValueError("Review windows must be within the clip and at most 600 seconds; split long films into windows.")
    output.mkdir(parents=True)
    (output / "frames").mkdir()
    pattern = str(output / "frames/frame-%06d.png")
    filters = "scale=320:-2" if every_frame else f"fps={fps:g},scale=320:-2"
    command = [ffmpeg, "-nostdin", "-v", "error", "-n", "-protocol_whitelist", "file,pipe", "-i", str(video), "-ss", str(start), "-t", str(stop - start), "-vf", filters]
    if every_frame:
        command += ["-fps_mode", "passthrough"]
    subprocess.run(command + [pattern], capture_output=True, check=True, timeout=120)
    frames = sorted((output / "frames").glob("*.png"))
    if not frames:
        raise ValueError("No review frames were extracted.")
    subprocess.run([ffmpeg, "-nostdin", "-v", "error", "-n", "-framerate", "1", "-i", pattern, "-vf", "tile=4x4:nb_frames=16:padding=4:margin=4", str(output / "sheet-%04d.png")], capture_output=True, check=True, timeout=120)
    sheets = sorted(output.glob("sheet-*.png"))
    manifest = {"source_video": str(video), "start_seconds": start, "end_seconds": stop, "mode": "every_decoded_frame" if every_frame else "sampled", "sampling_fps": None if every_frame else fps, "frames": len(frames), "sheets": len(sheets), "cells_per_sheet": 16, "frame_order": "Row-major, then next sheet; frame filenames preserve ordinal order.", "timestamp_notice": "For sampled mode, approximate source time = start + (ordinal - 1) / fps. Every-frame mode preserves decoded order; use source playback for exact variable-rate timestamps.", "visual_acceptance": "NOT_REVIEWED"}
    (output / "review.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video")
    parser.add_argument("output")
    parser.add_argument("--fps", type=float, default=4)
    parser.add_argument("--start", type=float, default=0)
    parser.add_argument("--end", type=float)
    parser.add_argument("--every-frame", action="store_true")
    args = parser.parse_args()
    try:
        value = create_review(args.video, args.output, args.fps, args.start, args.end, args.every_frame)
    except (ValueError, OSError, KeyError, subprocess.SubprocessError):
        print(json.dumps({"status": "FAIL", "error": "Frame extraction failed. Check the media, interval, new output folder and installed tools; captured decoder output is not echoed."}))
        return 1
    print(json.dumps(value, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
