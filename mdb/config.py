"""Common configuration."""

from logging import getLogger

from configlib import loadcfg
from peeweeplus import MySQLDatabase


__all__ = ['CONFIG', 'DATABASE', 'LOGGER']


CONFIG = loadcfg('mdb.conf')
DATABASE = MySQLDatabase.from_config(CONFIG['db'])
LOGGER = getLogger(__file__)
