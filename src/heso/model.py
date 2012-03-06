# -*- coding: utf-8 -*-
"""
    heso.model
    ~~~~~~~~~~

    Implements the model.

    :copyright: (c) 2011 lanius
    :license: Apache License, Version 2.0, see LICENSE for more details.
"""

from hashlib import sha1
import os
from uuid import uuid4

from peewee import Model, CharField, Q

from database import database


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    name = CharField()
    _password = CharField()

    @property
    def password(self):
        return None

    @password.setter
    def password(self, raw_password):
        if isinstance(raw_password, unicode):
            password_8bit = raw_password.encode('utf-8')
        else:
            password_8bit = raw_password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('utf-8')

        self._password = hashed_password

    @password.getter
    def password(self):
        return self._password

    def validate_password(self, raw_password):
        hashed_pass = sha1()
        hashed_pass.update(raw_password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()


def create_tables():
    database.connect()
    try:
        User.create_table()
    except:   # OperationalError
        pass  # database already exists. skip creating tables.
    database.close()
