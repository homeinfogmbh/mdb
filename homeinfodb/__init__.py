"""
ORM for HOMEINFO's CRM database
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Customer']

from homeinfodb.models import *

__tables__ = [Country, State, Address, Company, Department, Employee, Customer]
"""XXX: Order is important here!"""