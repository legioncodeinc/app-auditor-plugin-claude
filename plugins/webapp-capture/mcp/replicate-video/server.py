#!/usr/bin/env python3
"""MCP stdio server, using only Python's standard library (Python 3.11+)."""
import concurrent.futures
import json
from pathlib import Path
import sys
import threading

from catalog import MODELS, ROOT, provider_input, schema_for, tool_catalog, validate
from client import DomainError, ReplicateClient

VERSIONS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
MAX_MESSAGE = 1_000_000


def result(value, is_error=False):
    return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, allow_nan=False)}], "structuredContent": value, "isError": is_error}


class ProtocolError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class Server:
    def __init__(self, client=None):
        self.client = client or ReplicateClient()
        self.tools = {tool["name"]: tool for tool in tool_catalog()}
        self.models = {"replicate_" + slug: model for slug, (model, _) in MODELS.items()}
        self.initialized = False
        self.ready = False
        self.resources = {}
        guides = ROOT / "guides"  # model guides travel with the server, not with a skill folder
        for path in sorted(guides.glob("*.md")):
            uri = "replicate-video://guides/" + path.stem
            self.resources[uri] = path

    def dispatch(self, method, params):
        if not isinstance(params, dict):
            raise ProtocolError(-32602, "params must be an object")
        if method == "initialize":
            if self.initialized:
                raise ProtocolError(-32600, "Already initialized")
            info = params.get("clientInfo")
            if not isinstance(params.get("protocolVersion"), str) or not isinstance(params.get("capabilities"), dict) or not isinstance(info, dict) or not all(isinstance(info.get(key), str) for key in ("name", "version")):
                raise ProtocolError(-32602, "initialize requires protocolVersion, capabilities, clientInfo")
            self.initialized = True
            return {"protocolVersion": params["protocolVersion"] if params["protocolVersion"] in VERSIONS else VERSIONS[0], "capabilities": {"tools": {}, "resources": {}}, "serverInfo": {"name": "replicate-video-mcp", "version": "1.0.0"}, "instructions": "Seven video models only. Read a model guide, upload reference media or use path references for automatic upload, then call that model's tool with a unique request_key. Generations are paid. Reuse keys after uncertain submissions; poll existing IDs. REPLICATE_API_TOKEN stays in the server environment."}
        if method == "ping":
            return {}
        if method == "notifications/initialized":
            if not self.initialized:
                raise ProtocolError(-32600, "initialize must complete first")
            self.ready = True
            return None
        if not self.ready:
            raise ProtocolError(-32002, "Server is not initialized")
        if method == "tools/list":
            if set(params) - {"_meta"}:
                raise ProtocolError(-32602, "This fixed catalog has no pagination parameters")
            return {"tools": list(self.tools.values())}
        if method == "resources/list":
            if set(params) - {"_meta"}:
                raise ProtocolError(-32602, "This guide catalog has no pagination parameters")
            return {"resources": [{"uri": uri, "name": path.stem, "description": "Character and scene production guide: " + path.stem, "mimeType": "text/markdown"} for uri, path in self.resources.items()]}
        if method == "resources/read":
            uri = params.get("uri")
            if not isinstance(uri, str) or uri not in self.resources:
                raise ProtocolError(-32602, "Unknown guide resource")
            return {"contents": [{"uri": uri, "mimeType": "text/markdown", "text": self.resources[uri].read_text()}]}
        if method == "tools/call":
            if set(params) - {"name", "arguments", "_meta"}:
                raise ProtocolError(-32602, "Unsupported tools/call parameter")
            name = params.get("name")
            if not isinstance(name, str) or name not in self.tools:
                raise ProtocolError(-32602, "Unknown tool")
            arguments = params.get("arguments", {})
            if not isinstance(arguments, dict):
                raise ProtocolError(-32602, "Tool arguments must be an object")
            try:
                validate(arguments, self.tools[name]["inputSchema"])
            except ValueError as error:
                # MCP Tools / Error Handling permits input validation failures as tool errors.
                return result({"error": str(error), "action": "Correct the arguments using this tool's input schema."}, True)
            try:
                if name in self.models:
                    value = self.client.generate(self.models[name], arguments)
                elif name == "replicate_production_doctor":
                    from production_health import check_health
                    value = check_health(self.client, arguments.get("model", next(iter(MODELS.values()))[0]), arguments.get("live", False))
                elif name == "replicate_upload_file":
                    value = self.client.upload(arguments["path"])
                elif name == "replicate_model_schema":
                    model = arguments["model"]
                    snapshot = schema_for(model)
                    value = {"model": model, "source": snapshot["source"], "researched_at": snapshot["fetched_at"], "version": snapshot["version"], "provider_input_schema": provider_input(model), "tool_input_schema": self.tools[next(name for name, current in self.models.items() if current == model)]["inputSchema"], "guide_uri": "replicate-video://guides/" + model.split("/")[1]}
                    if arguments.get("refresh"):
                        value["live"] = self.client.live_schema(model)
                else:
                    value = self.client.prediction(arguments["prediction_id"], cancel=name == "replicate_cancel_prediction")
                return result(value, (value.get("status") == "failed" and name != "replicate_cancel_prediction") or value.get("status") == "NEEDS_ATTENTION")
            except DomainError as error:
                value = {"error": str(error)}
                if "request_key" in arguments:
                    value["request_key"] = arguments["request_key"]
                return result(value, True)
            except Exception:
                # Never expose provider payloads, local paths, credentials or a traceback through MCP.
                return result({"error": "Internal tool failure. Mutating operations were not retried. If generating, retain request_key and inspect prediction history before another submission."}, True)
        raise ProtocolError(-32601, "Method not found")

    def handle(self, message):
        if not isinstance(message, dict) or message.get("jsonrpc") != "2.0" or not isinstance(message.get("method"), str) or ("id" in message and (isinstance(message["id"], bool) or not isinstance(message["id"], (str, int)))):
            return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
        notification = "id" not in message
        # Notifications cannot invoke paid tools or initialize a session without an acknowledgement.
        if notification:
            if message["method"] == "notifications/initialized":
                try:
                    self.dispatch(message["method"], message.get("params", {}))
                except ProtocolError:
                    pass
            return None
        try:
            value = self.dispatch(message["method"], message.get("params", {}))
            return {"jsonrpc": "2.0", "id": message["id"], "result": value}
        except ProtocolError as error:
            return {"jsonrpc": "2.0", "id": message["id"], "error": {"code": error.code, "message": error.message}}
        except Exception:
            return {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32603, "message": "Internal error"}}


def main():
    server = Server()
    output_lock = threading.Lock()
    inflight_lock = threading.Lock()
    inflight = {}
    slots = threading.BoundedSemaphore(4)

    def write(value):
        if value is not None:
            with output_lock:
                sys.stdout.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + "\n")
                sys.stdout.flush()

    def execute(message, cancelled):
        try:
            if not cancelled.is_set():
                value = server.handle(message)
                if not cancelled.is_set():
                    write(value)
        finally:
            with inflight_lock:
                inflight.pop(message.get("id"), None)
            slots.release()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        while True:
            line = sys.stdin.buffer.readline(MAX_MESSAGE + 1)
            if not line:
                break
            if len(line) > MAX_MESSAGE:
                write({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Message exceeds 1MB; send file paths, not base64 media"}})
                # Exit on oversized frames rather than misreading their remainder as requests.
                break
            try:
                message = json.loads(line, parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
            except (ValueError, UnicodeDecodeError, RecursionError):
                write({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}})
                continue
            if isinstance(message, dict) and message.get("method") == "notifications/cancelled" and "id" not in message:
                params = message.get("params")
                request_id = params.get("requestId") if isinstance(params, dict) else None
                if isinstance(request_id, (str, int)) and not isinstance(request_id, bool):
                    with inflight_lock:
                        event = inflight.get(request_id)
                        if event:
                            event.set()
                # Local cancellation suppresses delivery; use cancel_prediction for an accepted remote job.
                continue
            if isinstance(message, dict) and message.get("method") == "tools/call" and "id" in message and isinstance(message["id"], (str, int)) and not isinstance(message["id"], bool):
                with inflight_lock:
                    duplicate = message["id"] in inflight
                if duplicate or not slots.acquire(blocking=False):
                    write({"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32000, "message": "Duplicate active ID or server busy; retain generation request_key"}})
                    continue
                event = threading.Event()
                with inflight_lock:
                    inflight[message["id"]] = event
                pool.submit(execute, message, event)
            else:
                write(server.handle(message))


if __name__ == "__main__":
    main()
