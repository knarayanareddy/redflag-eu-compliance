import json
from pathlib import Path

import jsonschema
import pytest
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "core-schemas.json"


def test_core_schema_is_valid_json_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)


def test_citation_contract_accepts_valid_and_rejects_invalid() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    citation_schema = {
        "$schema": schema["$schema"],
        "$defs": schema["$defs"],
        "$ref": "#/$defs/Citation",
    }
    validator = Draft202012Validator(citation_schema)
    valid_citation = {
        "id": "cit_test",
        "kind": "regulation",
        "locator": "Regulation (EU) 2023/988",
        "retrieved_at": "2026-10-26T12:00:00Z",
        "trust": "primary",
    }
    validator.validate(valid_citation)

    invalid_citation = {**valid_citation, "id": "bad-id", "trust": "unknown"}
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(invalid_citation)
