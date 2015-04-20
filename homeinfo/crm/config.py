"""Basic CRM system configuration"""

from configparser import ConfigParser

__date__ = '12.12.2014'
__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__all__ = ['db']

CONFIG_FILE = '/usr/local/etc/crm.conf'
config = ConfigParser()
config.read(CONFIG_FILE)
db = config['db']
