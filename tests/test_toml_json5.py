"""TOML and JSON5 load through a dict, then dump to any format."""

from __future__ import annotations

import json

import yaml

from lupaxa.data_converter import DataConverter

JSON5_DOC = """
{
  // toolbox project
  name: "Lupaxa",
  active: true,
  count: 3,
}
"""

TOML_DOC = """
name = "Lupaxa"
active = true
count = 3
"""

EXPECTED = {"name": "Lupaxa", "active": True, "count": 3}


def test_load_json5_to_dict() -> None:
    converter = DataConverter(JSON5_DOC, data_type="json5")
    assert converter.data == EXPECTED
    assert converter.data_type == "json5"


def test_load_toml_to_dict() -> None:
    converter = DataConverter(TOML_DOC, data_type="toml")
    assert converter.data == EXPECTED
    assert converter.data_type == "toml"


def test_json5_to_every_text_format() -> None:
    converter = DataConverter(JSON5_DOC, data_type="json5")
    assert json.loads(converter.to_json()) == EXPECTED
    assert yaml.safe_load(converter.to_yaml()) == EXPECTED
    assert "<name>Lupaxa</name>" in converter.to_xml()
    assert DataConverter(converter.to_toml(), data_type="toml").data == EXPECTED
    assert DataConverter(converter.to_json5(), data_type="json5").data == EXPECTED


def test_toml_to_every_text_format() -> None:
    converter = DataConverter(TOML_DOC, data_type="toml")
    assert json.loads(converter.to_json()) == EXPECTED
    assert yaml.safe_load(converter.to_yaml()) == EXPECTED
    assert "<count>3</count>" in converter.to_xml()
    assert DataConverter(converter.to_json5(), data_type="json5").data == EXPECTED
    assert DataConverter(converter.to_toml(), data_type="toml").data == EXPECTED


def test_dict_to_toml_and_json5() -> None:
    converter = DataConverter(EXPECTED, data_type="dict")
    assert DataConverter.toml_to_dict(converter.to_toml()) == EXPECTED
    assert DataConverter.json5_to_dict(converter.to_json5()) == EXPECTED


def test_json5_type_is_case_insensitive() -> None:
    converter = DataConverter("{ id: 1 }", data_type="JSON5")
    assert converter.data == {"id": 1}
