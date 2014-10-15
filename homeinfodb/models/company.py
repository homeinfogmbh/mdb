"""
Company related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Company']

from .abc import CRMModel
from .address import Address
from peewee import TextField, ForeignKeyField

class Company(CRMModel):
    """
    A company
    """
    name = TextField()
    """A representative name"""
    address = ForeignKeyField(Address, null=True)
    """The employee's address"""
    annotation = TextField()
    """Type like 'bank' or 'realtor', etc."""