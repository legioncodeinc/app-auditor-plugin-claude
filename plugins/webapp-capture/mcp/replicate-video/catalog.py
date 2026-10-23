"""Seven fixed video contracts, grounded in the bundled Replicate schemas."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODELS = {
    "wan_3": ("alibaba/wan-3", "Cinematic character motion and establishing scenes; text or one starting image. 2-30 seconds, 480p/720p/1080p. Image framing overrides aspect_ratio. No audio toggle or video-reference input."),
    "runway_gen_4_5": ("runwayml/gen-4.5", "Expressive character acting, physical action, and precise camera direction; text or one first-frame image. Exactly 5 or 10 seconds. No resolution, audio, last-frame, or video-reference control on this Replicate endpoint."),
    "veo_3_1": ("google/veo-3.1", "Character dialogue, environmental sound, and cinematic scenes with optional synchronized audio. Text, first/last frames, or 1-3 subject references. References require 16:9 and 8 seconds; use frames separately. 720p/1080p, 4/6/8 seconds."),
    "seedance_2_0": ("bytedance/seedance-2.0", "Character consistency, choreography, and music-driven scenes. First/last frames or up to 9 image, 3 video, and 3 audio references. Video/audio reference totals each <=15s. Label [Image1], [Video1], [Audio1] in the prompt. Audio references need image/video references. Native audio; intelligent duration -1; up to 15s."),
    "seedance_2_5": ("bytedance/seedance-2.5", "Longer character narratives and structured production briefs. Up to 30 image, 10 video, and 10 audio references; video/audio totals each <=30s. 4-30s or intelligent -1. First/last frames cannot mix with references. Frames/edit/extend require adaptive ratio; editing requires -1. Only 480p/720p on this endpoint, mp4/mov; native audio."),
    "kling_v3": ("kwaivgi/kling-v3-video", "Cinematic character scenes with explicit multi-shot timing and optional native audio. 3-15s, standard=720p/pro=1080p/4k. First/end images must be JPEG/PNG, <=10MB and >=300px; first-frame ratio 0.4-2.5. multi_prompt is a JSON string with up to 6 shots whose durations total duration. No video-reference input."),
    "grok_imagine_video": ("xai/grok-imagine-video", "Animate characters from images, create scenes from text, or edit an existing clip <=8.7s. 1-15s new generations, 480p/720p. Editing preserves input duration/ratio/resolution. Audio is native; there is no audio switch, seed, or negative-prompt field. Use positive motion direction."),
}


def schema_for(model):
    return json.loads((ROOT / "schemas" / (model.split("/")[1] + ".json")).read_text())


def dereference(value, document):
    if isinstance(value, list):
        return [dereference(v, document) for v in value]
    if not isinstance(value, dict):
        return value
    if "$ref" in value:
        target = document
        for part in value["$ref"].removeprefix("#/").split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return dereference({**target, **{k: v for k, v in value.items() if k != "$ref"}}, document)
    return {k: dereference(v, document) for k, v in value.items()}


def provider_input(model):
    doc = schema_for(model)["openapi_schema"]
    return dereference(doc["components"]["schemas"]["Input"], doc)


def clean_schema(value):
    if isinstance(value, list):
        return [clean_schema(v) for v in value]
    if not isinstance(value, dict):
        return value
    result = {k: clean_schema(v) for k, v in value.items() if k not in ("title", "x-order", "nullable")}
    if value.get("nullable"):
        result = {"anyOf": [result, {"type": "null"}]}
    return result


def object_schema(properties, required=()):
    return {"type": "object", "properties": properties, "required": list(required), "additionalProperties": False}


ID = {"type": "string", "pattern": "^[a-zA-Z0-9_-]{1,128}$", "description": "Replicate identifier, without a URL or path."}
FILE = {"oneOf": [
    object_schema({"path": {"type": "string", "minLength": 1, "description": "Local media path within REPLICATE_UPLOAD_ROOTS; automatically uploaded through the shared file endpoint."}}, ["path"]),
    object_schema({"file_id": {**ID, "description": "Unexpired file_id previously returned by replicate_upload_file on this server."}}, ["file_id"]),
], "description": "Reference media: local path for automatic upload, or a file_id from replicate_upload_file. Arbitrary URLs and data URIs are not accepted."}


def is_media(schema):
    return schema.get("format") == "uri" or schema.get("items", {}).get("format") == "uri"


def model_input(model):
    result = clean_schema(provider_input(model))
    result["additionalProperties"] = False
    for key, original in provider_input(model)["properties"].items():
        if is_media(original):
            media = copy.deepcopy(FILE)
            media["description"] = original.get("description", "Reference media") + " " + FILE["description"]
            if original.get("type") == "array":
                limit = {"reference_images": 30, "reference_videos": 10, "reference_audios": 10} if model.endswith("2.5") else {"reference_images": 9, "reference_videos": 3, "reference_audios": 3}
                if model == "google/veo-3.1":
                    limit = {"reference_images": 3}
                media = {"type": "array", "items": media, "maxItems": limit[key], "description": media["description"]}
            result["properties"][key] = media
    if model == "kwaivgi/kling-v3-video":
        for key in ("prompt", "negative_prompt"):
            result["properties"][key]["maxLength"] = 2500
    if model == "alibaba/wan-3":
        result["properties"]["seed"] = {"type": "integer", "minimum": 0, "maximum": 2147483647, "description": "Reproducibility seed; documented range 0-2147483647."}
    if model.endswith("seedance-2.5"):
        result["properties"]["duration"] = {"type": "integer", "anyOf": [{"const": -1}, {"minimum": 4, "maximum": 30}], "description": "4-30 seconds, or -1 for intelligent duration. Editing requires -1."}
    return result


REQUEST_KEY = {"type": "string", "pattern": "^[a-zA-Z0-9_-]{8,128}$", "description": "Unique client request key. Reuse the SAME key and arguments after an uncertain response; the durable ledger prevents a second generation POST. Changed arguments need a new key."}


def tool_catalog():
    tools = []
    for slug, (model, description) in MODELS.items():
        properties = {"input": model_input(model), "request_key": REQUEST_KEY}
        properties["input"]["description"] = "This model's published controls. Media fields use the upload wrapper; omitted provider controls keep provider defaults."
        if model.endswith("seedance-2.5"):
            properties["workflow"] = {"type": "string", "enum": ["generate", "edit", "extend"], "description": "Server workflow validation, not sent to Replicate. Default generate. Edit/extend require reference_videos; edit also requires duration=-1."}
        tools.append({"name": "replicate_" + slug, "title": model, "description": description + " Creates one PAID asynchronous prediction at /v1/models/" + model + "/predictions. Returns prediction_id/status/output_urls and polling guidance. Local references call replicate_upload_file internally. Read the model guide first. No blind retries; reuse request_key.", "inputSchema": object_schema(properties, ["input", "request_key"]), "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True}})
    tools.extend([
        {"name": "replicate_upload_file", "description": "Upload a local character image, scene image, video, or audio reference to POST /v1/files as multipart content. Returns file_id, url, expiry, checksum, type, size, and probed media metadata. Only allowed upload roots; under 100MB. Reuses identical unexpired uploads. Required before file_id references; generation also invokes this same uploader for path references. Uploads media to Replicate; does not generate video.", "inputSchema": object_schema({"path": {"type": "string", "minLength": 1, "description": "Local media file path within REPLICATE_UPLOAD_ROOTS; default root is the server working directory."}}, ["path"]), "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True}},
        {"name": "replicate_model_schema", "description": "Read the bundled researched schema and constraints for one of the seven video models. Optional refresh retrieves the current Replicate model schema and reports drift without changing the bundled contract. Read-only; no generation charge.", "inputSchema": object_schema({"model": {"type": "string", "enum": [v[0] for v in MODELS.values()], "description": "Exact allowlisted Replicate owner/model."}, "refresh": {"type": "boolean", "description": "Fetch live schema and compare, default false; needs REPLICATE_API_TOKEN."}}, ["model"]), "annotations": {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": True}},
        {"name": "replicate_get_prediction", "description": "Read status/output URLs for a prediction belonging to one of the seven video models. Returns starting/processing/succeeded/failed/canceled, sanitized failure, metrics, and suggested poll interval. Read-only. Poll at the returned interval; video jobs are asynchronous and have no automatic regeneration.", "inputSchema": object_schema({"prediction_id": ID}, ["prediction_id"]), "annotations": {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": True}},
        {"name": "replicate_cancel_prediction", "description": "Cancel a prediction belonging to one of the seven video models after checking its model. Changes remote prediction state; cannot undo completed work or promise a refund. Returns prediction status. Use only when cancellation is requested.", "inputSchema": object_schema({"prediction_id": ID}, ["prediction_id"]), "annotations": {"readOnlyHint": False, "destructiveHint": True, "idempotentHint": True, "openWorldHint": True}},
    ])
    tools.append({"name": "replicate_production_doctor", "description": "Read-only production health check: token availability without revealing it, Python, media tools, allowed folders, platform, and optional authenticated model-schema GET. Never uploads, generates, repairs settings, or installs software. Use this before production; use the standalone doctor script if this MCP is disconnected.", "inputSchema": object_schema({"live": {"type": "boolean", "description": "Perform a read-only authentication/schema GET; default false."}, "model": {"type": "string", "enum": [v[0] for v in MODELS.values()], "description": "Allowlisted model for read-only access check; defaults to first model."}}), "annotations": {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": True}})
    return tools


def validate(value, schema, path="arguments"):
    """Validate the finite JSON Schema vocabulary used by this fixed catalog."""
    if "anyOf" in schema or "oneOf" in schema:
        variants = schema.get("anyOf", schema.get("oneOf"))
        matches = 0
        for branch in variants:
            try:
                validate(value, branch, path)
                matches += 1
            except ValueError:
                pass
        if matches == 0 or ("oneOf" in schema and matches != 1):
            raise ValueError(f"{path}: does not match an allowed input shape")
    kind = schema.get("type")
    valid = {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str), "integer": isinstance(value, int) and not isinstance(value, bool), "number": isinstance(value, (int, float)) and not isinstance(value, bool), "boolean": isinstance(value, bool), "null": value is None}
    if kind and not valid.get(kind, False):
        raise ValueError(f"{path}: expected {kind}")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path}: value is not in the published enum")
    if "const" in schema and value != schema["const"]:
        raise ValueError(f"{path}: expected {schema['const']}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", float("-inf")) or value > schema.get("maximum", float("inf")):
            raise ValueError(f"{path}: outside the documented range")
    if isinstance(value, str):
        import re
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", float("inf")):
            raise ValueError(f"{path}: invalid text length")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            raise ValueError(f"{path}: invalid identifier format")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", float("inf")):
            raise ValueError(f"{path}: invalid number of references")
        for index, item in enumerate(value):
            validate(item, schema.get("items", {}), f"{path}[{index}]")
    if isinstance(value, dict) and "properties" in schema:
        properties = schema["properties"]
        for key in schema.get("required", []):
            if key not in value:
                raise ValueError(f"{path}.{key}: required")
        for key, item in value.items():
            if key not in properties:
                if schema.get("additionalProperties") is False:
                    raise ValueError(f"{path}: unsupported field {key}")
            else:
                validate(item, properties[key], f"{path}.{key}")
