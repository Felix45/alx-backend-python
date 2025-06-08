#!/usr/bin/env python3
"""
Unit tests for the client module.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

# Unpack TEST_PAYLOAD[0]
org_payload, repos_payload, expected_repos, apache2_repos = TEST_PAYLOAD[0]


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client_instance = GithubOrgClient(org_name)
        result = client_instance.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org) -> None:
        """
        Test that _public_repos_url returns the correct value.
        """
        mock_org.return_value = {"repos_url": "http://some_url.com"}
        client_instance = GithubOrgClient("google")

        result = client_instance._public_repos_url

        self.assertEqual(result, "http://some_url.com")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """
        Test that public_repos returns the expected list of repos.
        """
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://some_url.com"
            client_instance = GithubOrgClient("google")

            result = client_instance.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "http://some_url.com"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: dict,
                         license_key: str, expected: bool) -> None:
        """
        Test that has_license returns the correct boolean value.
        """
        client_instance = GithubOrgClient("google")
        result = client_instance.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup class by patching requests.get and defining side effects.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url.endswith("/orgs/google"):
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url.endswith("/orgs/google/repos"):
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the patched requests.get.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test that public_repos returns the expected repos.
        """
        client_instance = GithubOrgClient("google")
        result = client_instance.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos with license filtering.
        """
        client_instance = GithubOrgClient("google")
        result = client_instance.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
