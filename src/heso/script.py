# -*- coding: utf-8 -*-
"""
    heso.script
    ~~~~~~~~~~~

    Implements helpers to be generated as commands.

    :copyright: (c) 2011 lanius
    :license: Apache License, Version 2.0, see LICENSE for more details.
"""

import getpass
import sys

from model import User, create_tables
from database import database


def adduser(_=None):
    create_tables()

    username = raw_input('Username:')
    user = None
    try:
        user = User.get(name=username)
    except User.DoesNotExist:
        pass  # ok
    if user:
        sys.exit("The username has been already used.")
    password = getpass.getpass()
    user = User(name=username, password=password)
    user.save()
    print("The user was created successfully.")

    database.close()
