"""Abstract base classes for HOMEINFO's CRM database"""

from peewee import Model, MySQLDatabase, PrimaryKeyField
from .config import db

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['CRMModel']


class CRMModel(Model):
    """Generic HOMEINFO CRM Model"""

    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('host'),
                                 user=db.get('user'),
                                 passwd=db.get('passwd'),
                                 threadlocals=True)
        schema = database.database

    id = PrimaryKeyField()
    """The table's primary key"""
