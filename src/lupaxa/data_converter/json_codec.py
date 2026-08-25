"""JSON load and dump helpers."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from .exceptions import DataConverterError


def dumps(data: Mapping[str, Any]) -> str:
    try:
        return json.dumps(data, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise DataConverterError("Cannot encode value as JSON.") from exc


def loads(text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DataConverterError(f"Invalid JSON: {exc.msg}.") from exc
    if not isinstance(parsed, dict):
        raise DataConverterError("JSON document must be a mapping.")
    return parsed
