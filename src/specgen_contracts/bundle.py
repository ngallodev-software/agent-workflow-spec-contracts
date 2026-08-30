from __future__ import annotations

import hashlib
import json
from importlib.resources import files
from typing import Any

BUNDLE_VERSION = "0.1.0"
SUPPORTED_VERSIONS = (BUNDLE_VERSION,)
SCHEMA_FILES = {
    "agent-workflow/prompt-pack/v1": "pack.schema.json",
    "agent-workflow/evaluation-plan/v1": "evaluation-plan.schema.json",
    "agent-workflow/source-baseline/v1": "source-baseline.schema.json",
    "agent-workflow/agent-role/v1": "agent-role-v1.schema.json",
    "agent-workflow/task-result/v1": "task-result.schema.json",
}


def normalize(value: Any) -> Any:
    """Return JSON-compatible data with recursively sorted object keys."""
    if isinstance(value, dict):
        return {key: normalize(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(normalize(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()


def schema(schema_id: str) -> dict[str, Any]:
    try:
        name = SCHEMA_FILES[schema_id]
    except KeyError as exc:
        raise ValueError(f"unsupported schema ID: {schema_id}") from exc
    return json.loads(files("specgen_contracts").joinpath("schemas", name).read_text())


def schema_digest(schema_id: str) -> str:
    name = SCHEMA_FILES.get(schema_id)
    if name is None:
        raise ValueError(f"unsupported schema ID: {schema_id}")
    return hashlib.sha256(files("specgen_contracts").joinpath("schemas", name).read_bytes()).hexdigest()


def validate(schema_id: str, document: Any) -> list[dict[str, Any]]:
    """Return actionable diagnostics; an empty list means valid."""
    from jsonschema import Draft202012Validator
    validator = Draft202012Validator(schema(schema_id))
    return [{"path": list(error.absolute_path), "message": error.message, "validator": error.validator}
            for error in sorted(validator.iter_errors(document), key=lambda error: list(error.absolute_path))]


def descriptor(schema_id: str, document: Any) -> dict[str, Any]:
    if validate(schema_id, document):
        raise ValueError(f"invalid {schema_id} document")
    return {"bundle_version": BUNDLE_VERSION, "schema_id": schema_id,
            "schema_digest": schema_digest(schema_id),
            "document_digest": hashlib.sha256(canonical_bytes(document)).hexdigest()}


def negotiate(*, bundle_version: str, schema_id: str, schema_digest_value: str,
              features: set[str] | frozenset[str] = frozenset()) -> dict[str, Any]:
    if bundle_version not in SUPPORTED_VERSIONS:
        raise ValueError(f"unsupported bundle version: {bundle_version}")
    expected = schema_digest(schema_id)
    if schema_digest_value != expected:
        raise ValueError(f"schema digest mismatch for {schema_id}")
    return {"bundle_version": bundle_version, "schema_id": schema_id,
            "schema_digest": expected, "features": sorted(features)}
