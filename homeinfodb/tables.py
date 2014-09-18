'''
Created on 18.09.2014

@author: neumannr
'''
from .config import HIDBModel
from peewee import CharField, TextField

class Customer(HIDBModel):
    """
    HOMEINFO's customer(s)
    """
    cid = CharField(7)  # Customer' unique ID
    name = TextField()  # Customer's name
    

class Address(HIDBModel):
    """
    An Address
    """
    street = TextField()
    house_number = TextField()
    