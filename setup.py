#! /usr/bin/env python3

from distutils.core import setup

setup(
    name='homeinfo',
    version='1.0',
    author='Richard Neumann',
    author_email='r.neumann@homeinfo.de',
    requires=['peewee',
              'homeinfo'],
    package_dir={'homeinfo': ''},
    packages=['homeinfo.crm'],
    data_files=[('/usr/local/etc', ['files/etc/crm.conf'])],
    license=open('LICENSE.txt').read(),
    description='HOMEINFO ORM database root',
    long_description=open('README.txt').read(),
)
