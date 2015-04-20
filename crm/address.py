"""Address related models for HOMEINFO's CRM"""

from peewee import CharField, ForeignKeyField, DoesNotExist, create
from .abc import CRMModel
from .geo import State

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Address']


@create
class Address(CRMModel):
    """Address data"""

    street = CharField(64, null=True)
    """The street's name"""
    house_number = CharField(8, null=True)
    """The house number"""
    zip_code = CharField(32, null=True)
    """The zip code"""
    po_box = CharField(32, null=True)
    """The po box number"""
    city = CharField(64)
    """The name of the respective city"""
    state = ForeignKeyField(State, db_column='state', null=True)
    """The country of the address"""

    def __str__(self):
        """Converts the Address to a string"""
        result = ''
        if self.po_box:
            result += ''.join(['Postfach', ' ', self.po_box, '\n'])
        elif self.street:
            if self.house_number:
                result += ''.join([self.street, ' ', self.house_number, '\n'])
            else:
                result += ''.join([self.street, '\n'])
        if self.zip_code:
            result += ''.join([self.zip_code, ' ', self.city, '\n'])
        state = self.state
        if state:
            country_name = str(self.state.country)
            if country_name not in ['Deutschland', 'Germany', 'DE']:
                result += ''.join([country_name, '\n'])
        return result

    @classmethod
    def add(cls, city, street=None, house_number=None,
            zip_code=None, po_box=None, state=None):
        """Adds an address record to the database"""
        try:
            addr = Address.iget(  # @UndefinedVariable
                (Address.city == city) &
                (Address.street == street) &
                (Address.house_number == house_number) &
                (Address.zip_code == zip_code) &
                (Address.po_box == po_box) &
                (Address.state == state))
        except DoesNotExist:
            addr = Address()
            addr.city = city
            addr.street = street
            addr.house_number = house_number
            addr.zip_code = zip_code
            addr.po_box = po_box
            addr.state = state
            addr.isave()
        finally:
            return addr
