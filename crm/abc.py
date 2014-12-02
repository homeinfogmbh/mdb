"""
Abstract base classes for HOMEINFO's ORM database
"""
from ..config import crm
from peewee import Model, MySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['CRMModel']


class CRMModel(Model):
    """
    Generic HOMEINFO-DB Model
    """
    class Meta:
        database = MySQLDatabase(crm.get('db'),
                                 host=crm.get('host'),
                                 user=crm.get('user'),
                                 passwd=crm.get('passwd'))
        database.get_conn().ping(True)
        schema = crm.get('db')
