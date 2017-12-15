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

fd = open('/var/lib/awx/job_status/testhost.txt', 'r')
content = fd.readlines()
fd.close()

raw_host = []
site_list = []

for unfilt_host in content:
    raw_host.append(unfilt_host.strip())

for item in raw_host:
    x = item.split("-")[0]
    if x not in site_list:
        site_list.append(x)

jsondict = {'_meta': {}}

jsondict['_meta']['hostvars'] = {}

for site in site_list:
    site_host = []
    for host in raw_host:
        if re.search(host.split("-")[0], site, re.IGNORECASE):
            site_host.append(host)
    jsondict[site] = site_host
print(json.dumps(jsondict, sort_keys=True, indent=2))