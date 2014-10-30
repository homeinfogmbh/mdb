"""
Address related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Address']

from .abc import CRMModel
from homeinfodb.models.geo import Country
from peewee import CharField, ForeignKeyField    

class Address(CRMModel):
    """
    Address data
    """
    street = CharField(64, null=True)
    """The street's name"""
    house_number = CharField(8, null=True)
    """The house number"""
    zip = CharField(32, null=True)
    """The zip code"""
    po_box = CharField(32, null=True)
    """The po box number"""
    city = CharField(64)
    """The name of the respective city"""
    country = ForeignKeyField(Country, db_column='country', null=True)
    """The country of the address"""