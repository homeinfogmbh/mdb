"""Tables for HOMEINFO's CRM"""

from .address import Address
from .company import Company, Department, Employee
from .geo import Country, State
from .customer import Customer

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '15.10.2014'
__all__ = ['Address', 'Company', 'Department', 'Employee',
           'Country', 'State', 'Customer']
