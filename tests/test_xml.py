"""XML encode and decode details."""

from __future__ import annotations

import json

from lupaxa.data_converter import DataConverter


def test_list_values_become_repeated_elements() -> None:
    compact = "".join(DataConverter.dict_to_xml({"formats": ["json", "xml"]}).split())
    assert compact.count("<formats>") == 2
    assert "<formats>json</formats>" in compact
    assert "<formats>xml</formats>" in compact


def test_nested_dict() -> None:
    xml = DataConverter.dict_to_xml({"user": {"name": "Ann"}})
    assert "<user>" in xml
    assert "<name>Ann</name>" in xml


def test_attributes_round_trip() -> None:
    xml = '<person id="7"><name>Ann</name></person>'
    converter = DataConverter(xml, data_type="xml")
    assert converter.data == {"@id": "7", "name": "Ann"}
    out = converter.to_xml()
    assert 'id="7"' in out
    assert "<name>Ann</name>" in out


def test_duplicate_child_tags_become_list() -> None:
    xml = "<root><item>a</item><item>b</item></root>"
    assert DataConverter(xml, data_type="xml").data == {"item": ["a", "b"]}


def test_xml_to_json_matches_payload() -> None:
    assert json.loads(DataConverter.xml_to_json("<root><id>1</id></root>")) == {"id": "1"}
