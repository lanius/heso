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

"""Main script for running Heso on Heroku."""

import os
from setting import REPO_ROOT
from controller import app, make_app
from application import get_all_heso, destroy_heso

REMAINED = 8


@app.route('/clean')
def clean():
    for i, heso in enumerate(get_all_heso()):
        if REMAINED <= i:
            destroy_heso(heso['reponame'])
    return "Cleaning has been completed"


if __name__ == '__main__':
    if not os.path.exists(REPO_ROOT):
        os.mkdir(REPO_ROOT)
    app = make_app()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
