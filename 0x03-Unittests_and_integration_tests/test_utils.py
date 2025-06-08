#!/usr/bin/env python3
"""
Unit tests for the utils module.
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict,
                               path: tuple, expected: object) -> None:
        """
        Test that access_nested_map returns the expected value.
        """
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected
        )

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map: dict,
                                         path: tuple,
                                         expected_message: str) -> None:
        """
        Test that access_nested_map raises
        a KeyError with the expected message.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """
        Test that get_json returns the expected result.
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test class for the memoize decorator.
    """

    def test_memoize(self) -> None:
        """
        Test that memoize caches the result after the first call.
        """
        class TestClass:
            """
            A test class for memoization.
            """

            def a_method(self) -> int:
                """
                Returns 42.
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """
                Returns the value of a_method (should be memoized).
                """
                return self.a_method()

        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_method:
            test_obj = TestClass()
            first_result = test_obj.a_property
            second_result = test_obj.a_property

            self.assertEqual(first_result, 42)
            self.assertEqual(second_result, 42)
            mock_method.assert_called_once()
