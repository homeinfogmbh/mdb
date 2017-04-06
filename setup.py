#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo-crm',
    version='latest',
    author='Richard Neumann',
    package_dir={'homeinfo': ''},
    py_modules=['homeinfo.crm'],
    data_files=[
        ('/usr/bin',
         ['files/usr/bin/crmgr'])],
    description='HOMEINFO Customer Relationship Management ORM')
