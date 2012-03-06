# -*- coding: utf-8 -*-
"""
    heso.heroku
    ~~~~~~~~~~~

    Implements a helper for running Heso on Heroku.

    :copyright: (c) 2011 lanius
    :license: Apache License, Version 2.0, see LICENSE for more details.
"""

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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
