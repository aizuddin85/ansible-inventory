#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)
import xmlrpclib
import re
import json

# Declare the satellite info and the hostname search string that containt SEARCHFOR sting.
SATELLITE_URL = "http://rhns.example.com/rpc/api"
SATELLITE_LOGIN = "admin"
SATELLITE_PASSWORD = "PASSWORD_HERE"
SEARCHFOR = 'houston-linux'

# Connect to satellite, query the system namespace for listActiveSystem and populate the host into the host_list.
host_list = []
client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(SATELLITE_LOGIN, SATELLITE_PASSWORD)
host =  client.system.listActiveSystems(key)
client.auth.logout(key)

# Filter the host for the host we are looking for and populate into the host_list list.
for item in host:
    hostname = item['name']
        if re.search(SEARCHFOR, hostname, re.IGNORECASE):
            host_list.append(hostname)

invdict = {'_meta' : {}}
invdict['_meta']['hostvars'] = {}
invdict[SEARCHFOR] = host_list

# Print json dump.
print(json.dumps(invdict, sort_keys=True, indent=2))


