"""
Abstract base classes for HOMEINFO's ORM database
"""
from peewee import Model
from mysqlhacks import ProcessSaveMySQLDatabase

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['CRMModel']

DB = 'homeinfo_crm'
HOST = 'mysql.homeinfo.de'
USER = 'homeinfo_crm'
PASSWD = 'Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W'


class CRMModel(Model):
    """
    Generic HOMEINFO-DB Model
    """
    class Meta:
        database = ProcessSaveMySQLDatabase(DB, host=HOST,
                                            user=USER, passwd=PASSWD)
        database.get_conn().ping(True)
        schema = DB
