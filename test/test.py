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

def save_cookies(cookies):
    lwpCookieJar = cookielib.LWPCookieJar(filename="robot_10.0.2.2.txt")
    for cookie in cookies:
        lwpCookieJar.set_cookie(cookie)
    print "save_cookies:"
    print lwpCookieJar
    lwpCookieJar.save(ignore_discard=True)

def load_cookies():
    try:
        lwpCookieJar = cookielib.LWPCookieJar(filename="robot_10.0.2.2.txt")
        lwpCookieJar.load(ignore_discard=True)
        requestsCookieJar = requests.cookies.RequestsCookieJar()
        for cookie in lwpCookieJar:
            #requestsCookieJar.set(name=cookie.name, value=cookie.value, domain=".10.0.2.2")
            requestsCookieJar.set_cookie(cookie)
        print "load_cookies:"
        print requestsCookieJar
        return requestsCookieJar
    except IOError:
        #pass
        return None

requestsCookieJar = load_cookies()
username = "Default User"
password = "robotics"
digest_auth = HTTPDigestAuth(username, password)
session = requests.Session()
session.cookies = requestsCookieJar
url = "http://{0}:{1}/ctrl".format("10.0.2.2", "8610")
resp = session.get(url, timeout=1)
print resp.status_code
if resp.status_code == 401:
    print "Unauthorized (401)"
    resp = session.get(url, auth=digest_auth, timeout=1)
    print resp.status_code
    if resp.status_code == 200:
        save_cookies(session.cookies)
print "resp.cookies"
print resp.cookies
print "session.cookies"
print session.cookies
#print resp.text
session.close()
