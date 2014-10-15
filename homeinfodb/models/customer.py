"""
Customer related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Customer']

from .abc import CRMModel
from .company import Company
from peewee import CharField, ForeignKeyField, IntegerField, TextField

class Customer(CRMModel):
    """
    CRM's customer(s)
    """
    cid = CharField(7)
    """A unique customer ID"""
    company = ForeignKeyField(Company, related_name='customers')
    """A related company"""
    # TODO: Add other stuff like merchants etc.
    
    
class CustomerLegacy(CRMModel):
    """
    Legacy model for existing customer entries
    """
    cid = IntegerField(11)
    name = TextField()