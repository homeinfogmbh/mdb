"""
Homeinfo main package configuration
"""
from configparser import ConfigParser

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '20.11.2014'
__all__ = ['config', 'crm']

_CONFIG_FILE = '/usr/local/etc/homeinfo.cfg'
config = ConfigParser()
config.read(_CONFIG_FILE)
crm = config['crm']
