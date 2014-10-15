"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Department']

from .abc import CRMModel
from .company import Company
from peewee import ForeignKeyField, TextField

class Department(CRMModel):
    """
    Departments of companies
    """
    company = ForeignKeyField(Company, related_name='departments')
    """The company, this department belongs to"""
    name = TextField()
    """A representative name"""
    type = TextField()
    """A type like 'IT', 'customer service', etc."""