import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from catalog import tool_catalog
from client import ReplicateClient
from production_health import check_health
from production_doctor import diagnose


class DoctorTests(unittest.TestCase):
    def client(self, token):
        return ReplicateClient(token=token, roots=[ROOT])

    def test_missing_token_is_visible_without_provider_call(self):
        client = self.client("")
        with patch.object(client, "live_schema") as live:
            value = check_health(client, "alibaba/wan-3", True)
        self.assertEqual(value["status"], "NEEDS_ATTENTION")
        live.assert_not_called()
        self.assertFalse(value["credential_value_disclosed"])

    def test_live_check_never_echoes_secret_or_exception(self):
        client = self.client("fixture-private-secret")
        with patch.object(client, "live_schema", side_effect=RuntimeError("fixture-private-secret")):
            value = check_health(client, "alibaba/wan-3", True)
        self.assertNotIn("fixture-private-secret", json.dumps(value))
        self.assertEqual(value["provider"]["status"], "FAIL")
        self.assertEqual((value["uploads"], value["generations"]), (0, 0))

    def test_live_read_success_and_drift(self):
        client = self.client("fixture-token")
        for drift in [False, True]:
            with patch.object(client, "live_schema", return_value={"drift": drift}):
                value = check_health(client, "alibaba/wan-3", True)
            self.assertEqual(value["provider"]["status"], "FAIL" if drift else "PASS")

    def test_unexpanded_placeholder_is_not_a_token(self):
        value = check_health(self.client("${REPLICATE_API_TOKEN}"), "alibaba/wan-3")
        self.assertEqual(next(c for c in value["checks"] if c["name"] == "token")["status"], "FAIL")

    def test_catalog_doctor_is_read_only_and_has_no_credential_arg(self):
        tool = next(t for t in tool_catalog() if t["name"] == "replicate_production_doctor")
        self.assertTrue(tool["annotations"]["readOnlyHint"])
        self.assertEqual(set(tool["inputSchema"]["properties"]), {"live", "model"})

    def test_actual_bootstrap_without_credentials(self):
        with patch.dict(os.environ, {"REPLICATE_API_TOKEN": ""}):
            value = diagnose(False)
        self.assertEqual(value["connection"]["status"], "PASS")
        self.assertEqual(value["connection"]["tools"], len(tool_catalog()))
        self.assertEqual(value["provider"]["status"], "NOT_CHECKED")
        self.assertEqual(value["status"], "NEEDS_ATTENTION")

    def test_malformed_protocol_response_is_sanitized_failure(self):
        fake = SimpleNamespace(returncode=0, stdout="1\n", stderr="fixture-private-secret")
        with patch("production_doctor.subprocess.run", return_value=fake):
            value = diagnose(False)
        self.assertEqual(value["status"], "FAIL")
        self.assertNotIn("fixture-private-secret", json.dumps(value))

    def test_missing_project_is_read_only_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            value = diagnose(False, Path(directory) / "absent")
            self.assertEqual(value["status"], "FAIL")
            self.assertFalse((Path(directory) / "absent").exists())


if __name__ == "__main__":
    unittest.main()
