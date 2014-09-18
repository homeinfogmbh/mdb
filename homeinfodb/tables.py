"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

from .config import CRMModel
from peewee import CharField, TextField, IntegerField, ForeignKeyField

class Customers(CRMModel):
    """
    CRM's customer(s)
    """
    cid = CharField(7)  # A unique customer ID
    name = TextField()  # A representative name
    type = TextField()  # A type like 'bank' or 'realtor', etc.
    
    
class Countries(CRMModel):
    """
    Country data
    """
    iso = CharField(3)
    name = TextField()
    

class Addresses(CRMModel):
    """
    Address data
    """
    customer = ForeignKeyField(Customers, related_name='departments')
    street = TextField(null=True)
    house_number = CharField(45, null=True)
    zip = IntegerField(11, null=True)       # ZIP code
    po_box = TextField(null=True)           # Post box
    city = TextField()
    country = ForeignKeyField(Countries)
    
    
class Departments(CRMModel):
    """
    Departments of companies
    """
    customer = ForeignKeyField(Customers, related_name='departments')
    name = TextField()  # A representative name
    type = TextField()  # A type like 'IT', 'customer service', etc.
    
    
class Contacts(CRMModel):
    """
    Contact persons
    """
    department = ForeignKeyField(Departments, related_name='staff')
    first_name = TextField(null=True)
    surname = TextField()
    phone = TextField()
    phone_alt = TextField(null=True)
    cellphone = TextField(null=True)
    fax = TextField(null=True)
    email = TextField(null=True)