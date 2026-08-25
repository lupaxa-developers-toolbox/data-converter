"""YAML load and dump helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import yaml
from yaml import YAMLError

from .exceptions import DataConverterError


def dumps(data: Mapping[str, Any]) -> str:
    try:
        return yaml.safe_dump(
            dict(data),
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    except YAMLError as exc:
        raise DataConverterError("Cannot encode value as YAML.") from exc


def loads(text: str) -> dict[str, Any]:
    try:
        parsed = yaml.safe_load(text)
    except YAMLError as exc:
        raise DataConverterError("Invalid YAML.") from exc
    if not isinstance(parsed, dict):
        raise DataConverterError("YAML document must be a mapping.")
    return parsed
