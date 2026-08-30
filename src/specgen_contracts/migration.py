from __future__ import annotations

from copy import deepcopy
from typing import Any

from .bundle import BUNDLE_VERSION, descriptor, schema_digest, validate


def migrate(document: Any, *, schema_id: str, from_version: str, to_version: str = BUNDLE_VERSION) -> dict[str, Any]:
    """Migrate the supported v1 prompt pack to v2 without changing its input."""
    source_schema = "agent-workflow/prompt-pack/v1"
    target_schema = "agent-workflow/prompt-pack/v2"
    if (schema_id, from_version, to_version) != (source_schema, "0.1.0", BUNDLE_VERSION):
        raise ValueError(f"unsupported migration from {schema_id}@{from_version} to {to_version}; manual migration required")
    if validate(source_schema, document):
        raise ValueError(f"cannot migrate invalid {source_schema} document")
    target = deepcopy(document)
    target["schema"] = target_schema
    target["bundle_provenance"] = {
        "bundle_version": BUNDLE_VERSION,
        "schema_id": target_schema,
        "schema_digest": schema_digest(target_schema),
    }
    if validate(target_schema, target):
        raise ValueError(f"migration produced invalid {target_schema} document")
    source_descriptor = descriptor(source_schema, document)
    target_descriptor = descriptor(target_schema, target)
    return {"document": target, "source": source_descriptor, "target": target_descriptor,
            "source_descriptor": source_descriptor, "target_descriptor": target_descriptor}
