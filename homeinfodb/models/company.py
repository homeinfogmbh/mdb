"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Company']

from .abc import CRMModel
from .customer import Customer
from peewee import TextField, ForeignKeyField

class Company(CRMModel):
    """
    A company
    """
    customer = ForeignKeyField(Customer, related_name='companies')
    name = TextField()  # A representative name
    annotation = TextField()  # A type like 'bank' or 'realtor', etc.