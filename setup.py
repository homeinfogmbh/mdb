#! /usr/bin/env python3

from setuptools import setup

setup(
    name='homeinfo-crm',
    version='1.0',
    author='Richard Neumann',
    author_email='mail@richard-neumann.de',
    install_requires=['peewee',
                      'mysqlhacks'],
    packages=['homeinfo_crm',
              'homeinfo_crm.models'],
    license=open('LICENSE.txt').read(),
    description='ORM for HOMEINFO\'s CRM database',
    long_description=open('README.txt').read(),
)

from homeinfodb import __tables__
for table in __tables__:
    print('Creating table', table)
    table.create_table(fail_silently=True)
