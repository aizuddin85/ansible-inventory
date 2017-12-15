#!/usr/bin/env python
"""
Script to read flat file that contains host list.

The hostname convention like a-b-c0001. This script will take 'a' as the group
and populate host that has the same convention into the same dictionary.

['_meta']['hostvars'] kept empty so the awx inventory will not execute '--host' for host meta.
Refer http://docs.ansible.com/ansible/latest/dev_guide/developing_inventory.html for detail guide.

"""

import re
import json

FILENAME = '/var/lib/awx/job_status/testhost.txt'

"""
Read the FILENAME into memory.
"""
try:
    fd = open(FILENAME, 'r')
    content = fd.readlines()
    fd.close()
except IOError as err:
    raise err

"""
Initialized empty list for usage later.
"""
raw_host = []
group_list = []

"""
Read the fd content and populate into the raw_host list.
"""
for unfilt_host in content:
    raw_host.append(unfilt_host.strip())

"""
Process the raw_host and look for first field for group name. Populate the group_list.
"""
for item in raw_host:
    x = item.split("-")[0]
    if x not in group_list:
        group_list.append(x)
"""
Initialized dictionary that start with empty _meta and its child hostvars.
"""
jsondict = {'_meta': {}}
jsondict['_meta']['hostvars'] = {}

"""
Process host based on its group and produce json dump output that AWX inventory '--list' command
expected.
"""
for group in group_list:
    group_host = []
    for host in raw_host:
        if re.search(host.split("-")[0], group, re.IGNORECASE):
            group_host.append(host)
    jsondict[group] = group_host
print(json.dumps(jsondict, sort_keys=True, indent=2))
