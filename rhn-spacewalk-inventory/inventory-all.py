#!/usr/bin/python
# The inventory will be executed with --list and --host argument.
# In this script, those argument will be ignored.
# -*- coding:utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
import xmlrpclib
import re
import json

# Get Satellite API endpoint and creds.
SATELLITE_URL = "http://rhns.example.com/rpc/api"
SATELLITE_LOGIN = "rhnadmin"
SATELLITE_PASSWORD = "PASSWORD_HERE"

# Initialized list for processing later.
host_list = []
group_list = []
nogroup_host_list = []

# Connect to satellite, query the system namespace for listActiveSystem and populate the host into the host_list.
client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
host =  client.system.listActiveSystems(key)
for item in host:
    hostname = item['name']
    host_list.append(hostname)
client.auth.logout(key)

# Filter the group name based on the site name. If the server using non-standard convention without a-b-x00001, populate
# into nogroup_host_list.
for item in host_list:
    if re.search("-", item, re.IGNORECASE):
        x = item.split("-")[0]
        if x not in group_list:
            group_list.append(x)
    else:
        nogroup_host_list.append(item)

# Initialized dictionary for json dump. hostvars used to avoid of --host executed for each host. This can cause penalty
# on how long the inventory script to be completed since it will query each host for it metainfo.
invdict = {'_meta' : {}}
invdict['_meta']['hostvars'] = {}

# Populate host into particular group.
for grp in group_list:
    group_host = []
    for host in host_list:
        if re.search(host.split("-")[0], grp, re.IGNORECASE):
            group_host.append(host)
    invdict[grp] = group_host
invdict['no_distinct_group'] = nogroup_host_list

# Print the result in json format for inventory to read.
print(json.dumps(invdict, sort_keys=True, indent=2))


