# -*- coding: utf-8 -*-
"""
    heso.application
    ~~~~~~~~~~~~~~~~

    Implements the application layer, and accesses git repositories.

    :copyright: (c) 2011 lanius
    :license: Apache License, Version 2.0, see LICENSE for more details.
"""

import errno
import os
import stat
from datetime import datetime
from dircache import listdir
from itertools import chain
from random import randrange
from shutil import copyfile, rmtree
from tempfile import gettempdir
from time import time, gmtime, strftime

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


def create_heso(heso, username=None):
    if not username:
        username = 'anonymous'
    reponame = _create_reponame()
    _init_repo(reponame)

    _update_repo(reponame, heso['files'], heso['description'])
    _push_repo(reponame, "create repository.", username)
    _cleanup(reponame)


def update_heso(reponame, heso, username=None):
    if not username:
        username = 'anonymous'
    _update_repo(reponame, heso['files'], heso['description'])
    _push_repo(reponame, "update.", username)
    _cleanup(reponame)


def destroy_heso(reponame):
    _rmtree(_get_repo_path(reponame))


def get_heso(reponame, rev=None):
    repo = _get_repo(reponame)
    commit = repo.commit(rev)
    files = [{'filename': blob.name,
              'document': unicode(blob.data_stream.read(), 'utf-8'),
              'removed': False}
             for blob in commit.tree]
    return {'reponame': reponame,
            'files': files,
            'description': unicode(repo.description, 'utf-8'),
            # fixme: do you want to oldest committed date?
            'created': strftime('%b %d, %Y',
                                gmtime(commit.committed_date))}


def get_all_heso():
    return [get_heso(reponame) for reponame in _get_reponames()]


def get_history(reponame):
    return [{'rev': c.hexsha, 'revshort': c.hexsha[0:5],
             'author': c.author.name,
             'timestamp': _prettytime(c.committed_date)}
            for c in _get_repo(reponame).iter_commits()]


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
        file_path = os.path.join(tmp_path, f['filename'])
        if f['removed']:
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                pass
        else:
            with open(file_path, 'w') as fp:
                doc = _replace_lfcode(f['document'].encode('utf-8'))
                fp.write(doc)
    repo.description = description.encode('utf-8')


def _push_repo(reponame, comment,
               username='anonymous', email='heso@nirvake.org'):
    repo = Repo(_get_tmp_path(reponame))
    repo.git.add('-A')
    try:
        repo.git.commit('-m', '{0}'.format(comment),
                        '--author', '{0} <{1}>'.format(username, email))
        repo.git.push(_get_repo_path(reponame), 'master')
    except:
        # todo: handle error.
        pass


def _cleanup(reponame):
    _rmtree(_get_tmp_path(reponame))


def _get_tmp_path(reponame):
    return os.path.join(gettempdir(), reponame)


def _get_comment_path(reponame):
    return os.path.join(_get_repo_path(reponame), 'comments')


def _rmtree(path):
    rmtree(path, ignore_errors=False, onerror=_handle_readonly)


def _prettytime(timestamp):
    """See http://stackoverflow.com/questions/410221/natural-relative-days-in-python"""
    d = datetime.fromtimestamp(timestamp)
    diff = datetime.today() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime('%d %b %y')
    elif diff.days == 1:
        return '1 day ago'
    elif diff.days > 1:
        return '{0} days ago'.format(diff.days)
    elif s <= 1:
        return 'just now'
    elif s < 60:
        return '{0} seconds ago'.format(s)
    elif s < 120:
        return '1 minute ago'
    elif s < 3600:
        return '{0} minutes ago'.format(s / 60)
    elif s < 7200:
        return '1 hour ago'
    else:
        return '{0} hours ago'.format(s / 3600)


def _handle_readonly(func, path, exc):
    """For Windows.
    See http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows.
    """
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def _replace_lfcode(text):
    """For Windows."""
    return text.replace('\r', '')


if __name__ == '__main__':
    pass
