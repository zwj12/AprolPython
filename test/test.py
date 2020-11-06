#!/usr/bin/python
# -*- coding: utf-8 -*-

"""testwebservice
chmod a+x te*

"""

import sys
import json
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth
import requests
import cookielib

a = {2:"x", 1:"y"}

print a.keys()
print type(a.keys())
c = a.keys()
c.sort()
print c
for value in a.values():
    print value
