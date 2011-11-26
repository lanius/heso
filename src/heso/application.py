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

"""Application of Heso."""

import os
from dircache import listdir
from itertools import chain
from random import randrange
from shutil import copyfile, rmtree
from time import time, gmtime, strftime
from tempfile import gettempdir
from git import Repo
from setting import REPO_ROOT


def is_invalid(heso):
    files = heso['files']
    description = heso['description']
    if all(chain(*[[f['filename'], f['document']] for f in files
                   if not f['removed']])) and description:
        return False
    else:
        return True


def create_heso(heso):
    reponame = _create_reponame()
    _init_repo(reponame)

    _update_repo(reponame, heso['files'], heso['description'])
    _push_repo(reponame, "create repository.")
    _cleanup(reponame)


def update_heso(reponame, heso):
    _update_repo(reponame, heso['files'], heso['description'])
    _push_repo(reponame, "update.")
    _cleanup(reponame)


def destroy_heso(reponame):
    rmtree(_get_repo_path(reponame))


def get_heso(reponame):
    repo = _get_repo(reponame)
    files = [{'filename': blob.name,
              'document': unicode(blob.data_stream.read(), 'utf-8'),
              'removed': False}
             for blob in repo.tree()]
    return {'reponame': reponame,
            'files': files,
            'description': unicode(repo.description, 'utf-8'),
            # fixme: do you want to oldest committed date?
            'created': strftime("%b %d, %Y",
                               gmtime(repo.commit().committed_date))}


def get_all_heso():
    return [get_heso(reponame) for reponame in _get_reponames()]


def add_comment(reponame, comment):
    filename = ''.join([str(int(time() * 1000)), '.rst'])
    filepath = os.path.join(_get_comment_path(reponame), filename)
    with open(filepath, 'w') as fp:
        fp.write(comment.encode('utf-8'))


def get_all_comment(reponame):
    files = sorted(os.listdir(_get_comment_path(reponame)))
    comments = []
    for f in files:
        with open(os.path.join(_get_comment_path(reponame), f), 'r') as fp:
            comments.append(unicode(fp.read(), 'utf-8'))
    return comments


def _create_reponame():
    # fixme: generate unique name.
    key_length = 8
    _letter = map(lambda _i: chr(_i), range(65, 91))
    _letter.extend(map(lambda _i: chr(_i), range(97, 123)))
    name = ''.join(map(lambda _i: _letter[randrange(50)], range(key_length)))
    if name in _get_reponames():
        raise Exception("generated name is already used. please retry.")
    return name


def _init_repo(reponame):
    repo = Repo.init(_get_repo_path(reponame), bare=True)
    os.mkdir(_get_comment_path(reponame))
    return repo


def _get_reponames():
    files = [r for r in listdir(REPO_ROOT) if r.endswith('.git')]
    files = sorted(files,
                   key=lambda f: os.stat(os.path.join(REPO_ROOT, f)).st_mtime,
                   reverse=True)
    return [filename[0:-4] for filename in files]


def _get_repo(reponame):
    return Repo(_get_repo_path(reponame))


def _get_repo_path(reponame):
    return '{0}.git'.format(os.path.join(REPO_ROOT, reponame))


def _update_repo(reponame, files, description):
    repo = _get_repo(reponame)
    tmp_path = os.path.join(gettempdir(), reponame)
    repo.clone(tmp_path)
    for f in files:
        file_path =os.path.join(tmp_path, f['filename'])
        if f['removed']:
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
        else:
            with open(file_path, 'w') as fp:
                fp.write(f['document'].encode('utf-8'))
    repo.description = description.encode('utf-8')


def _push_repo(reponame, comment):
    repo = Repo(_get_tmp_path(reponame))
    repo.git.add('-A')
    try:
        repo.git.commit('-m', '"{0}"'.format(comment))
        repo.git.push(_get_repo_path(reponame), 'master')
    except:
        # todo: handle error.
        pass


def _cleanup(reponame):
    rmtree(_get_tmp_path(reponame))


def _get_tmp_path(reponame):
    return os.path.join(gettempdir(), reponame)


def _get_comment_path(reponame):
    return os.path.join(_get_repo_path(reponame), 'comments')


if __name__ == '__main__':
    pass
