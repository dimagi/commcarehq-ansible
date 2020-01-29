andrewrothstein.gcc-toolbox
=========
[![Build Status](https://travis-ci.org/andrewrothstein/ansible-gcc-toolbox.svg?branch=master)](https://travis-ci.org/andrewrothstein/ansible-gcc-toolbox)

[GCC](https://gcc.gnu.org/) tools

Requirements
------------

See [meta/main.yml](meta/main.yml)

Role Variables
--------------

See [defaults/main.yml](defaults/main.yml)

Dependencies
------------

See [meta/main.yml](meta/main.yml)

Example Playbook
----------------

```yml
- hosts: servers
  roles:
    - andrewrothstein.gcc-toolbox
```

License
-------

MIT

Author Information
------------------

Andrew Rothstein <andrew.rothstein@gmail.com>
