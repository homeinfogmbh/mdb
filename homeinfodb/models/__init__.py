"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '15.10.2014'

__all__ = ['Address', 'Company', 'Country', 
           'Customer', 'Department', 'Employee']

from .address import Address
from .company import Company
from .country import Country
from .customer import Customer
from .department import Department
from .employee import Employee