"""
Abstract base classes for HOMEINFO's ORM database
"""
from peewee import Model
from playhouse.pool import PooledMySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['CRMModel']

DB = 'homeinfo'
HOST = 'mysql.homeinfo.de'
USER = 'homeinfo'
PASSWD = 'Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W'

database = PooledMySQLDatabase(DB, host=HOST, user=USER, 
                               passwd=PASSWD, threadlocals=True)

class CRMModel(Model):
    """
    Generic HOMEINFO-DB Model
    """
    class Meta:
        database = database
        schema = DB