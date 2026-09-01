import json
from copy import deepcopy
from pathlib import Path

import pytest

from specgen_contracts import descriptor, negotiate, normalize, validate
from specgen_contracts.bundle import SCHEMA_FILES, schema_digest
from specgen_contracts.migration import migrate


def test_all_frozen_schema_digests_match_baseline():
    baseline = json.load(open(Path(__file__).parent / "fixtures" / "baseline.json"))
    expected = {item["schema_id"]: item["sha256"] for item in baseline["sources"][0]["files"]}
    actual = {key: schema_digest(key) for key in SCHEMA_FILES}
    assert {key: actual[key] for key in expected} == expected
    assert "agent-workflow/prompt-pack/v2" in actual


def test_normalization_and_descriptor_are_deterministic():
    value = {"b": [2, {"z": 1, "a": 0}], "a": "é"}
    assert normalize(value) == {"a": "é", "b": [2, {"a": 0, "z": 1}]}
    document = {"schema": "agent-workflow/source-baseline/v1", "generated_at": "now", "components": {}}
    assert descriptor("agent-workflow/source-baseline/v1", document)["bundle_version"] == "0.2.0"


def test_invalid_negotiation_and_migration_fail_closed():
    with pytest.raises(ValueError):
        negotiate(bundle_version="9.0.0", schema_id="agent-workflow/source-baseline/v1", schema_digest_value="x")
    with pytest.raises(ValueError):
        migrate({}, schema_id="agent-workflow/source-baseline/v1", from_version="9.0.0")


def test_invalid_document_has_diagnostic():
    errors = validate("agent-workflow/source-baseline/v1", {})
    assert errors and "message" in errors[0]


def test_prompt_pack_versions_negotiate_and_reject_substituted_provenance():
    v2 = {"schema": "agent-workflow/prompt-pack/v2", "pack_id": "p",
          "workflow": {"name": "agent-workflow", "minimum_version": "0.9.1"},
          "phases": [{"id": 1, "name": "phase", "directory": "phase", "tasks":
                      [{"id": "t", "tier": "primary", "agent_run_id": "r", "prompt": "do"}]}],
          "bundle_provenance": {"bundle_version": "0.2.0",
                                 "schema_id": "agent-workflow/prompt-pack/v2",
                                 "schema_digest": schema_digest("agent-workflow/prompt-pack/v2")}}
    assert not validate("agent-workflow/prompt-pack/v2", v2)
    assert negotiate(bundle_version="0.2.0", schema_id="agent-workflow/prompt-pack/v2",
                     schema_digest_value=v2["bundle_provenance"]["schema_digest"])["schema_id"].endswith("/v2")
    altered = deepcopy(v2)
    altered["bundle_provenance"]["bundle_version"] = "9.9.9"
    assert validate("agent-workflow/prompt-pack/v2", altered)
    altered = deepcopy(v2)
    altered["bundle_provenance"]["schema_digest"] = "0" * 64
    assert validate("agent-workflow/prompt-pack/v2", altered)


def test_prompt_pack_migration_copies_input_and_returns_descriptors():
    source = {"schema": "agent-workflow/prompt-pack/v1", "pack_id": "p",
              "workflow": {"name": "agent-workflow", "minimum_version": "0.9.1"},
              "phases": [{"id": 1, "name": "phase", "directory": "phase", "tasks":
                          [{"id": "t", "tier": "primary", "agent_run_id": "r", "prompt": "do"}]}]}
    sealed = deepcopy(source)
    result = migrate(source, schema_id="agent-workflow/prompt-pack/v1", from_version="0.1.0")
    assert source == sealed
    assert result["document"]["schema"] == "agent-workflow/prompt-pack/v2"
    assert result["document"]["bundle_provenance"] == {"bundle_version": "0.2.0",
        "schema_id": "agent-workflow/prompt-pack/v2",
        "schema_digest": schema_digest("agent-workflow/prompt-pack/v2")}
    assert result["source"]["schema_id"].endswith("/v1")
    assert result["target"]["schema_id"].endswith("/v2")


def test_unsupported_migration_is_actionable():
    with pytest.raises(ValueError, match="manual migration"):
        migrate({}, schema_id="agent-workflow/prompt-pack/v2", from_version="0.2.0")
