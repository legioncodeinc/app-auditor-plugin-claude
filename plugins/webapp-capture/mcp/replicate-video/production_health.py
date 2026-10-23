"""Read-only production diagnostics. Never returns or persists credentials."""
import os
import shutil
import sys


def check_health(client, model, live=False):
    token = client.token
    present = isinstance(token, str) and bool(token.strip()) and not token.startswith("${")
    checks = [
        {"name": "python", "status": "PASS" if sys.version_info >= (3, 11) else "FAIL", "detail": "Python 3.11+ is required."},
        {"name": "token", "status": "PASS" if present else "FAIL", "detail": "REPLICATE_API_TOKEN is available." if present else "No Replicate token. Easiest fix: run python3 mcp/replicate-video/scripts/set_token.py in your own terminal, then restart the app. Or set REPLICATE_API_TOKEN in the environment that launches the plugin. Never paste it into chat or tool arguments."},
        {"name": "ffprobe", "status": "PASS" if shutil.which("ffprobe") else "FAIL", "detail": "Required for inspected reference uploads."},
        {"name": "ffmpeg", "status": "PASS" if shutil.which("ffmpeg") else "WARN", "detail": "Needed for frame sheets, repairs and music assembly."},
        {"name": "file_platform", "status": "PASS" if os.name == "posix" else "FAIL", "detail": "The supplied upload implementation supports macOS/Linux directory-FD protection."},
        {"name": "upload_roots", "status": "PASS" if client.roots and all(root.is_dir() for root in client.roots) else "FAIL", "detail": "Allowed reference folders exist."},
        {"name": "image_backend", "status": "HOST_CHECK", "detail": "The chat must verify an authorized image-generation/editing tool is available. Python cannot prove host tool access."},
    ]
    api = {"checked": False, "model": model, "status": "NOT_CHECKED"}
    if live and present:
        try:
            value = client.live_schema(model)
            api.update(checked=True, status="FAIL" if value["drift"] else "PASS", schema_drift=value["drift"])
            api["detail"] = "Published inputs changed; review the model contract before a paid run." if value["drift"] else "Authentication, model access and input contract passed a read-only GET."
        except Exception:
            api.update(checked=True, status="FAIL", detail="Read-only provider check failed. Check account access, connectivity and token validity; no upload or generation was submitted.")
    elif live:
        api.update(status="FAIL", detail="A missing token prevented the provider check.")
    failures = any(check["status"] == "FAIL" for check in checks) or api["status"] == "FAIL"
    return {"status": "NEEDS_ATTENTION" if failures else "PASS", "checks": checks, "provider": api, "credential_value_disclosed": False, "uploads": 0, "generations": 0, "scope": "MCP and local production readiness; host image tools require a separate capability check."}
