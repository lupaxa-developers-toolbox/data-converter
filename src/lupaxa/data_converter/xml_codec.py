"""XML load and dump helpers."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from typing import Any

from defusedxml.ElementTree import ParseError, fromstring
from defusedxml.minidom import parseString

from .exceptions import DataConverterError

_XML_NAME = re.compile(r"^[_A-Za-z][-._A-Za-z0-9]*$")


def dumps(data: Mapping[str, Any], root_tag: str = "root") -> str:
    root = ET.Element(_require_name(root_tag))
    _append_mapping(data, root)
    try:
        raw = ET.tostring(root, encoding="unicode")
        return parseString(raw).toprettyxml()
    except DataConverterError:
        raise
    except Exception as exc:
        raise DataConverterError("Cannot encode value as XML.") from exc


def loads(text: str) -> tuple[str, dict[str, Any]]:
    try:
        root = fromstring(text)
    except ParseError as exc:
        raise DataConverterError("Invalid XML.") from exc
    except Exception as exc:
        raise DataConverterError("Invalid XML.") from exc
    return root.tag, _element_payload(root)


def _require_name(name: str) -> str:
    if not name or not _XML_NAME.match(name):
        raise DataConverterError(f"Invalid XML name: {name!r}.")
    return name


def _append_mapping(data: Mapping[str, Any], parent: ET.Element) -> None:
    for key, value in data.items():
        if key == "#text":
            parent.text = "" if value is None else str(value)
            continue
        if key.startswith("@"):
            parent.set(_require_name(key[1:]), "" if value is None else str(value))
            continue
        tag = _require_name(key)
        if isinstance(value, list):
            for item in value:
                child = ET.SubElement(parent, tag)
                _append_value(item, child)
            continue
        child = ET.SubElement(parent, tag)
        _append_value(value, child)


def _append_value(value: Any, parent: ET.Element) -> None:
    if isinstance(value, Mapping):
        _append_mapping(value, parent)
        return
    if isinstance(value, list):
        for item in value:
            child = ET.SubElement(parent, "item")
            _append_value(item, child)
        return
    if value is None:
        return
    parent.text = str(value)


def _element_payload(element: ET.Element) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for name, value in element.attrib.items():
        payload[f"@{name}"] = value

    for child in list(element):
        child_value = _child_value(child)
        if child.tag in payload:
            existing = payload[child.tag]
            if not isinstance(existing, list):
                payload[child.tag] = [existing]
            payload[child.tag].append(child_value)
        else:
            payload[child.tag] = child_value

    text = element.text.strip() if element.text and element.text.strip() else None
    if text:
        payload["#text"] = text
    return payload


def _child_value(element: ET.Element) -> Any:
    payload = _element_payload(element)
    if not element.attrib and not list(element):
        return payload.get("#text", "")
    return payload
