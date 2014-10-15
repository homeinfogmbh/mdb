"""
Geography related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Country', 'State']

from .abc import CRMModel
from peewee import CharField, TextField, ForeignKeyField

class Country(CRMModel):
    """
    Country data
    """
    iso = CharField(2)
    """An, *exactly* two characters long ISO 3166-2 country code
    example: 'DE'"""
    name = TextField()
    """The complete countrie's name"""
    original_name = TextField(null=True)
    """The countrie's name in its original language"""


class State(CRMModel):
    """
    Country data
    """
    country = ForeignKeyField(Country, related_name='states')
    """The country this state belongs to"""
    iso = CharField(2)
    """An *exactly* two characters long ISO 3166-2 state code
    examples: 'NI' or 'NW'"""
    name = TextField()
    """The complete countrie's name"""
    
    @property
    def iso3166(self):
        """Returns the full ISO 3166-2 compliant code"""
        return self.country.iso + '-' + self.iso