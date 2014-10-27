"""
Database static configuration
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

from peewee import MySQLDatabase

DB = 'homeinfo'
HOST = 'mysql.homeinfo.de'
USER = 'homeinfo'
PASSWD = 'Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W'

database = MySQLDatabase(DB, host=HOST, user=USER, passwd=PASSWD)