#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo-crm',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='info@homeinfo.de',
    maintainer='Richard Neumann',
    maintainer_email='r.neumann@homeinfo.de',
    py_modules=['mdb'],
    scripts=['files/mdbmgr'],
    description='HOMEINFO Master Database ORM.')
