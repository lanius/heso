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

"""Helper script that create a user."""

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
