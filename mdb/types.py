"""Common type hints."""

from typing import NamedTuple


__all__ = ['LongAddress', 'ShortAddress']


class LongAddress(NamedTuple):
    """A long address."""

    street: str
    house_number: str
    zip_code: str
    city: str


class ShortAddress(NamedTuple):
    """A short address."""

    street: str
    house_number: str
    zip_code: str
