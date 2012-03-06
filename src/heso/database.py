# -*- coding: utf-8 -*-
"""
    heso.database
    ~~~~~~~~~~~~~

    Decides the database to use.

    :copyright: (c) 2011 lanius
    :license: Apache License, Version 2.0, see LICENSE for more details.
"""

from peewee import SqliteDatabase
#from peewee import MySQLDatabase

from setting import USER_DB_FILE

database = SqliteDatabase(USER_DB_FILE, threadlocals=True)
#database = MySQLDatabase(...)
