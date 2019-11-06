<!--THIS FILE IS AUTOGENERATED: DO NOT EDIT-->
<!--See https://github.com/dimagi/commcare-cloud/blob/master/changelog/README.md for instructions-->
# 31. Update Formplayer Configuration

**Date:** 2019-11-06

**Optional per env:** _required on all environments_


## CommCare Version Dependency
This change is not known to be dependent on any particular version of CommCare.


## Change Context
There are some incompatible changes to the Formplayer configuration that will be required by
a later version of Formplayer.

## Details
Some of the configuration properties for Formplayer are changing and before that can be rolled out
the local config files need to be updated.

## Steps to update
```bash
$ commcare-cloud <env> update-config --limit formplayer
```