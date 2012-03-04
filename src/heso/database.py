#! /user/bin/env/ python
# -*- coding: utf-8 -*-
#
# Copyright 2012 lanius
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

"""Database of Heso."""

from peewee import SqliteDatabase
#from peewee import MySQLDatabase

from setting import USER_DB_FILE

database = SqliteDatabase(USER_DB_FILE, threadlocals=True)
#database = MySQLDatabase(...)