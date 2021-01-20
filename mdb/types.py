"""Common type hints."""

from typing import Tuple


__all__ = ['LongAddress', 'ShortAddress']


LongAddress = Tuple[str, str, str, str]
ShortAddress = Tuple[str, str, str]
