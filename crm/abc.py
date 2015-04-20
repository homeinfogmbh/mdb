"""Abstract base classes for HOMEINFO's ORM database"""

from peewee import Model, MySQLDatabase
from .config import db

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['CRMModel']


class CRMModel(Model):
    """Generic HOMEINFO-DB Model"""

    class Meta:
        database = MySQLDatabase(db.get('db'),
                                 host=db.get('host'),
                                 user=db.get('user'),
                                 passwd=db.get('passwd'),
                                 threadlocals=True)
        schema = database.database
