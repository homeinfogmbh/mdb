#! /usr/bin/env python3

from distutils.core import setup
from homeinfo.lib.misc import GitInfo

version, author, author_email, *_ = GitInfo()

setup(
    name='homeinfo-crm',
    version=version,
    author=author,
    author_email=author_email,
    requires=['peewee',
              'homeinfo.lib'],
    package_dir={'homeinfo': ''},
    packages=['homeinfo.crm'],
    data_files=[('/usr/local/etc', ['files/etc/crm.conf'])],
    description='HOMEINFO Customer Relationship Management ORM',
)
