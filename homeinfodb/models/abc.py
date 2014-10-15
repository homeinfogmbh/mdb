"""
Database static configuration
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['CRMModel']

from peewee import Model
from ..config import deferred_db

class CRMModel(Model):
    """
    Generic HOMEINFO-DB Model
    """
    class Meta:
        database = deferred_db