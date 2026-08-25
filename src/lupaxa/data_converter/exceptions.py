"""Errors raised by ``lupaxa.data_converter``."""

from __future__ import annotations


class DataConverterError(Exception):
    """Raised when a conversion cannot be completed."""

    def __init__(self, message: str = "Data conversion error.") -> None:
        super().__init__(message)
