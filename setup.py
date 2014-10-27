#! /usr/bin/env python3

from setuptools import setup

setup(
	name='homeinfodb',
	version='1.0',
	author='Richard Neumann',
	author_email='mail@richard-neumann.de',
    install_requires=['peewee'],
	packages=['homeinfodb',
			'homeinfodb.models'],
	license=open('LICENSE.txt').read(),
	description='ORM for HOMEINFO\'s CRM database',
	long_description=open('README.txt').read(),
)

from homeinfodb import __tables__
for table in __tables__:
	table.create_table(fail_silently=True)