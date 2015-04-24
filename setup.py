#! /usr/bin/env python3

from distutils.core import setup
from homeinfo.lib.misc import GitInfo

version, author, email, *_ = GitInfo()

setup(
    name='HOMEINFO Customer Relationship Management',
    version=version,
    author=author,
    author_email=email,
    requires=['peewee',
              'homeinfo.lib'],
    package_dir={'homeinfo': ''},
    packages=['homeinfo.crm'],
    data_files=[('/usr/local/etc', ['files/etc/crm.conf'])],
    description="HOMEINFO's CRM database ORM",
)
