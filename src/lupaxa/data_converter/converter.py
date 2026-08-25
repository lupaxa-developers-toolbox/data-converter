"""Public converter facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal

from . import json5_codec, json_codec, toml_codec, xml_codec, yaml_codec
from .exceptions import DataConverterError

DataType = Literal["json", "json5", "xml", "yaml", "toml", "dict"]
_SUPPORTED_TYPES = frozenset({"json", "json5", "xml", "yaml", "toml", "dict"})
_TEXT_LOADERS = {
    "json": json_codec.loads,
    "json5": json5_codec.loads,
    "yaml": yaml_codec.loads,
    "toml": toml_codec.loads,
}


class DataConverter:
    """Load any supported format to a dict, then dump to any supported format."""

    def __init__(self, data: str | Mapping[str, Any], data_type: str = "json") -> None:
        self._data_type = _normalize_type(data_type)
        if self._data_type == "xml":
            self._root_tag, self._data = xml_codec.loads(_as_text(data, "XML"))
        else:
            self._root_tag = "root"
            self._data = _load(data, self._data_type)

    @property
    def data(self) -> dict[str, Any]:
        """The loaded mapping."""
        return self._data

    @property
    def data_type(self) -> str:
        """Normalized source type."""
        return self._data_type

    @property
    def root_tag(self) -> str:
        """XML root tag used when serializing to XML."""
        return self._root_tag

    def to_json(self) -> str:
        return json_codec.dumps(self._data)

    def to_yaml(self) -> str:
        return yaml_codec.dumps(self._data)

    def to_xml(self, root_tag: str | None = None) -> str:
        return xml_codec.dumps(self._data, root_tag=root_tag or self._root_tag)

    def to_toml(self) -> str:
        return toml_codec.dumps(self._data)

    def to_json5(self) -> str:
        return json5_codec.dumps(self._data)

    @staticmethod
    def dict_to_xml(data: Mapping[str, Any], root_tag: str = "root") -> str:
        _require_mapping(data, "dictionary")
        return xml_codec.dumps(data, root_tag=root_tag)

    @staticmethod
    def json_to_xml(json_data: Mapping[str, Any], root_tag: str = "root") -> str:
        _require_mapping(json_data, "JSON object")
        return xml_codec.dumps(json_data, root_tag=root_tag)

    @staticmethod
    def xml_to_json(xml_data: str) -> str:
        _root_tag, payload = xml_codec.loads(_as_text(xml_data, "XML"))
        return json_codec.dumps(payload)

    @staticmethod
    def yaml_to_dict(yaml_data: str) -> dict[str, Any]:
        return yaml_codec.loads(_as_text(yaml_data, "YAML"))

    @staticmethod
    def toml_to_dict(toml_data: str) -> dict[str, Any]:
        return toml_codec.loads(_as_text(toml_data, "TOML"))

    @staticmethod
    def json5_to_dict(json5_data: str) -> dict[str, Any]:
        return json5_codec.loads(_as_text(json5_data, "JSON5"))


def _normalize_type(data_type: str) -> DataType:
    normalized = data_type.strip().lower()
    if normalized not in _SUPPORTED_TYPES:
        raise DataConverterError(
            f"Unsupported data type: {data_type!r}. Use json, json5, xml, yaml, toml, or dict."
        )
    return normalized  # type: ignore[return-value]


def _load(data: str | Mapping[str, Any], data_type: DataType) -> dict[str, Any]:
    if data_type == "dict":
        if not isinstance(data, Mapping):
            raise DataConverterError("A dictionary mapping is required.")
        return dict(data)
    loader = _TEXT_LOADERS.get(data_type)
    if loader is None:
        raise DataConverterError(f"Unsupported data type: {data_type!r}.")
    return loader(_as_text(data, data_type.upper()))


def _as_text(data: object, label: str) -> str:
    if isinstance(data, bytes):
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DataConverterError(f"Invalid {label} string.") from exc
    if not isinstance(data, str):
        raise DataConverterError(f"{label} string required.")
    return data


def _require_mapping(data: object, label: str) -> None:
    if not isinstance(data, Mapping):
        raise DataConverterError(f"A {label} mapping is required.")
