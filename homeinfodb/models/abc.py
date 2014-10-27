"""
Abstract base classes for HOMEINFO's ORM database
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['CRMModel']

from peewee import Model
from ..config import database, DB

class CRMModel(Model):
    """
    Generic HOMEINFO-DB Model
    """
    class Meta:
        database = database
        schema = DB