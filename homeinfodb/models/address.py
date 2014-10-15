"""
Address related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Address']

from .abc import CRMModel
from homeinfodb.models.geo import Country
from peewee import CharField, TextField, IntegerField, ForeignKeyField    

class Address(CRMModel):
    """
    Address data
    """
    street = TextField(null=True)
    house_number = CharField(45, null=True)
    zip = IntegerField(11, null=True)       # ZIP code
    po_box = TextField(null=True)           # Post box
    city = TextField()
    country = ForeignKeyField(Country)