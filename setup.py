#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo.crm',
    version='3.0.0-1',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    requires=['peewee',
              'homeinfo.lib'],
    package_dir={'homeinfo': ''},
    packages=['homeinfo.crm'],
    data_files=[('/usr/local/etc', ['files/etc/crm.conf'])],
    description="HOMEINFO's CRM database ORM",
)
