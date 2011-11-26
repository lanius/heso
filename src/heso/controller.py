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

from flask import Flask, request, render_template, abort, redirect, url_for
from setting import REPO_ROOT
from application import *
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


@app.route('/')
def index():
    hesoes = get_all_heso()
    return render_template('index.html', hesoes=hesoes)


@app.route('/create', methods=['POST'])
def create():
    heso = extract_heso(request.form)

    if is_invalid(heso):
        message = u'all fields are required.'
        hesoes = get_all_heso()
        return render_template('index.html',
                               hesoes=hesoes, error_message=message)

    create_heso(heso)
    return redirect(url_for('index'))


@app.route('/<reponame>', methods=['GET', 'POST'])
def heso(reponame):
    if request.method == 'GET':
        heso = get_heso(reponame)
        comments = get_all_comment(reponame)
        return render_template('heso.html', heso=heso, comments=comments)

    if request.method == 'POST':
        heso = extract_heso(request.form)

        if is_invalid(heso):
            message = u'all fields are required.'
            hesoes = get_all_heso()
            return render_template('index.html',
                                   hesoes=hesoes, error_message=message)

        update_heso(reponame, heso)
        return redirect(url_for('heso', reponame=reponame))


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
    files = []
    idx = 0
    while True:
        filename = form.get('filename[{0}]'.format(idx))
        document = form.get('document[{0}]'.format(idx))
        removed_str = form.get('removed[{0}]'.format(idx))

        if (not filename) and (not document) and (not removed_str):
            break

        removed = True if removed_str == u'true' else False

        files.append({'filename': filename, 'document': document,
                      'removed': removed})
        idx += 1

    return {'files': files, 'description': form.get('description')}


def make_app(global_conf={}):
    app.debug = False
    return app


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    app = make_app()
    app.debug = True
    app.run(host=host, port=port)
