#!/usr/bin/env python3
"""Module for testing utils."""
import unittest
from unittest.mock import patch
class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("SetupClass")
    @classmethod
    def tearDownClass(cls):
        print("TearDownClass")
    @patch(\"requests.get\")
    def test_public_repos(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [\"repo1\", \"repo2\"]
        self.assertEqual(len(mock_get.return_value.json()), 2)
if __name__ == \"__main__\":
    unittest.main()
