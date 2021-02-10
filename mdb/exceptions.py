"""Common exceptions."""

from peewee import Model


__all__ = ['AlreadyExists']


class AlreadyExists(Exception):
    """Indicates that a certain record already exists."""

    def __init__(self, record: Model, **keys):
        super().__init__(record, keys)
        self.record = record
        self.keys = keys

    def __str__(self):
        record_name = type(self.record).__name__

        if self.keys:
            return f'{record_name} already exists for {self.keys}.'

        return f'{record_name} already exists.'
