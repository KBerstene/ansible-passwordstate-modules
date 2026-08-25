#!/usr/bin/python3

""" PasswordState Ansible Action Plugin """

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase

import requests
from json.decoder import JSONDecodeError
from requests_ntlm import HttpNtlmAuth


class PasswordIdException(Exception):
    msg = "Either the password id or the match " "field id and value must be configured"


class Password(object):
    """Password"""

    def __init__(self, api, password_list_id, matcher):
        self.api = api
        self.password_list_id = password_list_id
        if "id" in matcher and matcher["id"] != None:
            self.password_id = matcher["id"]
        elif (
            "field" in matcher
            and "field_id" in matcher
            and matcher["field"] != None
            and matcher["field_id"] != None
        ):
            self.match_field = matcher["field"]
            self.match_field_id = matcher["field_id"]
        else:
            raise PasswordIdException()

    @property
    def password(self):
        """fetch the password from the api"""
        return self.api.get_password_fields(self)["Password"]

    @property
    def type(self):
        """the method to uniquely identify the password"""
        if hasattr(self, "password_id"):
            return "password_id"
        elif hasattr(self, "match_field") and hasattr(self, "match_field_id"):
            return "match_field"
        raise PasswordIdException()

    def update(self, fields):
        """Update the password"""
        return self.api.update(self, fields)


class PasswordState(object):
    """PasswordState"""

    def __init__(self, url, api_key, api_username=None, api_password=None):
        self.url = url
        self.api_key = api_key
        self.api_username = api_username
        self.api_password = api_password

    def update(self, password, fields):
        """update the password in PasswordState"""
        if self._password_match(password, fields):
            return False

        if password.type == "password_id":
            params = {
                "PasswordID": password.password_id,
                "PasswordListID": password.password_list_id,
            }
            params = PasswordState._merge_dicts(fields, params)

            self._request("passwords", "PUT", params)
        elif password.type == "match_field":
            if self._has_password(password):
                pid = self._get_password_id(password)

                params = {
                    "PasswordID": pid,
                    "PasswordListID": password.password_list_id,
                }
                params = PasswordState._merge_dicts(fields, params)

                self._request("passwords", "PUT", params)
            else:
                if not "Title" in fields:
                    raise AnsibleActionFail("Title is required when creating passwords")

                params = {
                    "PasswordListID": password.password_list_id,
                    password.match_field: password.match_field_id,
                }
                params = PasswordState._merge_dicts(fields, params)

                self._request("passwords", "POST", params)

        return True

    def get_password_fields(self, password):
        """get the password fields"""
        if password.type == "password_id":
            return self._get_password_by_id(password.password_id)
        elif password.type == "match_field":
            return self._get_password_by_field(password)

    def _get_password_by_id(self, password_id):
        """get the password by the password id"""
        passwords = self._request("passwords/" + str(password_id), "GET")
        if len(passwords) == 0:
            raise AnsibleActionFail("Password not found")
        if len(passwords) > 1:
            raise AnsibleActionFail("Multiple matching passwords found")
        return passwords[0]

    def _get_password_by_field(self, password):
        """get the password by a specific field"""
        return self._get_password_by_id(self._get_password_id(password))

    def _get_password_id(self, password):
        """get the password id by using a specific field"""
        uri = (
            "passwords/" + password.password_list_id + "?QueryAll&ExcludePassword=true"
        )
        passwords = self._request(uri, "GET")
        passwords = PasswordState._filter_passwords(
            passwords, password.match_field, password.match_field_id
        )
        if len(passwords) == 0:
            raise AnsibleActionFail("Password not found")
        elif len(passwords) > 1:
            raise AnsibleActionFail("Multiple matching passwords found")

        return passwords[0]["PasswordID"]

    def _has_password(self, password):
        """checks if the password exists"""
        if password.type == "password_id":
            uri = "passwords/" + password.password_id
            passwords = self._request(uri, "GET")
            if len(passwords) == 0:
                return False
            return True
        elif password.type == "match_field":
            plid = password.password_list_id
            uri = "passwords/" + plid + "?QueryAll&ExcludePassword=true"
            passwords = self._request(uri, "GET")
            passwords = PasswordState._filter_passwords(
                passwords, password.match_field, password.match_field_id
            )

            if len(passwords) == 1:
                return True
            elif len(passwords) > 1:
                raise AnsibleActionFail("Multiple matching passwords found")
            return False

    def _password_match(self, password, fields):
        """checks if the password entity is up to date"""
        match = True
        if self._has_password(password):
            current_password = self.get_password_fields(password)
            if (
                "password" in fields
                and current_password["Password"] != fields["password"]
            ):
                match = False
            if "Title" in fields and current_password["Title"] != fields["Title"]:
                match = False
            if (
                "UserName" in fields
                and current_password["UserName"] != fields["UserName"]
            ):
                match = False
        else:
            match = False
        return match

    def _request(self, uri, method, params=None):
        """send a request to the api and return as json"""
        request_methods = {
            "GET": requests.get,
            "PUT": requests.put,
            "POST": requests.post,
        }

        try:
            if self.api_key != None:
                full_uri = self.url + "/api/" + uri
                headers = {"APIKey": self.api_key}
                response = request_methods[method](
                    full_uri, headers=headers, params=params
                )
            else:
                full_uri = self.url + "/winapi/" + uri
                winauth = HttpNtlmAuth(self.api_username, self.api_password)
                response = request_methods[method](
                    full_uri, auth=winauth, params=params
                )
        except requests.exceptions.RequestException as inst:
            raise AnsibleActionFail("Failed: %s" % str(inst))

        if response.status_code > 204:
            raise AnsibleActionFail("Failed: %s" % str(response.json()))

        try:
            return response.json()
        except JSONDecodeError as inst:
            raise AnsibleActionFail("Failed: %s" % str(inst))

    @staticmethod
    def _filter_passwords(passwords, field, value):
        """filter out passwords which does not match the specific field value"""
        return [obj for i, obj in enumerate(passwords) if obj[field] == value]

    @staticmethod
    def _merge_dicts(xray, yankee):
        """merge two dicts"""
        zulu = xray.copy()
        zulu.update(yankee)
        return zulu

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        validation_result, new_module_args = self.validate_argument_spec(
            argument_spec={
                "state": {"default": "present", "choices": ["present"]},
                "url": {"required": True},
                "api_key": {"required": False},
                "api_username": {"required": False},
                "api_password": {"required": False},
                "password_list_id": {"required": False},
                "match_field": {"required": False},
                "match_field_id": {"required": False},
                "password_id": {"required": False},
                "username": {"required": False},
                "password": {"required": False},
                "title": {"required": False},
            },
            mutually_exclusive=[("api_key", "api_username")],
            required_one_of=[("api_key", "api_username")],
            required_together=[("api_username", "api_password")],
        )

        state = new_module_args["state"]
        url = new_module_args["url"]
        api_key = new_module_args["api_key"]
        api_username = new_module_args["api_username"]
        api_password = new_module_args["api_password"]
        password_list_id = new_module_args["password_list_id"]
        match_field = new_module_args["match_field"]
        match_field_id = new_module_args["match_field_id"]
        password_id = new_module_args["password_id"]
        username = new_module_args["username"]
        new_password = new_module_args["password"]
        title = new_module_args["title"]

        api = PasswordState(url, api_key, api_username, api_password)
        password = Password(
            api,
            password_list_id,
            {"id": password_id, "field": match_field, "field_id": match_field_id},
        )

        fields = {}
        if title != None:
            fields["Title"] = title
        if username != None:
            fields["UserName"] = username
        if password != None:
            fields["password"] = new_password

        if state == "present":
            result["changed"] = password.update(fields)

        return result
