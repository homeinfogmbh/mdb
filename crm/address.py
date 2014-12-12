"""
Address related models for HOMEINFO's CRM
"""
from .abc import CRMModel
from .geo import Country
from peewee import CharField, ForeignKeyField

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Address']


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

    def __str__(self):
        """Converts the Address to a string"""
        result = ''
        if self.po_box:
            result += ' '.join(['Postfach', self.po_box, '\n'])
        elif self.street:
            if self.house_number:
                result += ''.join([' '.join([self.street,
                                             self.house_number]),
                                   '\n'])
            else:
                result += ''.join([self.street, '\n'])
        if self.zip:
            result += ''.join([' '.join([self.zip,
                                         self.city]),
                               '\n'])
        if self.country:
            result += ''.join([str(self.country), '\n'])
        return result
