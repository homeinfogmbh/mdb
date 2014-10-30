"""
Company related models for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Company', 'Department', 'Employee']

from .abc import CRMModel
from .address import Address
from peewee import CharField, ForeignKeyField

class Company(CRMModel):
    """
    A company
    """
    name = CharField(64)
    """A representative name"""
    address = ForeignKeyField(Address, db_column='address', null=True)
    """The employee's address"""
    annotation = CharField(256, null=True)
    """Type like 'bank' or 'realtor', etc."""
    

class Department(CRMModel):
    """
    Departments of companies
    """
    company = ForeignKeyField(Company, db_column='company', 
                              related_name='departments')
    """The company, this department belongs to"""
    name = CharField(64)
    """A representative name"""
    type = CharField(64, null=True)
    """A type like 'IT', 'customer service', etc."""
    
    
class Employee(CRMModel):
    """
    Employees
    """
    department = ForeignKeyField(Department, db_column='department',
                                 related_name='staff')
    """The department this employee is working in"""
    first_name = CharField(32, null=True)
    """The employee's first name"""
    surname = CharField(32)
    """The employee's surname"""
    phone = CharField(32)
    """The employee's phone number"""
    cellphone = CharField(32, null=True)
    """The employee's cell phone number"""
    email = CharField(64, null=True)
    """The employee's email address"""
    phone_alt = CharField(32, null=True)
    """An alternative phone number"""
    fax = CharField(32, null=True)
    """The employee's fax number"""
    address = ForeignKeyField(Address, db_column='address', null=True)
    """The employee's address"""