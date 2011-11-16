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

"""Controller of Heso."""

import os
from flask import Flask, request, render_template, abort, redirect, url_for, flash
from setting import REPO_ROOT
from application import *
from forms import HesoForm
#from mock import *


app = Flask(__name__)


@app.before_request
def before_request():
    pass


@app.after_request
def after_request(response):
    response.headers['Server'] = 'I am heso !'
    return response


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = HesoForm(request.form)
    if request.method == 'POST':
        if form.validate():
            create_heso(extract_heso(form))
            return redirect(url_for('index'))
        flash(u'all fields are required.')
    hesoes = get_all_heso()
    return render_template('index.html', hesoes=hesoes, form=form, for_create=True)


@app.route('/<reponame>', methods=['GET', 'POST'])
def heso(reponame):
    if request.method == 'POST':
        form = HesoForm(request.form)
        if form.validate():
            update_heso(reponame, extract_heso(form))
            return redirect(url_for('heso', reponame=reponame))
        flash(u'all fields are required.')
    else:
        form = HesoForm(**get_heso(reponame))
    comments = get_all_comment(reponame)
    hesoes = get_all_heso()
    return render_template('index.html', reponame=reponame, hesoes=hesoes, form=form,
            comments=comments)


@app.route('/<reponame>/comment', methods=['POST'])
def comment(reponame):
    comment = request.form.get('comment')
    add_comment(reponame, comment)
    return redirect(url_for('heso', reponame=reponame))


@app.errorhandler(500)
def error(e):
    message = u'any error occured.'
    hesoes = get_all_heso()
    return render_template('index.html',
                           hesoes=hesoes, error_message=message)


def extract_heso(form):
    return {
                'files': [
                    { 'filename': f.filename.data, 'document': f.document.data, }
                    for f in form.files.entries
                ],
                'description': form.description.data
            }


def make_app(global_conf={}):
    app.debug = False
    app.secret_key = os.urandom(24)
    return app


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    app = make_app()
    app.debug = True
    app.run(host=host, port=port)
