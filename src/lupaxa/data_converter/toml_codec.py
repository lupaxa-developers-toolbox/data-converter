"""TOML load and dump helpers."""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

import tomli_w

from .exceptions import DataConverterError

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def dumps(data: Mapping[str, Any]) -> str:
    try:
        return tomli_w.dumps(dict(data))
    except (TypeError, ValueError) as exc:
        raise DataConverterError("Cannot encode value as TOML.") from exc


def loads(text: str) -> dict[str, Any]:
    try:
        parsed = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise DataConverterError("Invalid TOML.") from exc
    if not isinstance(parsed, dict):
        raise DataConverterError("TOML document must be a mapping.")
    return parsed
