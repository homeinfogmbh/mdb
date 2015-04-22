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

    def __repr__(self):
        """Converts the Address to a one-line string"""
        if self.po_box:
            return ' '.join([self.po_box, self.city])
        else:
            return ', '.join([' '.join([self.street, self.house_number]),
                              ' '.join([self.zip_code, self.city])])

    @classmethod
    def add(cls, city, po_box=None, addr=None, state=None):
        """Adds an address record to the database
        Usage:
            * Add address with either po_box or addr parameter
            * addr must be a tuple: (<street>, <house_number>, <zip_code>)
        """
        if po_box is None and addr is None:
            raise ValueError('Must specify either po_box or addr')
        elif po_box is not None and addr is not None:
            raise ValueError('Must specify either po_box or addr')
        elif addr is not None:
            street, house_number, zip_code = addr
            if state is None:
                try:
                    address = Address.get((Address.city == city) &
                                          (Address.street == street) &
                                          (Address.house_number
                                           == house_number) &
                                          (Address.zip_code == zip_code))
                except DoesNotExist:
                    address = Address()
                    address.city = city
                    address.street = street
                    address.house_number = house_number
                    address.zip_code = zip_code
                    address.save()
                return address
            else:
                try:
                    address = Address.get((Address.city == city) &
                                          (Address.street == street) &
                                          (Address.house_number
                                           == house_number) &
                                          (Address.zip_code == zip_code) &
                                          (Address.state == state))
                except DoesNotExist:
                    address = Address()
                    address.city = city
                    address.street = street
                    address.house_number = house_number
                    address.zip_code = zip_code
                    address.state = state
                    address.save()
                return address
        elif po_box is not None:
            if state is None:
                try:
                    address = Address.get(Address.po_box == po_box)
                except DoesNotExist:
                    address = Address()
                    address.po_box = po_box
                    address.save()
                return address
            else:
                try:
                    address = Address.get((Address.po_box == po_box) &
                                          (Address.state == state))
                except DoesNotExist:
                    address = Address()
                    address.po_box = po_box
                    address.state = state
                    address.save()
                return address
        else:
            raise ValueError('Must specify either po_box or addr')
