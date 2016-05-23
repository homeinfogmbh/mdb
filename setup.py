#! /usr/bin/env python3

from distutils.core import setup
from homeinfo.lib.misc import GitInfo

version, author, author_email, *_ = GitInfo()

setup(
    name='homeinfo-crm',
    version=version,
    author=author,
    author_email=author_email,
    requires=[
        'peewee',
        'homeinfo-peewee',
        'homeinfo.lib'],
    package_dir={'homeinfo': ''},
    py_modules=['homeinfo.crm.py'],
    data_files=[('/usr/bin', ['files/usr/bin/crmgr'])],
    description='HOMEINFO Customer Relationship Management ORM')
