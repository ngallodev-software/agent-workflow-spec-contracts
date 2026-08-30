import json

import pytest

from specgen_contracts import descriptor, negotiate, normalize, validate
from specgen_contracts.bundle import SCHEMA_FILES, schema_digest
from specgen_contracts.migration import migrate


def test_all_frozen_schema_digests_match_baseline():
    baseline = json.load(open("/lump/apps/specgen-aw/docs/research/SHARED_CONTRACT_FIXTURE_BASELINE_20260830.json"))
    expected = {item["schema_id"]: item["sha256"] for item in baseline["sources"][0]["files"]}
    assert {key: schema_digest(key) for key in SCHEMA_FILES} == expected


def test_normalization_and_descriptor_are_deterministic():
    value = {"b": [2, {"z": 1, "a": 0}], "a": "é"}
    assert normalize(value) == {"a": "é", "b": [2, {"a": 0, "z": 1}]}
    document = {"schema": "agent-workflow/source-baseline/v1", "generated_at": "now", "components": {}}
    assert descriptor("agent-workflow/source-baseline/v1", document)["bundle_version"] == "0.1.0"


def test_invalid_negotiation_and_migration_fail_closed():
    with pytest.raises(ValueError):
        negotiate(bundle_version="9.0.0", schema_id="agent-workflow/source-baseline/v1", schema_digest_value="x")
    with pytest.raises(ValueError):
        migrate({}, schema_id="agent-workflow/source-baseline/v1", from_version="9.0.0")


def test_invalid_document_has_diagnostic():
    errors = validate("agent-workflow/source-baseline/v1", {})
    assert errors and "message" in errors[0]
