andrewrothstein.couchdb-cluster
===============================
[![Build Status](https://travis-ci.org/andrewrothstein/ansible-couchdb-cluster.svg?branch=master)](https://travis-ci.org/andrewrothstein/ansible-couchdb-cluster)

Configures a CouchDB cluster.

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
- hosts: couchdb
  roles:
    - andrewrothstein.couchdb-cluster
```

License
-------

MIT

Author Information
------------------

Andrew Rothstein <andrew.rothstein@gmail.com>
