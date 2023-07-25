#! /usr/bin/env python3
"""Installation script."""

from setuptools import setup


setup(
    name="mdb",
    use_scm_version={"local_scheme": "node-and-timestamp"},
    setup_requires=["setuptools_scm"],
    install_requires=["configlib", "peewee", "peeweeplus"],
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="info@homeinfo.de",
    maintainer="Richard Neumann",
    maintainer_email="r.neumann@homeinfo.de",
    packages=["mdb", "mdb.mgr"],
    entry_points={"console_scripts": ["mdbmgr = mdb.mgr:main"]},
    description="HOMEINFO Master Database ORM.",
)
