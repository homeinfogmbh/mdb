"""
Customer related models for HOMEINFO's CRM
"""
from .abc import CRMModel
from .company import Company
from peewee import ForeignKeyField

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Customer']


class Customer(CRMModel):
    """
    CRM's customer(s)
    """
    company = ForeignKeyField(Company, related_name='customers')
    """A related company"""
    # TODO: Add other stuff like merchants etc.

    @property
    def cid(self):
        """Returns the Customer ID"""
        return self.id

    @cid.setter
    def cid(self, cid):
        """Sets the Customer ID"""
        self.id = cid

    @property
    def name(self):
        """Returns the customer's name"""
        return str(self.company.name) if self.company else ''

    def __str__(self):
        """Returns a string representation of the customer"""
        return self.name

    def __repr__(self):
        """Returns a string representation of the customer"""
        return str(self.cid)
