# -*- coding: utf-8 -*-
"""
Heso
----

Heso is a web application to share snippets and pastes with others, and
an open source clone of Gist.

"""
from setuptools import setup, find_packages

description = """Heso is a web application \
to share snippets and pastes with others."""

setup(
    name='Heso',
    version='0.1.0',
    description=description,
    author='lanius',
    author_email='lanius@nirvake.org',
    license='Apache License 2.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Flask',
        'Flask-Mitten',
        'GitPython',
        'WTForms',
        'peewee',
    ],
    entry_points="""
    [paste.app_factory]
    main = heso.controller:make_app
    [console_scripts]
    heso-adduser = heso.script:adduser
    """,
)
