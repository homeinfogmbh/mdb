"""
Company related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Company', 'Department', 'Employee']

from .abc import CRMModel
from .address import Address
from peewee import TextField, ForeignKeyField

class Company(CRMModel):
    """
    A company
    """
    name = TextField()
    """A representative name"""
    address = ForeignKeyField(Address, null=True)
    """The employee's address"""
    annotation = TextField()
    """Type like 'bank' or 'realtor', etc."""
    

class Department(CRMModel):
    """
    Departments of companies
    """
    company = ForeignKeyField(Company, related_name='departments')
    """The company, this department belongs to"""
    name = TextField()
    """A representative name"""
    type = TextField()
    """A type like 'IT', 'customer service', etc."""
    
    
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