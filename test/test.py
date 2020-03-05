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
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)
    lwpCookieJar = cookielib.LWPCookieJar(filename="robot_10.0.2.2.txt")
    lwpCookieJar = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=lwpCookieJar, overwrite=True)
    lwpCookieJar.save(ignore_discard=True)
    print "save_cookies"
    print cookies_dict
    print lwpCookieJar

def load_cookies():
    try:
        lwpCookieJar = cookielib.LWPCookieJar(filename="robot_10.0.2.2.txt")
        lwpCookieJar.load(ignore_discard=True)
        cookies_dict = requests.utils.dict_from_cookiejar(lwpCookieJar)
        cookies = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
        print "load_cookies"
        print lwpCookieJar
        print cookies_dict
        print cookies
        return cookies
    except IOError:
        return None

username = "Default User"
password = "robotics"
digest_auth = HTTPDigestAuth(username, password)
session = requests.Session()
print session.cookies
#load_cookies(session)
# by xml format data
url = "http://{0}:{1}/ctrl".format("10.0.2.2", "8610")
resp = session.get(url, auth=digest_auth, timeout=1)
print resp.status_code
print resp.headers
print resp.cookies
print session.cookies
print session.cookies.items()
print session.cookies.get_dict()
print session.cookies.list_domains()
print session.cookies.list_paths()
save_cookies(session.cookies)
