from __future__ import annotations

from typing import Any

from .bundle import BUNDLE_VERSION, descriptor


def migrate(document: Any, *, schema_id: str, from_version: str, to_version: str = BUNDLE_VERSION) -> dict[str, Any]:
    """Migrate only explicitly supported identities; never mutate the input."""
    if from_version != to_version or from_version != BUNDLE_VERSION:
        raise ValueError(f"no deterministic migration from {from_version} to {to_version}")
    return {"document": document, "provenance": {"migration": "identity", "from_version": from_version,
            "to_version": to_version, "source": descriptor(schema_id, document)}}
