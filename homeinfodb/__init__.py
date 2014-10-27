"""
ORM for HOMEINFO's CRM database
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Customer']

from homeinfodb.models import *

__tables__ = [Customer, Country, State, Address, Company, Department, Employee]
"""XXX: Order is important here!"""