""" PasswordState Test """

import unittest

from passwordstate_password_fact import Password
from passwordstate_password_fact import PasswordState
from ddt import ddt, data, unpack
import mock


class PasswordTest(unittest.TestCase):
    """PasswordTest"""

    @mock.patch("requests.get", autospec=True)
    def test_gather_facts_id(self, mock_get):
        """gather facts by id"""
        value = [
            {
                "Password": "foo",
                "Title": "bar",
                "UserName": "foobar",
                "GenericField1": "123",
                "PasswordID": 999,
            }
        ]
        mock_get.return_value = mock.Mock(status_code=200, json=lambda: value)

        module = mock.Mock()
        url = "http://passwordstate"
        api_key = "abc123xyz"

        api = PasswordState(module, url, api_key)
        password = Password(api, "123", {"id": "999", "field": None, "field_id": None})

        facts = password.gather_facts("fact_name_prefix")
        expected = {
            "fact_name_prefix_password": "foo",
            "fact_name_prefix_username": "foobar",
        }
        self.assertEqual(expected, facts)

    @mock.patch("requests.get", autospec=True)
    def test_gather_facts_field(self, mock_get):
        """gather facts by custom field"""
        value = [
            {
                "Password": "foo",
                "Title": "bar",
                "UserName": "foobar",
                "GenericField1": "123",
                "PasswordID": 999,
            }
        ]
        mock_get.return_value = mock.Mock(status_code=200, json=lambda: value)

        module = mock.Mock()
        url = "http://passwordstate"
        api_key = "abc123xyz"

        api = PasswordState(module, url, api_key)
        password = Password(
            api, "123", {"id": None, "field": "GenericField1", "field_id": "123"}
        )

        facts = password.gather_facts("fact_name_prefix")
        expected = {
            "fact_name_prefix_password": "foo",
            "fact_name_prefix_username": "foobar",
        }
        self.assertEqual(expected, facts)
