#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo',
    version='1.0',
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    requires=['peewee',
              'mysqlhacks'],
    packages=['homeinfo',
              'homeinfo.crm'],
    license=open('LICENSE.txt').read(),
    description='HOMEINFO ORM database root',
    long_description=open('README.txt').read(),
)

from homeinfo.crm import __tables__
for table in __tables__:
    print('Creating table', table)
    table.create_table(fail_silently=True)
