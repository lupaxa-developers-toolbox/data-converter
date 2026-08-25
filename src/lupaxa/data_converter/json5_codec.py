"""JSON5 load and dump helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import json5

from .exceptions import DataConverterError


def dumps(data: Mapping[str, Any]) -> str:
    try:
        return json5.dumps(dict(data), ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise DataConverterError("Cannot encode value as JSON5.") from exc


def loads(text: str) -> dict[str, Any]:
    try:
        parsed = json5.loads(text)
    except (ValueError, TypeError) as exc:
        raise DataConverterError("Invalid JSON5.") from exc
    if not isinstance(parsed, dict):
        raise DataConverterError("JSON5 document must be a mapping.")
    return parsed
