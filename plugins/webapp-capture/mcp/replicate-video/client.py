"""Bounded Replicate HTTP calls, inspected uploads, and durable duplicate protection."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import stat
import subprocess
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid

from catalog import MODELS, dereference, is_media, provider_input

API = "https://api.replicate.com/v1"
ALLOWED = {item[0] for item in MODELS.values()}
MAX_FILE = 100_000_000
MAX_REFERENCE_BYTES = 250_000_000


class DomainError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise DomainError("Replicate API redirect refused; credentials are never forwarded.")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def unexpired(value):
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")) > dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=60)
    except (ValueError, TypeError, AttributeError):
        return False


def comparable_schema(value):
    """Normalize observed API/card encoding differences without dropping constraints."""
    if isinstance(value, list):
        return [comparable_schema(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {
        key: comparable_schema(item) for key, item in value.items()
        if key not in ("title", "x-order")
        and not (key == "default" and item is None and value.get("nullable"))
    }
    branches = result.get("allOf")
    if isinstance(branches, list) and len(branches) == 1 and isinstance(branches[0], dict):
        branch = dict(branches[0])
        siblings = {key: item for key, item in result.items() if key != "allOf"}
        # Pydantic's generic enum annotation is replaced by the field description
        # in Replicate's dereferenced public card. Keep any substantive description.
        if "description" in siblings and branch.get("description") == "An enumeration.":
            branch.pop("description")
        if all(key not in siblings or canonical(siblings[key]) == canonical(item) for key, item in branch.items()):
            return {**branch, **siblings}
    return result


class Ledger:
    def __init__(self, path):
        path = Path(path)
        if not path.parent.exists():
            path.parent.mkdir(mode=0o700, parents=True)
        if not path.exists():
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.Lock()
        with self.db:
            self.db.execute("CREATE TABLE IF NOT EXISTS requests (scope TEXT, key TEXT, hash TEXT, result TEXT, PRIMARY KEY(scope,key))")
            self.db.execute("CREATE TABLE IF NOT EXISTS files (scope TEXT, hash TEXT, result TEXT, PRIMARY KEY(scope,hash))")

    def begin(self, scope, key, digest):
        with self.lock, self.db:
            row = self.db.execute("SELECT hash,result FROM requests WHERE scope=? AND key=?", (scope, key)).fetchone()
            if row:
                if row[0] != digest:
                    raise DomainError("request_key already belongs to different arguments; use a new key for a different intended generation.")
                if row[1] is None:
                    raise DomainError("This request_key has an unresolved submission. Do not create another paid job. Inspect Replicate's prediction history before deciding whether to use a new key.")
                return json.loads(row[1])
            self.db.execute("INSERT INTO requests VALUES (?,?,?,NULL)", (scope, key, digest))
        return None

    def finish(self, scope, key, result):
        with self.lock, self.db:
            self.db.execute("UPDATE requests SET result=? WHERE scope=? AND key=?", (canonical(result), scope, key))

    def file(self, scope, digest=None, file_id=None):
        with self.lock:
            if digest:
                row = self.db.execute("SELECT result FROM files WHERE scope=? AND hash=?", (scope, digest)).fetchone()
                return json.loads(row[0]) if row else None
            for row in self.db.execute("SELECT result FROM files WHERE scope=?", (scope,)):
                value = json.loads(row[0])
                if value["file_id"] == file_id:
                    return value
        return None

    def save_file(self, scope, digest, result):
        with self.lock, self.db:
            self.db.execute("INSERT OR REPLACE INTO files VALUES (?,?,?)", (scope, digest, canonical(result)))


def media_type(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith(b"BM"):
        return "image/bmp"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    if data[:4] == b"RIFF" and data[8:12] == b"WAVE":
        return "audio/wav"
    if data.startswith(b"fLaC"):
        return "audio/flac"
    if data.startswith(b"ID3") or (len(data) > 1 and data[0] == 255 and data[1] & 0xE0 == 0xE0):
        return "audio/mpeg"
    if data.startswith(b"OggS"):
        return "audio/ogg"
    if data.startswith(b"\x1a\x45\xdf\xa3"):
        return "video/webm"
    if data[4:8] == b"ftyp":
        return "video/quicktime" if data[8:12] == b"qt  " else "video/mp4"
    raise DomainError("Unsupported media content. Use PNG/JPEG/WebP/BMP, MP4/MOV/WebM, or WAV/MP3/FLAC/OGG/M4A references.")


def inspect_media(data, mime):
    executable = shutil.which("ffprobe")
    if not executable:
        raise DomainError("ffprobe is required to inspect reference media before upload; it is not installed automatically.")
    with tempfile.NamedTemporaryFile(prefix="replicate-video-") as handle:
        handle.write(data)
        handle.flush()
        try:
            proc = subprocess.run([executable, "-v", "error", "-protocol_whitelist", "file,pipe", "-show_entries", "format=duration:stream=codec_type,width,height", "-of", "json", handle.name], capture_output=True, timeout=20, check=False)
            info = json.loads(proc.stdout) if proc.returncode == 0 else None
        except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
            info = None
    if not info or not info.get("streams"):
        raise DomainError("Reference media could not be decoded by ffprobe; provide a valid media file.")
    video = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    audio = any(s.get("codec_type") == "audio" for s in info["streams"])
    if video and any(type(video.get(key)) is not int or video[key] <= 0 for key in ("width", "height")):
        raise DomainError("Reference image/video dimensions could not be decoded; provide valid media.")
    if mime.startswith("image/") and not video:
        raise DomainError("The file does not contain a valid image.")
    if mime.startswith("audio/") and (not audio or video):
        raise DomainError("The file does not contain a supported audio-only reference.")
    if mime.startswith("video/") and not video:
        if audio:
            mime = "audio/mp4"
        else:
            raise DomainError("The file does not contain a supported video or audio stream.")
    result = {"content_type": mime}
    if video:
        result.update(width=video.get("width"), height=video.get("height"))
    if not mime.startswith("image/"):
        try:
            duration = float(info["format"]["duration"])
            if not 0 < duration < float("inf"):
                raise ValueError
            result["duration_seconds"] = duration
        except (KeyError, ValueError, TypeError):
            raise DomainError("Reference duration could not be measured; use a seekable MP4/MOV or supported audio file.")
    return result


def open_media_under_root(candidate, root):
    """Walk from / with directory FDs; no ancestor or final symlink is followed."""
    if os.open not in os.supports_dir_fd or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise DomainError("Reference uploads require POSIX directory-FD and no-follow support (macOS/Linux).")
    directory = os.open(root.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        parts = (*root.parts[1:], *candidate.relative_to(root).parts)
        if not parts:
            raise DomainError("Upload path must name a regular media file.")
        for part in parts[:-1]:
            next_directory = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = next_directory
        return os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    finally:
        os.close(directory)


class ReplicateClient:
    def __init__(self, *, token=None, roots=None, state_path=None, transport=None):
        self.token = token if token is not None else os.environ.get("REPLICATE_API_TOKEN", "")
        self.roots = [Path(p).expanduser().resolve() for p in (roots or os.environ.get("REPLICATE_UPLOAD_ROOTS", str(Path.cwd())).split(os.pathsep))]
        self.state_path = state_path or os.environ.get("REPLICATE_VIDEO_STATE", str(Path.home() / ".local/state/replicate-video-mcp/state.sqlite3"))
        self._ledger = None
        self.state_lock = threading.Lock()
        self.upload_lock = threading.Lock()
        self.scope = hashlib.sha256(self.token.encode()).hexdigest()
        self.transport = transport

    @property
    def ledger(self):
        with self.state_lock:
            if self._ledger is None:
                self._ledger = Ledger(self.state_path)
        return self._ledger

    def authenticated(self):
        if not self.token.strip():
            raise DomainError("REPLICATE_API_TOKEN is missing. Supply it in the server environment; never put it in tool arguments.")

    def request(self, method, path, body=None, content_type="application/json"):
        self.authenticated()
        if not path.startswith("/") or ".." in path or "?" in path:
            raise DomainError("Invalid Replicate API path.")
        if self.transport:
            return self.transport(method, path, body, content_type)
        payload = body if isinstance(body, bytes) else (canonical(body).encode() if body is not None else None)
        request = urllib.request.Request(API + path, data=payload, method=method, headers={"Authorization": "Bearer " + self.token, "Content-Type": content_type, "Accept": "application/json", "User-Agent": "replicate-video-mcp/1.0"})
        try:
            with urllib.request.build_opener(NoRedirect).open(request, timeout=45) as response:
                data = response.read(4_000_001)
                if len(data) > 4_000_000:
                    raise DomainError("Replicate API response exceeded the 4MB response limit.")
                value = json.loads(data)
                if not isinstance(value, dict):
                    raise DomainError("Replicate returned an unexpected response shape.")
                return value
        except urllib.error.HTTPError as error:
            # Do not surface provider bodies, which can echo prompts, credentials or signed URLs.
            messages = {401: "Check the server's REPLICATE_API_TOKEN.", 403: "Check account access to this model.", 404: "The model, prediction, or file was not found.", 422: "Replicate rejected the inputs; compare the model schema.", 429: "Rate limit reached; wait before retrying read-only calls."}
            raise DomainError(f"Replicate HTTP {error.code}. {messages.get(error.code, 'Provider request failed.')} Mutating requests are never retried automatically.") from None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
            raise DomainError("Replicate connection or response failed. A submission may have reached Replicate; reuse the same request_key, and inspect prediction history if it remains unresolved.") from None

    def live_schema(self, model):
        value = self.request("GET", "/models/" + model)
        version = value.get("latest_version") or {}
        doc = version.get("openapi_schema")
        if not isinstance(doc, dict):
            raise DomainError("Replicate did not return the live model schema; no upload or generation was attempted.")
        try:
            current = dereference(doc["components"]["schemas"]["Input"], doc)
        except (KeyError, TypeError):
            raise DomainError("Replicate returned an unsupported schema shape; no upload or generation was attempted.") from None
        return {"version": version.get("id"), "input_schema": current, "drift": canonical(comparable_schema(current)) != canonical(comparable_schema(provider_input(model)))}

    def prepare_file(self, path):
        self.authenticated()
        candidate = Path(path).expanduser().resolve()
        root = next((root for root in self.roots if candidate.is_relative_to(root)), None)
        if root is None:
            raise DomainError("File is outside REPLICATE_UPLOAD_ROOTS. Use a file in an allowed root.")
        try:
            fd = open_media_under_root(candidate, root)
            with os.fdopen(fd, "rb") as handle:
                info = os.fstat(handle.fileno())
                if not stat.S_ISREG(info.st_mode):
                    raise DomainError("Only regular media files can be uploaded.")
                if not 0 < info.st_size < MAX_FILE:
                    raise DomainError("Media files must be nonempty and less than 100MB.")
                data = handle.read(MAX_FILE)
                if len(data) >= MAX_FILE:
                    raise DomainError("Media files must be less than 100MB.")
        except OSError:
            raise DomainError("The reference file is missing or unreadable.") from None
        media = inspect_media(data, media_type(data))
        return {"data": data, "sha256": hashlib.sha256(data).hexdigest(), **media}

    def upload_prepared(self, prepared):
        digest = fingerprint({"sha256": prepared["sha256"], "type": prepared["content_type"]})
        with self.upload_lock:
            cached = self.ledger.file(self.scope, digest=digest)
            if cached and unexpired(cached.get("expires_at")):
                return {**cached, "reused": True}
            boundary = "replicate-video-" + uuid.uuid4().hex
            # Neutral filename avoids sending local filenames or directory names to the provider.
            extension = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/bmp": "bmp", "video/mp4": "mp4", "video/quicktime": "mov", "video/webm": "webm", "audio/wav": "wav", "audio/flac": "flac", "audio/mpeg": "mp3", "audio/ogg": "ogg", "audio/mp4": "m4a"}[prepared["content_type"]]
            header = f'--{boundary}\r\nContent-Disposition: form-data; name="content"; filename="reference.{extension}"\r\nContent-Type: {prepared["content_type"]}\r\n\r\n'.encode()
            body = header + prepared["data"] + f"\r\n--{boundary}--\r\n".encode()
            result = self.request("POST", "/files", body, "multipart/form-data; boundary=" + boundary)
            try:
                file_id = result["id"]
                url = result["urls"]["get"]
                parsed = urllib.parse.urlsplit(url)
                if parsed.scheme != "https" or parsed.hostname not in ("api.replicate.com", "replicate.delivery") and not (parsed.hostname or "").endswith(".replicate.delivery"):
                    raise ValueError
                if not unexpired(result["expires_at"]):
                    raise ValueError
                if not isinstance(file_id, str) or not file_id:
                    raise ValueError
            except (KeyError, TypeError, ValueError):
                raise DomainError("Upload returned an unusable file ID, URL or expiry; no prediction was submitted.") from None
            normalized = {"file_id": file_id, "url": url, "expires_at": result["expires_at"], "size": len(prepared["data"]), "sha256": prepared["sha256"], **{k: v for k, v in prepared.items() if k not in ("data", "sha256")}, "reused": False}
            self.ledger.save_file(self.scope, digest, normalized)
            return normalized

    def upload(self, path):
        return self.upload_prepared(self.prepare_file(path))

    def reference(self, value):
        if "path" in value:
            return self.prepare_file(value["path"])
        file = self.ledger.file(self.scope, file_id=value["file_id"])
        if not file or not unexpired(file.get("expires_at")):
            raise DomainError("Unknown or expired file_id. Upload the reference with replicate_upload_file again.")
        return file

    def reference_rules(self, model, field, media):
        kind = "audio" if "audio" in field else "video" if "video" in field else "image"
        if not media["content_type"].startswith(kind + "/"):
            raise DomainError(f"{field} requires {kind} media.")
        if model == "alibaba/wan-3" and field == "image":
            if len(media.get("data", b"")) > 10_000_000 or media.get("size", 0) > 10_000_000:
                raise DomainError("Wan first-frame images must be <=10MB.")
        if model == "kwaivgi/kling-v3-video":
            if media["content_type"] not in ("image/jpeg", "image/png"):
                raise DomainError("Kling frames must be JPEG or PNG.")
            if len(media.get("data", b"")) > 10_000_000 or media.get("size", 0) > 10_000_000:
                raise DomainError("Kling frames must be <=10MB.")
            if min(media.get("width", 0), media.get("height", 0)) < 300:
                raise DomainError("Kling frame dimensions must each be >=300px.")
            if field == "start_image" and not 0.4 <= media["width"] / media["height"] <= 2.5:
                raise DomainError("Kling first-frame aspect ratio must be between 0.4 and 2.5.")
        if model == "xai/grok-imagine-video":
            if kind == "image" and media["content_type"] not in ("image/jpeg", "image/png", "image/webp"):
                raise DomainError("Grok images must be JPEG, PNG or WebP.")
            if kind == "video" and media["duration_seconds"] > 8.7:
                raise DomainError("Grok editing input must be <=8.7 seconds.")

    def generate(self, model, args):
        self.authenticated()
        supplied = args["input"]
        validate_combinations(model, supplied, args.get("workflow", "generate"))
        digest = fingerprint({"model": model, "arguments": args})
        # Check the ledger before live schema or file checks: completed repeats always return the original job.
        with self.ledger.lock:
            row = self.ledger.db.execute("SELECT hash,result FROM requests WHERE scope=? AND key=?", (self.scope, args["request_key"])).fetchone()
        if row:
            return self.ledger.begin(self.scope, args["request_key"], digest)
        live = self.live_schema(model)
        if live["drift"]:
            raise DomainError("The published model inputs changed since the bundled research. Use replicate_model_schema with refresh=true and update the contract before spending.")
        prepared = {}
        total_reference_bytes = 0
        for field, schema in provider_input(model)["properties"].items():
            if is_media(schema) and field in supplied:
                values = supplied[field] if schema.get("type") == "array" else [supplied[field]]
                prepared[field] = []
                for value in values:
                    media = self.reference(value)
                    total_reference_bytes += len(media.get("data", b"")) or media.get("size", 0)
                    if total_reference_bytes > MAX_REFERENCE_BYTES:
                        raise DomainError("Combined reference media must be <=250MB per generation; no uploads or prediction were submitted.")
                    prepared[field].append(media)
                for media in prepared[field]:
                    self.reference_rules(model, field, media)
                if field in ("reference_videos", "reference_audios"):
                    limit = 30 if model.endswith("2.5") else 15
                    if sum(m["duration_seconds"] for m in prepared[field]) > limit:
                        raise DomainError(f"{field} combined duration must be <= {limit} seconds.")
        cached = self.ledger.begin(self.scope, args["request_key"], digest)
        if cached:
            return cached
        inputs = dict(supplied)
        uploads = []
        for field, values in prepared.items():
            files = [self.upload_prepared(media) if "data" in media else media for media in values]
            uploads.extend(file["file_id"] for file in files)
            inputs[field] = [file["url"] for file in files] if isinstance(supplied[field], list) else files[0]["url"]
        response = self.request("POST", "/models/" + model + "/predictions", {"input": inputs})
        result = prediction_result(response, expected_model=model)
        result.update(request_key=args["request_key"], uploaded_file_ids=uploads)
        self.ledger.finish(self.scope, args["request_key"], result)
        return result

    def prediction(self, prediction_id, cancel=False):
        value = self.request("GET", "/predictions/" + prediction_id)
        if value.get("model") not in ALLOWED:
            raise DomainError("Prediction does not belong to one of the seven allowed video models.")
        if cancel and value.get("status") not in ("succeeded", "failed", "canceled"):
            value = self.request("POST", "/predictions/" + prediction_id + "/cancel")
        return prediction_result(value)


def validate_combinations(model, inputs, workflow="generate"):
    def present(key):
        return bool(inputs.get(key))
    if "prompt" in inputs and not inputs["prompt"].strip() and not (model.endswith("2.5") and any(present(k) for k in ("image", "reference_images", "reference_videos"))):
        raise DomainError("A nonempty scene prompt is required unless Seedance 2.5 has usable visual media.")
    if model == "google/veo-3.1":
        if present("last_frame") and not present("image"):
            raise DomainError("Veo last_frame requires image.")
        if present("reference_images"):
            if inputs.get("aspect_ratio", "16:9") != "16:9" or inputs.get("duration", 8) != 8:
                raise DomainError("Veo reference_images require 16:9 and duration=8.")
            if present("image") or present("last_frame"):
                raise DomainError("Choose Veo subject references or first/last frames separately.")
    if model.startswith("bytedance/"):
        if present("last_frame_image") and not present("image"):
            raise DomainError("Seedance last_frame_image requires image.")
        reference_keys = ("reference_images", "reference_videos", "reference_audios") if model.endswith("2.5") else ("reference_images",)
        if (present("image") or present("last_frame_image")) and any(present(k) for k in reference_keys):
            raise DomainError("Seedance first/last frames conflict with the selected reference mode.")
        if present("reference_audios") and not (present("reference_images") or present("reference_videos")):
            raise DomainError("Seedance reference_audios require reference_images or reference_videos.")
        if model.endswith("2.5"):
            if not present("prompt") and not any(present(k) for k in ("image", "reference_images", "reference_videos")):
                raise DomainError("Seedance 2.5 requires a prompt or visual media.")
            if workflow in ("edit", "extend") and not present("reference_videos"):
                raise DomainError("Seedance 2.5 edit/extend requires reference_videos.")
            if (present("image") or workflow in ("edit", "extend")) and inputs.get("aspect_ratio", "16:9") != "adaptive":
                raise DomainError("Seedance 2.5 frames/edit/extend require aspect_ratio=adaptive.")
            if workflow == "edit" and inputs.get("duration", 5) != -1:
                raise DomainError("Seedance 2.5 editing requires duration=-1.")
    if model == "kwaivgi/kling-v3-video":
        if present("end_image") and not present("start_image"):
            raise DomainError("Kling end_image requires start_image.")
        if present("multi_prompt"):
            try:
                shots = json.loads(inputs["multi_prompt"])
                valid = isinstance(shots, list) and 1 <= len(shots) <= 6
                valid = valid and all(isinstance(s, dict) and set(s) == {"prompt", "duration"} and isinstance(s["prompt"], str) and 0 < len(s["prompt"].strip()) <= 2500 and type(s["duration"]) is int and s["duration"] >= 1 for s in shots)
                valid = valid and sum(s["duration"] for s in shots) == inputs.get("duration", 5)
                if not valid:
                    raise ValueError
            except (ValueError, TypeError, KeyError):
                raise DomainError("Kling multi_prompt must be a JSON array string with 1-6 prompt/duration shots, each >=1s, totaling duration.") from None
    if model == "xai/grok-imagine-video" and present("video"):
        if present("image"):
            raise DomainError("Choose Grok image animation or video editing separately.")
        if any(key in inputs for key in ("duration", "aspect_ratio", "resolution")):
            raise DomainError("Grok editing ignores duration/aspect_ratio/resolution; omit these controls.")


def prediction_result(value, expected_model=None):
    model = value.get("model") or expected_model
    if model not in ALLOWED or expected_model and model != expected_model:
        raise DomainError("Replicate returned an unexpected prediction model.")
    if not value.get("id") or value.get("status") not in ("starting", "processing", "succeeded", "failed", "canceled"):
        raise DomainError("Replicate returned an invalid prediction ID or status; submission outcome may be uncertain.")
    output = value.get("output")
    urls = [output] if isinstance(output, str) else output if isinstance(output, list) else []
    urls = [url for url in urls if isinstance(url, str) and urllib.parse.urlsplit(url).scheme == "https"]
    result = {"prediction_id": value["id"], "model": model, "status": value["status"], "output_urls": urls, "poll_after_seconds": 15 if value["status"] in ("starting", "processing") else 0, "web_url": "https://replicate.com/p/" + urllib.parse.quote(value["id"], safe=""), "metrics": {k: v for k, v in (value.get("metrics") or {}).items() if k in ("predict_time", "total_time") and isinstance(v, (float, int))}, "output_notice": "Replicate API output files are temporary. Save completed media promptly."}
    if value["status"] == "failed":
        result["error"] = "Prediction failed at Replicate. Inspect the prediction page for provider details; no retry or new charge was initiated."
    return result
