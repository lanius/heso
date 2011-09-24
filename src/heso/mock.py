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

"""Mock for application."""


def is_invalid(heso):
    return False


def create_heso(heso):
    pass


def update_heso(reponame, heso):
    pass


def get_heso(reponame):
    files = _get_mock_files()
    return {'reponame': "aBcDeFg",
            'files': files,
            'description': "this is test description.",
            'created': "Sep 14, 2011"}


def get_all_heso():
    return [get_heso("mock")]


def add_comment(reponame, comment):
    pass


def get_all_comment(reponame):
    comments = ["this is test comment.", "enjoy Heso life!"]
    return comments


def _get_mock_files():
    files = []
    files.append({'filename': "add.py", 'document': """import this
def add(x, y):
    return x + y
x = 1
y = 2
print add(x, y)
"""})
    files.append({'filename': "hello.html", 'document': """<html>
<head>
    <title>Hello World</title>
</head>
<body>
    Hello World, Heso!
</body>
</html>"""})
    return files


if __name__ == "__main__":
    pass
