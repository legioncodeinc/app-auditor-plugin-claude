#!/usr/bin/env python3
"""Independent bootstrap doctor, usable even when the host MCP connection is down."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from catalog import MODELS, tool_catalog


def diagnose(live=False, project=None, timeout=55):
    model = next(iter(MODELS.values()))[0]
    expected = {tool["name"] for tool in tool_catalog()}
    environment = os.environ.copy()
    if project:
        project = Path(project).expanduser().resolve()
        if not project.is_dir():
            return {"status": "FAIL", "error": "Project folder does not exist.", "credential_value_disclosed": False}
        environment["REPLICATE_UPLOAD_ROOTS"] = str(project)
    messages = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "production-doctor", "version": "1.0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "resources/list"},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "replicate_production_doctor", "arguments": {"live": live, "model": model}}},
    ]
    try:
        process = subprocess.run([sys.executable, str(ROOT / "launch.py")], input="".join(json.dumps(m) + "\n" for m in messages), text=True, capture_output=True, cwd=project or ROOT, env=environment, timeout=timeout)
        if process.returncode or len(process.stdout) > 2_000_000:
            raise ValueError
        responses = [json.loads(line) for line in process.stdout.splitlines()]
        if any(not isinstance(response, dict) for response in responses):
            raise ValueError("Invalid protocol response")
        indexed = {response.get("id"): response for response in responses}
        tools = indexed[2]["result"]["tools"]
        resources = indexed[3]["result"]["resources"]
        actual = {tool["name"] for tool in tools}
        health = indexed[4]["result"]["structuredContent"]
        match = actual == expected
        return {**health, "connection": {"status": "PASS" if match else "FAIL", "handshake": indexed[1]["result"]["protocolVersion"], "tools": len(tools), "guides": len(resources), "expected_tools_match": match, "stderr_empty": not process.stderr}, "status": health["status"] if match else "FAIL"}
    except (subprocess.TimeoutExpired, OSError, ValueError, KeyError, TypeError):
        return {"status": "FAIL", "error": "MCP startup, discovery or health response failed. Check Python 3.11+, plugin files and the host MCP connection. No automatic repair or paid operation was attempted.", "credential_value_disclosed": False, "uploads": 0, "generations": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Make one read-only provider GET to verify authentication and schema.")
    parser.add_argument("--project", help="Existing production folder to check in the diagnostic child only.")
    args = parser.parse_args()
    result = diagnose(args.live, args.project)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
