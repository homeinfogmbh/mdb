"""Customer related models for HOMEINFO's CRM"""

from hashlib import sha256
from peewee import ForeignKeyField, create
from .abc import CRMModel
from .company import Company

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
    def sha256name(self):
        """Returns the SHA-256 encoded CID"""
        return str(sha256(str(self.cid).encode()).hexdigest())

    @property
    def name(self):
        """Returns the customer's name"""
        return str(self.company.name) if self.company else ''
