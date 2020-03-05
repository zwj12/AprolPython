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
        return requestsCookieJar
    except IOError:
        #pass
        return None

requestsCookieJar = load_cookies()
print requestsCookieJar
username = "Default User"
password = "robotics"
digest_auth = HTTPDigestAuth(username, password)
url = "http://{0}:{1}/ctrl".format("10.0.2.2", "8610")
#rqheaders = {"Connection":"close"}
#resp = requests.get(url, auth=digest_auth, headers=rqheaders, timeout=1)
resp = requests.get(url, auth=digest_auth, timeout=1)
if resp.status_code == 200:
    save_cookies(resp.cookies)
