"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Employee']

from .abc import CRMModel
from .department import Department
from .address import Address
from peewee import ForeignKeyField, TextField
    
class Employee(CRMModel):
    """
    Employees
    """
    department = ForeignKeyField(Department, related_name='staff')
    """The department this employee is working in"""
    first_name = TextField(null=True)
    """The employee's first name"""
    surname = TextField()
    """The employee's surname"""
    phone = TextField()
    """The employee's phone number"""
    cellphone = TextField(null=True)
    """The employee's cell phone number"""
    email = TextField(null=True)
    """The employee's email address"""
    phone_alt = TextField(null=True)
    """An alternative phone number"""
    fax = TextField(null=True)
    """The employee's fax number"""
    address = ForeignKeyField(Address, null=True)
    """The employee's address"""