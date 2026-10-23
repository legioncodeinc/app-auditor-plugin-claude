import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from review_frames import create_review


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "Existing media runtimes required")
class ReviewTests(unittest.TestCase):
    def test_sampled_and_every_frame_are_distinguished_and_source_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            video = root / "fixture.mp4"
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-n", "-f", "lavfi", "-i", "color=c=blue:s=160x90:r=24:d=1", "-c:v", "libx264", str(video)], check=True, capture_output=True)
            original = hashlib.sha256(video.read_bytes()).hexdigest()
            sample = create_review(video, root / "sample", fps=4)
            full = create_review(video, root / "full", every_frame=True)
            self.assertEqual((sample["mode"], sample["frames"]), ("sampled", 4))
            self.assertEqual((full["mode"], full["frames"]), ("every_decoded_frame", 24))
            self.assertEqual((sample["sheets"], full["sheets"]), (1, 2))
            self.assertEqual(full["visual_acceptance"], "NOT_REVIEWED")
            self.assertEqual(hashlib.sha256(video.read_bytes()).hexdigest(), original)

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.mp4"
            source.write_bytes(b"fixture")
            output = root / "existing"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("original")
            with self.assertRaises(ValueError):
                create_review(source, output)
            self.assertEqual(sentinel.read_text(), "original")


if __name__ == "__main__":
    unittest.main()
