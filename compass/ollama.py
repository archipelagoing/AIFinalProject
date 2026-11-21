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
MAX_MODEL_ATTEMPTS = 2


class InvalidModelOutput(ValueError):
    """The model response is ambiguous, malformed, or outside its allowlist."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidModelOutput("Duplicate JSON field.")
        result[key] = value
    return result


def _reject_constant(value: str):
    raise InvalidModelOutput(f"Nonstandard JSON constant: {value}.")


def parse_model_output(content: str, expected: Request) -> Request:
    """Parse the structured intent and refuse anything unlike the safe request.

    This function has no access to transaction data or execution tools. A model
    response can only confirm the independently parsed request, never select a
    different tool, month, category, or limit.
    """
    if not isinstance(content, str):
        raise InvalidModelOutput("Model output is missing or too large.")
    try:
        if len(content.encode("utf-8")) > MAX_RESPONSE_BYTES:
            raise InvalidModelOutput("Model output is missing or too large.")
    except UnicodeError as error:
        raise InvalidModelOutput("Model output is not valid UTF-8 text.") from error
    try:
        candidate = json.loads(content, object_pairs_hook=_unique_object,
                               parse_constant=_reject_constant)
        VALIDATOR.validate(candidate)
    except (json.JSONDecodeError, UnicodeError, ValidationError, TypeError, RecursionError) as error:
        raise InvalidModelOutput("Model output did not match the intent schema.") from error
    if not isinstance(candidate, dict) or type(candidate.get("limit")) is not int:
        raise InvalidModelOutput("Model output did not match the intent schema.")
    if candidate != asdict(expected):
        raise InvalidModelOutput("Model changed the deterministic request.")
    return Request(**candidate)


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
        messages = [
            {"role": "system", "content": "Route this financial question to the provided JSON schema. Do not calculate money. Preserve the validated month, category and count. Return only JSON."},
            {"role": "user", "content": json.dumps({"question": question, "validated_request": asdict(expected)})},
        ]
        for attempt in range(MAX_MODEL_ATTEMPTS):
            if attempt:
                # Never echo untrusted malformed output back into a retry prompt.
                messages.append({"role": "system", "content": "The previous response failed validation. Return the validated_request object exactly, using only the required schema fields."})
            response = _post("/api/chat", {
                "model": model, "stream": False, "format": INTENT_SCHEMA,
                "options": {"temperature": 0, "num_predict": 160, "num_ctx": 2048},
                "messages": messages,
            }, deadline)
            if not isinstance(response, dict) or response.get("done") is not True:
                raise ValueError("Incomplete model response.")
            message = response.get("message")
            content = message.get("content") if isinstance(message, dict) else None
            try:
                request = parse_model_output(content, expected)
            except InvalidModelOutput:
                if attempt + 1 == MAX_MODEL_ATTEMPTS:
                    raise
                continue
            return request, "Local Ollama routing (validated against deterministic interpretation)"
        raise InvalidModelOutput("Model did not produce a valid intent.")
    except (OSError, http.client.HTTPException, ValueError, TypeError, KeyError, AttributeError, RecursionError):
        return expected, "Deterministic fallback: local router unavailable or its response failed validation."
