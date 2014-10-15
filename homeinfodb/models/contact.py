"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Contact']

from .abc import CRMModel
from .department import Department
from peewee import ForeignKeyField, TextField
    
class Contact(CRMModel):
    """
    Contact persons
    """
    department = ForeignKeyField(Department, related_name='staff')
    first_name = TextField(null=True)
    surname = TextField()
    phone = TextField()
    phone_alt = TextField(null=True)
    cellphone = TextField(null=True)
    fax = TextField(null=True)
    email = TextField(null=True)