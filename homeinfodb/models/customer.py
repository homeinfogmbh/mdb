"""
Customer related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Customer']

from .abc import CRMModel
from .company import Company
from peewee import ForeignKeyField

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
    def cid (self, cid):
        """Sets the Customer ID"""
        self.id = cid
        
    @property
    def name(self):
        """Returns the customer's name"""
        return self.company.name