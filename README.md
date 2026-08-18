[![Build Status](https://github.com/KBerstene/ansible-passwordstate-modules/actions/workflows/build.yml/badge.svg)](https://github.com/KBerstene/ansible-passwordstate-modules/actions/workflows/build.yml)

# Ansible Passwordstate Modules

This repository contains an Ansible collection for setting and getting Passwordstate passwords.

Original codebase credit to the [BoxUK modules](https://github.com/boxuk/ansible-boxuk-modules-passwordstate), with additional major contributions by [eizedev](https://github.com/eizedev/ansible-passwordstate-modules).

All Python prerequisites can be installed using `python3 -m pip install -r dev-requirements.txt`.

This collection is unaffiliated with ClickStudios and Passwordstate, and therefore it is not going to be published through Ansible Galaxy at this time.  It can be installed as a local collection using the following `ansible-galaxy` command:

```bash
ansible-galaxy collection install git+https://github.com/KBerstene/ansible-passwordstate-modules.git
```

## passwordstate.password module

The `passwordstate.password` module enables adding and updating of passwords inside Passwordstate:

```yml
---
- name: Passwordstate
  hosts: localhost
  connection: local
  tasks:
    - name: push password to passwordstate
      local.passwordstate.password:
        url: 'https://passwordstate.internal.corp.net'
        api_key: 'xxxxxxxxx'
        password_list_id: 'xxxx'
        match_field: 'GenericField1'
        match_field_id: 'xx'
        title: 'My password title'
        username: 'username'
        password: 'my secure password'
```

## local.passwordstate.password_fact

The `local.passwordstate.password_fact` module enables fetching of passwords stored in Passwordstate:

### Fetch by custom match field/id

```yml
---
- name: Passwordstate
  hosts: localhost
  connection: local
  tasks:
    - name: get password from passwordstate
      local.passwordstate.password_fact:
        url: 'https://passwordstate.internal.corp.net'
        api_key: 'xxxxxxxxx'
        password_list_id: 'xxxx'
        match_field: 'GenericField1'
        match_field_id: 'xx'
        fact_name: 'myaccount'
    - debug: var=myaccount_password
```

### Fetch by password id

```yml
---
- name: Passwordstate
  hosts: localhost
  connection: local
  tasks:
    - name: get password from passwordstate
      local.passwordstate.password_fact:
        url: 'https://passwordstate.internal.corp.net'
        api_key: 'xxxxxxxxx'
        password_id: 'xx'
        fact_name: 'myaccount'
    - debug: var=myaccount_username
    - debug: var=myaccount_password
```

## Windows Authentication API

Passwordstate offers an API that uses Windows authentication instead of standard API keys.  The Windows API can be used by simply replacing the `api_key` option with the `api_username` and `api_password` options, which can be prompted for at the beginning of a playbook or otherwise stored and passed:

```yml
---
- name: Passwordstate
  hosts: localhost
  connection: local
  tasks:
    - name: get password from passwordstate
    local.passwordstate.password_fact:
        url: 'https://passwordstate.internal.corp.net'
        api_username: '{{ passwordstate_api_username }}'
        api_password: '{{ passwordstate_api_password }}'
        password_id: 'xx'
        fact_name: 'myaccount'
    - debug: var=myaccount_username
    - debug: var=myaccount_password
```

## Output

If running `ansible-playbook` with `-vvv` the output, if using one of the examples from above, could be:

```yml
ok: [localhost] => {
    "ansible_facts": {
        "myaccount_accounttype": "Active Directory",
        "myaccount_accounttypeid": 64,
        "myaccount_description": "Test Description",
        "myaccount_domain": "",
        "myaccount_expirydate": "",
        "myaccount_genericfield1": "xx",
        "myaccount_genericfield10": "",
        "myaccount_genericfield2": "foobar",
        "myaccount_genericfield3": "",
        "myaccount_genericfield4": "",
        "myaccount_genericfield5": "",
        "myaccount_genericfield6": "",
        "myaccount_genericfield7": "",
        "myaccount_genericfield8": "None",
        "myaccount_genericfield9": "",
        "myaccount_genericfieldinfo": [
            {
                "DisplayName": "GenericField1",
                "GenericFieldID": "GenericField1",
                "Value": "xx"
            },
            {
                "DisplayName": "Test Field",
                "GenericFieldID": "GenericField2",
                "Value": "foobar"
            },
            {
                "DisplayName": "Test Field 2",
                "GenericFieldID": "GenericField8",
                "Value": "None"
            }
        ],
        "myaccount_hostname": "foobar_host",
        "myaccount_notes": "",
        "myaccount_password": "FooBar_Password1",
        "myaccount_passwordid": 999,
        "myaccount_title": "My password title",
        "myaccount_url": "https://passwordstate",
        "myaccount_username": "My password user"
    },
    "changed": false,
    "invocation": {
        "module_args": {
            "api_key": "xxxxxxxxx",
            "api_password": null,
            "api_username": null,
            "fact_name": "myaccount",
            "match_field": null,
            "match_field_id": null,
            "password_id": "999",
            "password_list_id": "2",
            "url": "https://passwordstate"
        }
    }
}
```
