"""Optional loopback-only intent router. A deterministic request bounds its authority."""

from dataclasses import asdict
import http.client
import json
import re
import time

from jsonschema import Draft202012Validator, ValidationError

from compass.questions import Request, SUPPORTED_INTENTS, parse_question

INTENT_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["tool", "month", "category", "limit"],
    "properties": {
        "tool": {"type": "string", "enum": list(SUPPORTED_INTENTS)},
        "month": {"type": "string", "pattern": r"^[0-9]{4}-(0[1-9]|1[0-2])$"},
        "category": {"type": ["string", "null"], "minLength": 1, "maxLength": 80},
        "limit": {"type": "integer", "minimum": 1, "maximum": 20},
    },
}
VALIDATOR = Draft202012Validator(INTENT_SCHEMA)
TIMEOUT_SECONDS = 4.0
MAX_RESPONSE_BYTES = 65536


def _post(path: str, payload: dict, deadline: float) -> dict:
    # http.client uses no environment proxies and does not follow redirects.
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("Local router timed out.")
    connection = http.client.HTTPConnection("127.0.0.1", 11434, timeout=remaining)
    try:
        connection.request("POST", path, json.dumps(payload), {"Content-Type": "application/json"})
        transport_socket = connection.sock
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError("Local router unavailable.")
        body = bytearray()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Local router timed out.")
            # read1 bounds each blocking read; recompute the total deadline each time.
            if transport_socket is not None:
                transport_socket.settimeout(remaining)
            chunk = response.read1(min(4096, MAX_RESPONSE_BYTES + 1 - len(body)))
            body.extend(chunk)
            if len(body) > MAX_RESPONSE_BYTES:
                raise ValueError("Local router response too large.")
            if not chunk:
                break
        result = json.loads(body)
        if not isinstance(result, dict):
            raise ValueError("Expected a response object.")
        return result
    finally:
        connection.close()


def route(question: str, transactions, selected_month: str, *, model: str = "",
          enabled: bool = False, local_only_confirmed: bool = False) -> tuple[Request, str]:
    """Unsupported/ambiguous input is clarified before any model request.

    Model routing is advisory: it must preserve the full independently parsed
    request. No transaction values or source descriptions are sent to a model.
    """
    expected = parse_question(question, transactions, selected_month)
    if not enabled:
        return expected, "Deterministic routing"
    if (not local_only_confirmed or not re.fullmatch(r"[A-Za-z0-9_.:/-]{1,120}", model)
            or "cloud" in model.casefold()):
        return expected, "Deterministic fallback: configure an installed local model and disable Ollama cloud."
    try:
        deadline = time.monotonic() + TIMEOUT_SECONDS
        details = _post("/api/show", {"model": model}, deadline)
        if (details.get("remote_host") or details.get("remote_model")
                or details.get("details", {}).get("format") != "gguf"):
            raise ValueError("Local model metadata required.")
        response = _post("/api/chat", {
            "model": model, "stream": False, "format": INTENT_SCHEMA,
            "options": {"temperature": 0, "num_predict": 160, "num_ctx": 2048},
            "messages": [
                {"role": "system", "content": "Route this financial question to the provided JSON schema. Do not calculate money. Preserve the validated month, category and count. Return only JSON."},
                {"role": "user", "content": json.dumps({"question": question, "validated_request": asdict(expected)})},
            ],
        }, deadline)
        if response.get("done") is not True:
            raise ValueError("Incomplete model response.")
        candidate = json.loads(response["message"]["content"])
        VALIDATOR.validate(candidate)
        if type(candidate["limit"]) is not int or candidate != asdict(expected):
            raise ValueError("Model changed the question's filters or intent.")
        return Request(**candidate), "Local Ollama routing (validated against deterministic interpretation)"
    except (OSError, http.client.HTTPException, ValueError, TypeError, KeyError, AttributeError, ValidationError, RecursionError):
        return expected, "Deterministic fallback: local router unavailable or its response failed validation."
