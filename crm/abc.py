"""
Abstract base classes for HOMEINFO's ORM database
"""
from .config import db
from homeinfo.db import HIModel
from peewee import MySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['CRMModel']


class CRMModel(HIModel):
    """Generic HOMEINFO-DB Model"""
    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('host'),
                                 user=db.get('user'),
                                 passwd=db.get('passwd'),
                                 threadlocals=True)
        schema = db.get('db')

    def __enter__(self):
        """Opens a connection explicitly"""
        self._meta.database.connect()
        return self

    def __exit__(self, tpe, value, tb):
        """Closes a connection if existent"""
        try:
            self._meta.database.close()
        except:
            pass
