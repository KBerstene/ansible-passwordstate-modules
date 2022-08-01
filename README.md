[![Build Status](https://github.com/KBerstene/ansible-passwordstate-modules/actions/workflows/build.yml/badge.svg)](https://github.com/KBerstene/ansible-passwordstate-modules/actions/workflows/build.yml)

# Ansible PasswordState Modules

This repository contains two ansible modules for
setting and getting passwordstate passwords.

It has been rebuilt from the original [BoxUK modules](https://github.com/boxuk/ansible-boxuk-modules-passwordstate)
to run on Python 3, use the `requests` library in place of `urllib`, and add functionality for using the Windows Authentication API.

All Python prerequisites can be installed using `python3 -m pip install -r dev-requirements.txt`.

## passwordstate_password

The `passwordstate_password` module enables adding and updating of passwords inside PasswordState:

```yml
---
- name: Passwordstate
  hosts: localhost
  connection: local
  tasks:
    - name: push password to passwordstate
      passwordstate_password:
        url: 'https://passwordstate.internal.corp.net'
        api_key: 'xxxxxxxxx'
        password_list_id: 'xxxx'
        match_field: 'GenericField1'
        match_field_id: 'xx'
        title: 'My password title'
        username: 'username'
        password: 'my secure password'
```

## passwordstate_password_fact

The `passwordstate_password_fact` module enables fetching of passwords stored in PasswordState:

### Fetch by custom match field/id

```yml
---
- name: Passwordstate
  hosts: localhost
  connection: local
  tasks:
    - name: get password from passwordstate
      passwordstate_password_fact:
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
      passwordstate_password_fact:
        url: 'https://passwordstate.internal.corp.net'
        api_key: 'xxxxxxxxx'
        password_id: 'xx'
        fact_name: 'myaccount'
    - debug: var=myaccount_username
    - debug: var=myaccount_password
```

## Windows Authentication API

PasswordState offers an API that uses Windows authentication instead of standard API keys.  The Windows API can be used by simply replacing the `api_key` option with the `api_username` and `api_password` options, which can be prompted for at the beginning of a playbook or otherwise stored and passed:

```yml
---
- name: Passwordstate
  hosts: localhost
  connection: local
  tasks:
    - name: get password from passwordstate
    passwordstate_password_fact:
        url: 'https://passwordstate.internal.corp.net'
        api_username: '{{ passwordstate_api_username }}'
        api_password: '{{ passwordstate_api_password }}'
        password_id: 'xx'
        fact_name: 'myaccount'
    - debug: var=myaccount_username
    - debug: var=myaccount_password
```
