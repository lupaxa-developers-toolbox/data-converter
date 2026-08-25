"""DataConverter load and convert behaviour."""

from __future__ import annotations

import json

import pytest
import yaml

from lupaxa.data_converter import DataConverter

PAYLOAD = {"name": "Lupaxa", "active": True, "count": 3}


def test_from_dict_to_json() -> None:
    converter = DataConverter(PAYLOAD, data_type="dict")
    assert json.loads(converter.to_json()) == PAYLOAD


def test_from_dict_to_yaml() -> None:
    converter = DataConverter(PAYLOAD, data_type="dict")
    assert yaml.safe_load(converter.to_yaml()) == PAYLOAD


def test_from_dict_to_xml_wraps_root() -> None:
    converter = DataConverter({"id": 1}, data_type="dict")
    xml = converter.to_xml()
    assert "<root>" in xml
    assert "<id>1</id>" in xml


def test_from_json_to_json_is_identity_document() -> None:
    converter = DataConverter('{"id": 1, "ok": true}', data_type="json")
    assert json.loads(converter.to_json()) == {"id": 1, "ok": True}


def test_from_json_to_xml_and_yaml() -> None:
    converter = DataConverter('{"id": 1}', data_type="json")
    assert "<id>1</id>" in converter.to_xml()
    assert yaml.safe_load(converter.to_yaml()) == {"id": 1}


def test_from_yaml_to_dict_methods() -> None:
    converter = DataConverter("name: Lupaxa\nactive: true\n", data_type="yaml")
    assert json.loads(converter.to_json()) == {"name": "Lupaxa", "active": True}
    assert "<name>Lupaxa</name>" in converter.to_xml()
    assert yaml.safe_load(converter.to_yaml()) == {"name": "Lupaxa", "active": True}


def test_from_xml_to_json_uses_element_payload() -> None:
    converter = DataConverter("<root><id>1</id></root>", data_type="xml")
    assert json.loads(converter.to_json()) == {"id": "1"}


def test_from_xml_to_xml_keeps_root() -> None:
    converter = DataConverter("<person><name>Ann</name></person>", data_type="xml")
    xml = converter.to_xml()
    assert "<person>" in xml
    assert "<name>Ann</name>" in xml
    assert xml.count("<person>") == 1


def test_to_xml_root_tag_override() -> None:
    converter = DataConverter({"id": 1}, data_type="dict")
    assert "<item>" in converter.to_xml(root_tag="item")
    assert "<id>1</id>" in converter.to_xml(root_tag="item")


def test_data_type_is_case_insensitive() -> None:
    converter = DataConverter('{"id": 1}', data_type="JSON")
    assert json.loads(converter.to_json()) == {"id": 1}


def test_loaded_mapping_is_exposed() -> None:
    converter = DataConverter(PAYLOAD, data_type="dict")
    assert converter.data == PAYLOAD
    assert converter.data_type == "dict"


def test_xml_root_tag_is_exposed() -> None:
    converter = DataConverter("<person><name>Ann</name></person>", data_type="xml")
    assert converter.root_tag == "person"


def test_classmethod_helpers() -> None:
    xml = DataConverter.dict_to_xml({"id": 1}, root_tag="item")
    assert "<item>" in xml
    assert DataConverter.json_to_xml({"id": 1}).count("<id>1</id>") == 1
    assert json.loads(DataConverter.xml_to_json("<root><id>1</id></root>")) == {"id": "1"}
    assert DataConverter.yaml_to_dict("id: 1\n") == {"id": 1}


@pytest.mark.parametrize("data_type", ["json", "xml", "yaml", "toml", "json5", "dict"])
def test_supported_data_types_construct(data_type: str) -> None:
    if data_type == "dict":
        DataConverter({"a": 1}, data_type=data_type)
    elif data_type == "xml":
        DataConverter("<root><a>1</a></root>", data_type=data_type)
    elif data_type == "yaml":
        DataConverter("a: 1\n", data_type=data_type)
    elif data_type == "toml":
        DataConverter("a = 1\n", data_type=data_type)
    elif data_type == "json5":
        DataConverter("{ a: 1 }", data_type=data_type)
    else:
        DataConverter('{"a": 1}', data_type=data_type)
