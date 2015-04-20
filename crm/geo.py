"""Geography related models for HOMEINFO's CRM"""

from peewee import CharField, ForeignKeyField, create
from .abc import CRMModel

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Country', 'State']


@create
class Country(CRMModel):
    """Country data"""

    _iso = CharField(2, db_column='iso')
    """An, *exactly* two characters long ISO 3166-2 country code
    example: 'DE'"""
    name = CharField(64)
    """The complete country's name"""
    original_name = CharField(64, null=True)
    """The countrie's name in its original language"""

    def __str__(self):
        """Converts the country to a string"""
        return self.name

    @property
    def iso(self):
        """Returns the ISO code"""
        return self._iso

    @iso.setter
    def iso(self, iso):
        """Sets the ISO code"""
        if len(iso) is 2:
            self._iso = iso
        else:
            raise ValueError('ISO code must be exactly two characters long')


@create
class State(CRMModel):
    """Country data"""

    country = ForeignKeyField(Country, db_column='country',
                              related_name='states')
    """The country this state belongs to"""
    _iso = CharField(2, db_column='iso')
    """An *exactly* two characters long ISO 3166-2 state code
    examples: 'NI' or 'NW'"""
    name = CharField(64)
    """The complete state's name"""

    @property
    def iso(self):
        """Returns the ISO code"""
        return self._iso

    @iso.setter
    def iso(self, iso):
        """Sets the ISO code"""
        if len(iso) is 2:
            self._iso = iso
        else:
            raise ValueError('ISO code must be exactly two characters long')

    @property
    def iso3166(self):
        """Returns the full ISO 3166-2 compliant code"""
        return '-'.join([self.country.iso, self.iso])
