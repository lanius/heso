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

"""Test script of Heso."""

import errno, stat
import os
from shutil import rmtree
import time
import unittest
import application
import controller
from setting import REPO_ROOT


class ControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = controller.make_app().test_client()

    def tearDown(self):
        pass

    def test_index(self):
        rv = self.app.get('/')
        self.assert_("Heso" in rv.data)

class ApplicationTestCase(unittest.TestCase):

    def setUp(self):
        self.begin_repos = self._get_current_repos()

    def tearDown(self):
        diff = self._get_diff_repos()
        for reponame in diff:
            self._remove_repo(reponame)

    def test_is_invalid(self):
        valid_heso = self._make_heso()
        self.assertFalse(application.is_invalid(valid_heso))

        desc_blank_heso = valid_heso.copy()
        desc_blank_heso['description'] = ""
        self.assertTrue(application.is_invalid(desc_blank_heso))

        fname_blank_heso = valid_heso.copy()
        fname_blank_heso['files'][0]['filename'] = ""
        self.assertTrue(application.is_invalid(fname_blank_heso))

    def test_create_heso(self):
        heso = self._make_heso()
        application.create_heso(heso)
        diff = self._get_diff_repos()
        self.assertEqual(len(diff), 1)

    def test_update_heso(self):
        heso = self._make_heso()
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]
        expected = application.get_heso(reponame)
        expected['description'] = "This heso is updated."
        application.update_heso(reponame, expected)

        result = application.get_heso(reponame)
        self.assertEqual(result['description'], expected['description'])
        self.assertEqual(result['files'][0]['filename'],
                         expected['files'][0]['filename'])

    def test_destroy_heso(self):
        heso = self._make_heso()
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]
        application.destroy_heso(reponame)
        self.assert_(reponame not in self._get_current_repos())

    def test_get_heso(self):
        heso = self._make_heso()
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]
        result = application.get_heso(reponame)
        self.assertEqual(result['description'], heso['description'])
        self.assertEqual(result['files'][0]['filename'],
                         heso['files'][0]['filename'])

    def test_get_all_heso(self):
        for i in xrange(3):
            heso = self._make_heso()
            heso['description'] = "Heso description number {0}.".format(i+1)
            application.create_heso(heso)

        all_heso = application.get_all_heso()
        expected = self._get_current_repos()
        for heso in all_heso:
            self.assert_(heso['reponame'] in expected)

    def test_get_history(self):
        heso = self._make_heso()
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]

        heso['files'][0]['document'] = "This heso is updated once."
        application.update_heso(reponame, heso)
        heso['files'][0]['document'] = "This heso is updated twice."
        application.update_heso(reponame, heso)

        history = application.get_history(reponame)
        self.assertEqual(len(history), 3)

    def test_comment(self):
        heso = self._make_heso()
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]

        begin_comments = application.get_all_comment(reponame)
        for i in xrange(3):
            comment = "This is test comment number {0}.".format(i+1)
            application.add_comment(reponame, comment)
            time.sleep(0.001)  # fixme: I don't want to use sleep!
        comments = application.get_all_comment(reponame)
        self.assertEqual(len(comments), len(begin_comments) + 3)

    def _make_heso(self):
        return {'description': "This is a test description.",
                'files': [
                    {'filename': "heso_test.py",
                     'document': "import heso",
                     'removed': False}
                    ]}

    def _get_current_repos(self):
        return [repodir[0:-4] for repodir in os.listdir(REPO_ROOT)]

    def _get_diff_repos(self):
        reposet = set(self._get_current_repos())
        return list(reposet.difference(set(self.begin_repos)))

    def _remove_repo(self, reponame):
        application.destroy_heso(reponame)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ControllerTestCase))
    suite.addTest(unittest.makeSuite(ApplicationTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
