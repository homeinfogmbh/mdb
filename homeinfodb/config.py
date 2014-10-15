"""
Database static configuration
"""
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'

from peewee import MySQLDatabase

deferred_db = MySQLDatabase('homeinfo', host='mysql.homeinfo.de', 
                            user='homeinfodb', 
                            passwd='Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W')