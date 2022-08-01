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
                "PasswordID": 999,
                "Password": "foo",
                "UserName": "foobar",
                "Title": "bar",
                "HostName": "foobar_host",
                "Domain": "",
                "Description": "",
                "Notes": "",
                "URL": "http://passwordstate",
                "AccountType": "",
                "AccountTypeID": "",
                "GenericField1": "123",
                "GenericField2": "",
                "GenericField3": "",
                "GenericField4": "",
                "GenericField5": "",
                "GenericField6": "",
                "GenericField7": "",
                "GenericField8": "",
                "GenericField9": "",
                "GenericField10": "",
                "GenericFieldInfo": "",
                "ExpiryDate": "2051-05-12",
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
            "fact_name_prefix_passwordid": 999,
            "fact_name_prefix_password": "foo",
            "fact_name_prefix_username": "foobar",
            "fact_name_prefix_title": "bar",
            "fact_name_prefix_hostname": "foobar_host",
            "fact_name_prefix_domain": "",
            "fact_name_prefix_description": "",
            "fact_name_prefix_notes": "",
            "fact_name_prefix_url": "http://passwordstate",
            "fact_name_prefix_accounttype": "",
            "fact_name_prefix_accounttypeid": "",
            "fact_name_prefix_genericfield1": "123",
            "fact_name_prefix_genericfield2": "",
            "fact_name_prefix_genericfield3": "",
            "fact_name_prefix_genericfield4": "",
            "fact_name_prefix_genericfield5": "",
            "fact_name_prefix_genericfield6": "",
            "fact_name_prefix_genericfield7": "",
            "fact_name_prefix_genericfield8": "",
            "fact_name_prefix_genericfield9": "",
            "fact_name_prefix_genericfield10": "",
            "fact_name_prefix_expirydate": "2051-05-12",
        }
        self.maxDiff = None
        self.assertEqual(expected, facts)

    @mock.patch("requests.get", autospec=True)
    def test_gather_facts_field(self, mock_get):
        """gather facts by custom field"""
        value = [
            {
                "PasswordID": 998,
                "Password": "foo",
                "UserName": "foobar",
                "Title": "bar",
                "HostName": "foobar_host",
                "Domain": "",
                "Description": "",
                "Notes": "",
                "URL": "http://passwordstate",
                "AccountType": "",
                "AccountTypeID": "",
                "GenericField1": "123",
                "GenericField2": "",
                "GenericField3": "",
                "GenericField4": "",
                "GenericField5": "",
                "GenericField6": "",
                "GenericField7": "",
                "GenericField8": "",
                "GenericField9": "",
                "GenericField10": "",
                "GenericFieldInfo": "",
                "ExpiryDate": "2051-05-12",
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
            "fact_name_prefix_passwordid": 998,
            "fact_name_prefix_password": "foo",
            "fact_name_prefix_username": "foobar",
            "fact_name_prefix_title": "bar",
            "fact_name_prefix_hostname": "foobar_host",
            "fact_name_prefix_domain": "",
            "fact_name_prefix_description": "",
            "fact_name_prefix_notes": "",
            "fact_name_prefix_url": "http://passwordstate",
            "fact_name_prefix_accounttype": "",
            "fact_name_prefix_accounttypeid": "",
            "fact_name_prefix_genericfield1": "123",
            "fact_name_prefix_genericfield2": "",
            "fact_name_prefix_genericfield3": "",
            "fact_name_prefix_genericfield4": "",
            "fact_name_prefix_genericfield5": "",
            "fact_name_prefix_genericfield6": "",
            "fact_name_prefix_genericfield7": "",
            "fact_name_prefix_genericfield8": "",
            "fact_name_prefix_genericfield9": "",
            "fact_name_prefix_genericfield10": "",
            "fact_name_prefix_expirydate": "2051-05-12",
        }
        self.maxDiff = None
        self.assertEqual(expected, facts)
