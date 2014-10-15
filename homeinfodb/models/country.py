"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Country']

from .abc import CRMModel
from peewee import CharField, TextField

class Country(CRMModel):
    """
    Country data
    """
    iso = CharField(3)
    name = TextField()