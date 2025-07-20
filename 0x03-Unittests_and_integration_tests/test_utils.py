"""Module for testing GitHubOrgClient utilities.""" 

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from client import GitHubOrgClient

class TestGitHubOrgClient(unittest.TestCase):
    """Unit tests for GitHubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down patcher"""
        cls.get_patcher.stop()

    @parameterized.expand([
        ("google", True),
        ("abc", False),
    ])
    def test_has_license(self, org, expected):
        """Test has_license method"""
        client = GitHubOrgClient(org)
        repo = {"license": {"key": "mit"}} if expected else {"license": {"key": "apache-2.0"}}
        self.assertEqual(client.has_license(repo, "mit"), expected)

    def test_public_repos(self):
        """Test public_repos with mocked requests"""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        self.mock_get.return_value.json.return_value = test_payload
        client = GitHubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, ["repo1", "repo2"])

if __name__ == "__main__":
    unittest.main()

