"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '15.10.2014'

__all__ = ['Address', 'Contact', 'Country', 'Customer', 'Department']

from .address import Address
from .contact import Contact
from .country import Country
from .customer import Customer
from .department import Department