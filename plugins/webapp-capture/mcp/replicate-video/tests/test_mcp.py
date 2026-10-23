import concurrent.futures
import datetime as dt
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import wave
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from catalog import MODELS, model_input, provider_input, schema_for, tool_catalog, validate
from client import DomainError, ReplicateClient, inspect_media, media_type, validate_combinations
from server import Server


def png(width=320, height=320):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress((b"\0" + b"\0" * width * 3) * height)) + chunk(b"IEND", b"")


class Backend:
    def __init__(self):
        self.calls = []
        self.drift = False
        self.fail_create = False
        self.status = "starting"
        self.prediction_model = "alibaba/wan-3"

    def __call__(self, method, path, body, content_type):
        self.calls.append((method, path, body, content_type))
        if method == "GET" and path.startswith("/models/"):
            snap = schema_for(path.removeprefix("/models/"))
            doc = json.loads(json.dumps(snap["openapi_schema"]))
            if self.drift:
                doc["components"]["schemas"]["Input"]["properties"]["new_control"] = {"type": "boolean"}
            return {"latest_version": {"id": snap["version"], "openapi_schema": doc}}
        if path == "/files":
            number = sum(c[1] == "/files" for c in self.calls)
            return {"id": f"file{number}", "urls": {"get": f"https://api.replicate.com/v1/files/file{number}/download?signature=mock"}, "expires_at": (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1)).isoformat()}
        if method == "POST" and path.endswith("/predictions"):
            if self.fail_create:
                raise DomainError("Mocked ambiguous submission")
            self.prediction_model = path.removeprefix("/models/").removesuffix("/predictions")
            return {"id": "prediction1", "model": self.prediction_model, "status": self.status, "output": "https://replicate.delivery/test/scene.mp4" if self.status == "succeeded" else None}
        if path.startswith("/predictions/"):
            return {"id": "prediction1", "model": self.prediction_model, "status": "canceled" if path.endswith("/cancel") else self.status, "output": None, "input": {"prompt": "private prompt"}, "logs": "private provider logs", "error": "private error"}
        raise AssertionError(f"Unexpected API call {method} {path}")

    def posts(self):
        return [call for call in self.calls if call[0] == "POST"]


class MCPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.backend = Backend()
        self.client = ReplicateClient(token="offline-fixture-token", roots=[self.root], state_path=self.root / "state.sqlite3", transport=self.backend)
        self.server = Server(self.client)
        self.server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "offline-tests", "version": "1"}}})
        self.server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
        self.image = self.root / "character.png"
        self.image.write_bytes(png())

    def tearDown(self):
        if self.client._ledger:
            self.client.ledger.db.close()
        self.temp.cleanup()

    def call(self, name, arguments):
        return self.server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": name, "arguments": arguments}})

    def generation(self, tool="replicate_wan_3", **inputs):
        return self.call(tool, {"input": {"prompt": "A copper automaton gently opens its hand in a moonlit observatory.", **inputs}, "request_key": "scene_take_001"})

    def test_catalog_is_exact_and_specific(self):
        tools = self.server.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/list"})["result"]["tools"]
        self.assertEqual({t["name"] for t in tools}, {"replicate_" + slug for slug in MODELS} | {"replicate_upload_file", "replicate_model_schema", "replicate_get_prediction", "replicate_cancel_prediction", "replicate_production_doctor"})
        self.assertTrue(all(len(t["description"]) > 150 for t in tools))
        for tool in tools:
            self.assertFalse(tool["inputSchema"]["additionalProperties"])
        self.assertEqual(self.backend.calls, [])

    def test_all_models_route_to_separate_endpoints(self):
        for index, (slug, (model, _)) in enumerate(MODELS.items()):
            response = self.call("replicate_" + slug, {"input": {"prompt": "A single character takes a bow in warm light."}, "request_key": f"unique_take_{index}"})
            self.assertFalse(response["result"]["isError"], response)
            self.assertEqual(self.backend.posts()[-1][1], f"/models/{model}/predictions")
            self.assertEqual(set(self.backend.posts()[-1][2]), {"input"})

    def test_unknown_model_field_is_rejected_before_any_http(self):
        response = self.generation("replicate_runway_gen_4_5", resolution="4k")
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_enums_bounds_and_types_are_rejected(self):
        cases = [("replicate_runway_gen_4_5", {"duration": 8}), ("replicate_veo_3_1", {"resolution": "4k"}), ("replicate_kling_v3", {"mode": "cinema"}), ("replicate_wan_3", {"seed": -1}), ("replicate_seedance_2_5", {"duration": 3}), ("replicate_wan_3", {"duration": True})]
        for tool, inputs in cases:
            with self.subTest(tool=tool, inputs=inputs):
                self.assertTrue(self.generation(tool, **inputs)["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_empty_prompt_and_seedance25_empty_call(self):
        for tool in ("replicate_wan_3", "replicate_seedance_2_5"):
            response = self.call(tool, {"input": {"prompt": " "}, "request_key": "empty_take01"})
            self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_missing_token_is_tool_error_without_http(self):
        self.client.token = ""
        self.assertTrue(self.generation()["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_schema_drift_prevents_spend_and_uploads(self):
        self.backend.drift = True
        response = self.generation(image={"path": str(self.image)})
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])

    def test_local_reference_calls_shared_upload_before_prediction(self):
        response = self.generation(image={"path": str(self.image)})
        self.assertFalse(response["result"]["isError"], response)
        posts = self.backend.posts()
        self.assertEqual([post[1] for post in posts], ["/files", "/models/alibaba/wan-3/predictions"])
        self.assertIn(b'name="content"; filename="reference.png"', posts[0][2])
        self.assertNotIn(str(self.image).encode(), posts[0][2])
        self.assertIn("multipart/form-data; boundary=", posts[0][3])
        self.assertEqual(posts[1][2]["input"]["image"], "https://api.replicate.com/v1/files/file1/download?signature=mock")

    def test_explicit_upload_reused_for_file_id_and_same_bytes(self):
        first = self.call("replicate_upload_file", {"path": str(self.image)})["result"]["structuredContent"]
        second = self.call("replicate_upload_file", {"path": str(self.image)})["result"]["structuredContent"]
        self.assertTrue(second["reused"])
        response = self.generation(image={"file_id": first["file_id"]})
        self.assertFalse(response["result"]["isError"])
        self.assertEqual(sum(post[1] == "/files" for post in self.backend.posts()), 1)

    def test_arbitrary_url_and_data_uri_rejected(self):
        for value in ("https://example.com/private.png", "data:image/png;base64,AAAA", {"url": "https://example.com/file.png"}):
            self.assertTrue(self.generation(image=value)["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_unknown_file_id_rejected_before_mutation(self):
        self.assertTrue(self.generation(image={"file_id": "unknown123"})["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])

    def test_outside_root_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            source = Path(outside) / "ref.png"
            source.write_bytes(png())
            (self.root / "alias.png").symlink_to(source)
            for path in (source, self.root / "alias.png"):
                with self.subTest(path=path):
                    self.assertTrue(self.call("replicate_upload_file", {"path": str(path)})["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])

    def test_ancestor_swap_race_does_not_read_outside_root(self):
        inside = self.root / "references"
        inside.mkdir()
        (inside / "ref.png").write_bytes(png())
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside)
            (external / "ref.png").write_bytes(png())
            original_open = os.open
            swapped = False
            def raced_open(path, flags, *args, **kwargs):
                nonlocal swapped
                if path == "references" and "dir_fd" in kwargs and not swapped:
                    inside.rename(self.root / "original-references")
                    inside.symlink_to(external, target_is_directory=True)
                    swapped = True
                return original_open(path, flags, *args, **kwargs)
            with patch("client.os.open", side_effect=raced_open), patch("client.os.supports_dir_fd", {os.open}):
                with self.assertRaises(DomainError):
                    self.client.prepare_file(str(inside / "ref.png"))
            self.assertTrue(swapped)
        self.assertEqual(self.backend.calls, [])

    def test_empty_nonmedia_and_malformed_images_rejected(self):
        for body in (b"", b"REPLICATE_API_TOKEN=not-media", b"\x89PNG\r\n\x1a\ninvalid"):
            file = self.root / "bad.png"
            file.write_bytes(body)
            self.assertTrue(self.call("replicate_upload_file", {"path": str(file)})["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_ffprobe_image_dimensions_and_audio_duration(self):
        image = inspect_media(png(320, 400), "image/png")
        self.assertEqual((image["width"], image["height"]), (320, 400))
        stream = io.BytesIO()
        with wave.open(stream, "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(8000)
            audio.writeframes(b"\0" * 16000)
        metadata = inspect_media(stream.getvalue(), "audio/wav")
        self.assertAlmostEqual(metadata["duration_seconds"], 1.0)

    def test_missing_ffprobe_fails_before_upload(self):
        with patch("client.shutil.which", return_value=None):
            response = self.generation(image={"path": str(self.image)})
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])

    def test_reference_total_cap_before_any_post(self):
        with patch("client.MAX_REFERENCE_BYTES", 100), patch.object(self.client, "reference", return_value={"data": b"x" * 60, "content_type": "image/png", "sha256": "mock"}):
            response = self.generation("replicate_seedance_2_5", reference_images=[{"file_id": "ref1"}, {"file_id": "ref2"}])
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])
        self.assertEqual(self.client.ledger.db.execute("SELECT COUNT(*) FROM requests").fetchone()[0], 0)

    def test_idempotency_survives_restart(self):
        first = self.generation()["result"]["structuredContent"]
        next_client = ReplicateClient(token="offline-fixture-token", roots=[self.root], state_path=self.root / "state.sqlite3", transport=self.backend)
        try:
            second = next_client.generate("alibaba/wan-3", {"input": {"prompt": "A copper automaton gently opens its hand in a moonlit observatory."}, "request_key": "scene_take_001"})
            self.assertEqual(first, second)
            self.assertEqual(len(self.backend.posts()), 1)
        finally:
            next_client.ledger.db.close()

    def test_concurrent_same_key_creates_exactly_one_prediction(self):
        args = {"input": {"prompt": "A character waves."}, "request_key": "concurrent_take01"}
        def call():
            try:
                return self.client.generate("alibaba/wan-3", args)
            except DomainError as error:
                return str(error)
        with concurrent.futures.ThreadPoolExecutor(2) as workers:
            responses = list(workers.map(lambda _: call(), range(2)))
        self.assertTrue(any(isinstance(value, dict) for value in responses))
        self.assertEqual(len(self.backend.posts()), 1)

    def test_changed_arguments_cannot_reuse_key(self):
        self.generation()
        response = self.generation(duration=10)
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(len(self.backend.posts()), 1)

    def test_ambiguous_submission_is_not_retried(self):
        self.backend.fail_create = True
        first = self.generation()
        second = self.generation()
        self.assertTrue(first["result"]["isError"])
        self.assertTrue(second["result"]["isError"])
        self.assertEqual(len(self.backend.posts()), 1)
        self.assertIn("unresolved", second["result"]["structuredContent"]["error"])

    def test_veo_constraints_prevent_uploads(self):
        ref = {"path": str(self.image)}
        for controls in ({"reference_images": [ref], "duration": 6}, {"reference_images": [ref], "aspect_ratio": "9:16"}, {"last_frame": ref}, {"image": ref, "reference_images": [ref]}):
            self.assertTrue(self.generation("replicate_veo_3_1", **controls)["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_seedance_reference_constraints_and_counts(self):
        ref = {"file_id": "ref1"}
        for tool, controls in (("replicate_seedance_2_0", {"reference_images": [ref] * 10}), ("replicate_seedance_2_5", {"reference_images": [ref] * 31}), ("replicate_seedance_2_0", {"reference_audios": [ref]}), ("replicate_seedance_2_5", {"image": ref, "reference_videos": [ref]}), ("replicate_seedance_2_0", {"last_frame_image": ref})):
            self.assertTrue(self.generation(tool, **controls)["result"]["isError"])
        self.assertEqual(self.backend.calls, [])

    def test_seedance_video_and_audio_duration_totals(self):
        for model, seconds, field in (("replicate_seedance_2_0", 16, "reference_videos"), ("replicate_seedance_2_5", 31, "reference_videos"), ("replicate_seedance_2_0", 16, "reference_audios")):
            media = {"content_type": "audio/wav" if "audio" in field else "video/mp4", "duration_seconds": seconds, "size": 10, "file_id": "ref1", "url": "https://replicate.delivery/test/ref"}
            with patch.object(self.client, "reference", return_value=media):
                controls = {field: [{"file_id": "ref1"}]}
                if "audio" in field:
                    controls["reference_images"] = [{"file_id": "ref2"}]
                    def refs(value):
                        return media if value["file_id"] == "ref1" else {"content_type": "image/png", "size": 10, "file_id": "ref2", "url": "https://replicate.delivery/test/ref2"}
                    with patch.object(self.client, "reference", side_effect=refs):
                        response = self.generation(model, **controls)
                else:
                    response = self.generation(model, **controls)
            self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])

    def test_seedance25_edit_workflow_not_forwarded(self):
        media = {"content_type": "video/mp4", "duration_seconds": 5, "size": 10, "file_id": "ref1", "url": "https://replicate.delivery/test/video.mp4"}
        args = {"input": {"prompt": "Change the character's coat to blue, preserving motion.", "reference_videos": [{"file_id": "ref1"}], "duration": -1, "aspect_ratio": "adaptive"}, "workflow": "edit", "request_key": "seedance25_edit01"}
        with patch.object(self.client, "reference", return_value=media):
            response = self.call("replicate_seedance_2_5", args)
        self.assertFalse(response["result"]["isError"])
        self.assertNotIn("workflow", self.backend.posts()[-1][2]["input"])
        for input_change in ({"duration": 5}, {"aspect_ratio": "16:9"}, {"reference_videos": []}):
            modified = {**args, "request_key": "different_edit01", "input": {**args["input"], **input_change}}
            self.assertTrue(self.call("replicate_seedance_2_5", modified)["result"]["isError"])

    def test_kling_shot_json_total_and_frames(self):
        for controls in ({"multi_prompt": "[]"}, {"multi_prompt": [{"prompt": "one", "duration": 5}]}, {"multi_prompt": '[{"prompt":"one","duration":3}]', "duration": 5}, {"end_image": {"file_id": "ref1"}}):
            self.assertTrue(self.generation("replicate_kling_v3", **controls)["result"]["isError"])
        good = '[{"prompt":"The character enters.","duration":2},{"prompt":"The character bows.","duration":3}]'
        self.assertFalse(self.generation("replicate_kling_v3", multi_prompt=good)["result"]["isError"])
        with self.assertRaises(DomainError):
            self.client.reference_rules("kwaivgi/kling-v3-video", "start_image", {"content_type": "image/png", "size": 5, "width": 100, "height": 100})

    def test_grok_edit_constraints_and_probed_duration(self):
        for controls in ({"video": {"file_id": "ref1"}, "duration": 5}, {"video": {"file_id": "ref1"}, "image": {"file_id": "ref2"}}):
            self.assertTrue(self.generation("replicate_grok_imagine_video", **controls)["result"]["isError"])
        with self.assertRaises(DomainError):
            self.client.reference_rules("xai/grok-imagine-video", "video", {"content_type": "video/mp4", "duration_seconds": 8.71})
        self.client.reference_rules("xai/grok-imagine-video", "video", {"content_type": "video/mp4", "duration_seconds": 8.7})

    def test_prediction_status_and_failed_state_are_honest(self):
        self.backend.status = "failed"
        response = self.call("replicate_get_prediction", {"prediction_id": "prediction1"})
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(response["result"]["structuredContent"]["status"], "failed")
        self.assertNotIn("private", json.dumps(response))
        self.assertNotIn("offline-fixture-token", json.dumps(response))

    def test_cancel_checks_model_and_terminal_state(self):
        self.backend.prediction_model = "some/image-model"
        response = self.call("replicate_cancel_prediction", {"prediction_id": "prediction1"})
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])
        self.backend.prediction_model = "alibaba/wan-3"
        self.backend.status = "succeeded"
        self.assertFalse(self.call("replicate_cancel_prediction", {"prediction_id": "prediction1"})["result"]["isError"])
        self.assertEqual(self.backend.posts(), [])
        self.backend.status = "processing"
        canceled = self.call("replicate_cancel_prediction", {"prediction_id": "prediction1"})["result"]
        self.assertEqual(canceled["structuredContent"]["status"], "canceled")
        self.assertFalse(canceled["isError"])
        self.assertEqual(self.backend.posts()[-1][1], "/predictions/prediction1/cancel")

    def test_model_schema_is_read_only_and_refresh_reports_drift(self):
        response = self.call("replicate_model_schema", {"model": "bytedance/seedance-2.5"})
        self.assertFalse(response["result"]["isError"])
        self.assertEqual(self.backend.calls, [])
        self.backend.drift = True
        response = self.call("replicate_model_schema", {"model": "bytedance/seedance-2.5", "refresh": True})
        self.assertTrue(response["result"]["structuredContent"]["live"]["drift"])
        self.assertEqual(self.backend.posts(), [])

    def test_notification_cannot_create_predictions(self):
        response = self.server.handle({"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "replicate_wan_3", "arguments": {"input": {"prompt": "A character waves."}, "request_key": "notice_take01"}}})
        self.assertIsNone(response)
        self.assertEqual(self.backend.calls, [])

    def test_protocol_envelopes_unknown_methods_and_bad_tool_shapes(self):
        cases = [([], -32600), ({"jsonrpc": "2.0", "id": True, "method": "ping"}, -32600), ({"jsonrpc": "2.0", "id": 4, "method": "not/a/method"}, -32601), ({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "not_a_tool"}}, -32602), ({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "replicate_wan_3", "arguments": []}}, -32602)]
        for message, code in cases:
            self.assertEqual(self.server.handle(message)["error"]["code"], code)

    def test_initialization_is_required_and_negotiates_version(self):
        server = Server(self.client)
        self.assertEqual(server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["error"]["code"], -32002)
        response = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "future-version", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}})
        self.assertEqual(response["result"]["protocolVersion"], "2025-11-25")
        self.assertEqual(response["result"]["capabilities"], {"tools": {}, "resources": {}})

    def test_client_metadata_and_initialize_shape(self):
        server = Server(self.client)
        invalid = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {}}})
        self.assertEqual(invalid["error"]["code"], -32602)
        listed = self.server.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/list", "params": {"_meta": {"client": "test"}}})
        self.assertEqual(len(listed["result"]["tools"]), 12)

    def test_http_redirect_refused_and_error_body_not_leaked(self):
        from client import NoRedirect
        with self.assertRaises(DomainError):
            NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.com")
        client = ReplicateClient(token="offline-fixture-token", roots=[self.root], state_path=self.root / "state.sqlite3")
        error = urllib.error.HTTPError("https://api.replicate.com", 422, "private error", {}, io.BytesIO(b"private prompt offline-fixture-token"))
        with patch("client.urllib.request.build_opener") as opener:
            opener.return_value.open.side_effect = error
            with self.assertRaises(DomainError) as raised:
                client.request("POST", "/models/alibaba/wan-3/predictions", {"input": {"prompt": "private"}})
        self.assertIn("HTTP 422", str(raised.exception))
        self.assertNotIn("private", str(raised.exception))
        self.assertNotIn("offline-fixture-token", str(raised.exception))

    def test_stdio_subprocess_handshake_errors_and_clean_stdout(self):
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "1"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "resources/list"},
            {"jsonrpc": "2.0", "id": 4, "method": "resources/read", "params": {"uri": "replicate-video://guides/veo-3.1"}},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "replicate_model_schema", "arguments": {"model": "alibaba/wan-3"}}},
        ]
        payload = "\n".join(json.dumps(m) for m in messages) + "\n" + "[" * 10000 + "0" + "]" * 10000 + '\n{"jsonrpc":"2.0","id":6,"method":"ping"}\n'
        env = {**os.environ, "REPLICATE_API_TOKEN": "", "REPLICATE_VIDEO_STATE": str(self.root / "stdio.sqlite3")}
        proc = subprocess.run([sys.executable, str(ROOT / "server.py")], input=payload, capture_output=True, text=True, timeout=15, env=env)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr, "")
        output = [json.loads(line) for line in proc.stdout.splitlines()]
        indexed = {m["id"]: m for m in output if m["id"] is not None}
        self.assertEqual(len(indexed[2]["result"]["tools"]), 12)
        self.assertEqual(len(indexed[3]["result"]["resources"]), 8)
        self.assertIn("reference_images", indexed[4]["result"]["contents"][0]["text"])
        self.assertFalse(indexed[5]["result"]["isError"])
        self.assertEqual(indexed[6]["result"], {})
        self.assertTrue(any(m.get("error", {}).get("code") == -32700 for m in output))
        self.assertFalse((self.root / "stdio.sqlite3").exists())


if __name__ == "__main__":
    unittest.main()
