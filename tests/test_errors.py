"""Conversion errors wrap into DataConverterError."""

from __future__ import annotations

import pytest

from lupaxa.data_converter import DataConverter, DataConverterError


def test_unsupported_data_type() -> None:
    with pytest.raises(DataConverterError, match="Unsupported data type"):
        DataConverter("{}", data_type="csv")


def test_dict_type_rejects_string() -> None:
    with pytest.raises(DataConverterError, match="dictionary"):
        DataConverter('{"id": 1}', data_type="dict")


def test_json_type_rejects_mapping() -> None:
    with pytest.raises(DataConverterError, match="JSON string"):
        DataConverter({"id": 1}, data_type="json")


def test_invalid_json_is_wrapped() -> None:
    with pytest.raises(DataConverterError, match="Invalid JSON") as excinfo:
        DataConverter("{not-json", data_type="json")
    assert excinfo.value.__cause__ is not None


def test_json_array_is_rejected() -> None:
    with pytest.raises(DataConverterError, match="mapping"):
        DataConverter("[1, 2, 3]", data_type="json")


def test_invalid_xml_is_wrapped() -> None:
    with pytest.raises(DataConverterError, match="Invalid XML") as excinfo:
        DataConverter("<root><unclosed>", data_type="xml")
    assert excinfo.value.__cause__ is not None


def test_invalid_yaml_is_wrapped() -> None:
    with pytest.raises(DataConverterError, match="Invalid YAML") as excinfo:
        DataConverter(":\n  - bad", data_type="yaml")
    assert excinfo.value.__cause__ is not None


def test_yaml_list_root_is_rejected() -> None:
    with pytest.raises(DataConverterError, match="mapping"):
        DataConverter("- one\n- two\n", data_type="yaml")


def test_empty_yaml_is_rejected() -> None:
    with pytest.raises(DataConverterError, match="mapping"):
        DataConverter("", data_type="yaml")


def test_invalid_xml_tag_from_dict_key() -> None:
    with pytest.raises(DataConverterError, match="XML"):
        DataConverter.dict_to_xml({"not a tag": 1})


def test_invalid_toml_is_wrapped() -> None:
    with pytest.raises(DataConverterError, match="Invalid TOML") as excinfo:
        DataConverter("[[[", data_type="toml")
    assert excinfo.value.__cause__ is not None


def test_invalid_json5_is_wrapped() -> None:
    with pytest.raises(DataConverterError, match="Invalid JSON5") as excinfo:
        DataConverter("{ name: }", data_type="json5")
    assert excinfo.value.__cause__ is not None


def test_json5_array_is_rejected() -> None:
    with pytest.raises(DataConverterError, match="mapping"):
        DataConverter("[1, 2, 3]", data_type="json5")


def test_default_error_message() -> None:
    error = DataConverterError()
    assert str(error) == "Data conversion error."
