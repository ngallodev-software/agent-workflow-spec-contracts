import json
from importlib.resources import files

from specgen_contracts import validate


def test_conformance_fixture_outcomes():
    fixture = json.loads(files("specgen_contracts").joinpath("fixtures", "conformance.json").read_text())
    for case in fixture["cases"]:
        assert bool(validate(case["schema_id"], case["document"])) is (not case["valid"]), case["id"]
