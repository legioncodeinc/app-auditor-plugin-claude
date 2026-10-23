import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import token_store

GOOD = "r8_" + "A1b2C3d4E5f6G7h8I9j0K1l2"


class TokenStoreTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "cfg" / "replicate.env"
        self.env = patch.dict(os.environ, {"WEBAPP_CAPTURE_TOKEN_FILE": str(self.path)})
        self.env.start()
        os.environ.pop("REPLICATE_API_TOKEN", None)

    def tearDown(self):
        self.env.stop()
        self.dir.cleanup()

    def set_token(self, value, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "set_token.py"), "--stdin", *args], input=value + "\n", text=True, capture_output=True, env=os.environ.copy())

    def test_set_token_writes_owner_only_file_and_never_echoes_it(self):
        result = self.set_token(GOOD)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(GOOD, result.stdout + result.stderr)
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.path.parent.stat().st_mode & 0o777, 0o700)
        self.assertEqual(token_store.read_token(), GOOD)
        where = subprocess.run([sys.executable, str(ROOT / "scripts" / "set_token.py"), "--where"], text=True, capture_output=True, env=os.environ.copy())
        self.assertIn("saved", where.stdout)
        self.assertNotIn(GOOD, where.stdout)

    def test_rejects_values_that_are_not_tokens(self):
        result = self.set_token("hello world")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.path.exists())

    def test_ignores_readable_or_linked_files(self):
        token_store.write_token(GOOD)
        os.chmod(self.path, 0o644)
        self.assertIsNone(token_store.read_token())
        os.chmod(self.path, 0o600)
        link = Path(self.dir.name) / "link.env"
        link.symlink_to(self.path)
        self.assertIsNone(token_store.read_token(link))
        with self.assertRaises(SystemExit):
            token_store.write_token(GOOD, link)

    def test_environment_wins_and_placeholders_fall_back_to_the_file(self):
        token_store.write_token(GOOD)
        os.environ["REPLICATE_API_TOKEN"] = "r8_fromenvironment0000000000"
        token_store.load_into_environment()
        self.assertEqual(os.environ["REPLICATE_API_TOKEN"], "r8_fromenvironment0000000000")
        os.environ["REPLICATE_API_TOKEN"] = "${user_config.replicate_api_token}"
        token_store.load_into_environment()
        self.assertEqual(os.environ["REPLICATE_API_TOKEN"], GOOD)
        os.environ.pop("REPLICATE_API_TOKEN")
        self.path.unlink()
        token_store.load_into_environment()
        self.assertNotIn("REPLICATE_API_TOKEN", os.environ)

    def test_doctor_sees_the_saved_token_without_disclosing_it(self):
        token_store.write_token(GOOD)
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "production_doctor.py")], text=True, capture_output=True, env=os.environ.copy(), timeout=60)
        self.assertIn('"name": "token",\n      "status": "PASS"', result.stdout)
        self.assertNotIn(GOOD, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
