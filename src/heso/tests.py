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

import os
from shutil import rmtree
import time
import unittest
import application
import controller
from setting import REPO_ROOT


class ControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = controller.app.test_client()

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
        valid_heso = {'description': "This is description.",
                      'files': [{'filename': "heso_test.py",
                                'document': "import heso"}]}
        self.assertFalse(application.is_invalid(valid_heso))

        invalid_heso = {'description': "",
                      'files':[{'filename': "heso_test.py",
                                'document': "import heso"}]}
        self.assertTrue(application.is_invalid(invalid_heso))

        invalid_heso = {'description': "This is description.",
                      'files':[{'filename': "",
                                'document': "import heso"}]}
        self.assertTrue(application.is_invalid(invalid_heso))

    def test_create_heso(self):
        heso = {'description': "This is description.",
                'files': [{'filename': "heso_test.py",
                          'document': "import heso"}]}
        application.create_heso(heso)
        diff = self._get_diff_repos()
        self.assertEqual(len(diff), 1)

    def test_get_heso(self):
        heso = {'description': "This is description.",
                'files':[{'filename': "heso_test.py",
                          'document': "import heso"}]}
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]
        result = application.get_heso(reponame)
        self.assertEqual(result['description'], heso['description'])
        self.assertEqual(result['files'][0]['filename'],
                         heso['files'][0]['filename'])

    def test_get_all_heso(self):
        heso1 = {'description': "This is description. I am Heso 1.",
                'files': [{'filename': "heso_test.py",
                          'document': "import heso"}]}
        application.create_heso(heso1)
        heso2 = {'description': "This is description. I am Heso 2.",
                'files': [{'filename': "heso_test.py",
                          'document': "import heso"}]}
        application.create_heso(heso2)
        heso3 = {'description': "This is description.  I am Heso 3.",
                'files': [{'filename': "heso_test.py",
                          'document': "import heso"}]}
        application.create_heso(heso3)
        
        all_heso = application.get_all_heso()
        expected = self._get_current_repos()
        for heso in all_heso:
            self.assert_(heso['reponame'] in expected)
        
    def test_update_heso(self):
        heso = {'description':"This is description.",
                'files':[{'filename':"heso_test.py",
                          'document':"import heso"}]}
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]
        expected = application.get_heso(reponame)
        expected['description'] = "This heso is updated."
        application.update_heso(reponame, expected)

        result = application.get_heso(reponame)
        self.assertEqual(result['description'], expected['description'])
        self.assertEqual(result['files'][0]['filename'],
                         expected['files'][0]['filename'])

    def test_comment(self):
        heso = {'description': "This is description.",
                'files': [{'filename': "heso_test.py",
                          'document': "import heso"}]}
        application.create_heso(heso)
        reponame = self._get_diff_repos()[0]

        begin_comments = application.get_all_comment(reponame)

        comment1 = "This is test comment 1."
        application.add_comment(reponame, comment1)
        time.sleep(0.001)  # fixme: I don't want to use sleep!

        comment2 = "This is test comment 2."
        application.add_comment(reponame, comment2)
        time.sleep(0.001)  # fixme: I don't want to use sleep!

        comment3 = "This is test comment 3."
        application.add_comment(reponame, comment3)

        comments = application.get_all_comment(reponame)

        self.assertEqual(len(comments), len(begin_comments) + 3)
        self.assertEqual(comments[-1], comment3)

    def _get_current_repos(self):
        return [repodir[0:-4] for repodir in os.listdir(REPO_ROOT)]

    def _get_diff_repos(self):
        reposet = set(self._get_current_repos())
        return list(reposet.difference(set(self.begin_repos)))

    def _remove_repo(self, reponame):
        path = os.path.join(REPO_ROOT, ''.join([reponame, '.git']))
        rmtree(path)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ControllerTestCase))
    suite.addTest(unittest.makeSuite(ApplicationTestCase))
    return suite


if __name__ == '__main__':
    unittest.main()
