"""Customer related models for HOMEINFO's CRM"""

from .abc import CRMModel
from .company import Company
from peewee import ForeignKeyField
from hashlib import sha256
from homeinfolib import create, connection

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Customer']


@create
class Customer(CRMModel):
    """CRM's customer(s)"""

    company = ForeignKeyField(Company, related_name='customers')
    """A related company"""

    def __str__(self):
        """Returns the customer's full name"""
        return self.name

    def __repr__(self):
        """Returns the customer's ID"""
        return str(self.id)

    @property
    def cid(self):
        """Returns the Customer ID"""
        return self.id

    @cid.setter
    def cid(self, cid):
        """Sets the Customer ID"""
        self.id = cid

    @property
    def sha256name(self):
        """Returns the SHA-256 encoded CID"""
        return str(sha256(str(self.cid).encode()).hexdigest())

    @property
    def name(self):
        """Returns the customer's name"""
        with connection(self):
            name = str(self.company.name) if self.company else ''
        return name
