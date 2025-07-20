"""Module for testing GitHubOrgClient utilities.""" 

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from client import GitHubOrgClient

class TestGitHubOrgClient(unittest.TestCase):
    """Tests for GitHubOrgClient methods"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop patcher for requests.get"""
        cls.get_patcher.stop()

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        client = GitHubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

    def test_public_repos(self):
        """Test public_repos returns repo names"""
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_response = MagicMock()
        mock_response.json.return_value = payload
        self.mock_get.return_value = mock_response

        client = GitHubOrgClient("test_org")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])

