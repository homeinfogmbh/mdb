"""
Tables for HOMEINFO's CRM
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

__all__ = ['Customer']

from .abc import CRMModel
from peewee import CharField, TextField

class Customer(CRMModel):
    """
    CRM's customer(s)
    """
    cid = CharField(7)  # A unique customer ID
    name = TextField()  # A representative name
    type = TextField()  # A type like 'bank' or 'realtor', etc.