#! /user/bin/env/ python
# -*- coding: utf-8 -*-
#
# Copyright 2011 lanius
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages

description = ("Heso is web application ",
               "to share snippets and pastes with others.")

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
    heso_add_user = heso.script:add_user
    """,
)
