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
    cookies_dict = cookies.get_dict()
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
        print "lwpCookieJar"
        print lwpCookieJar
        new_cj =  requests.cookies.RequestsCookieJar()
        for cookie in lwpCookieJar:
            print cookie
            new_cj.set_cookie(cookie)
        print new_cj
        print "end"
        cookies_dict = requests.utils.dict_from_cookiejar(lwpCookieJar)
        cookiejar = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
        print "merge"
        new_cj =  requests.cookies.RequestsCookieJar()
        for (key, value) in cookies_dict.items():
            cookie = requests.cookies.create_cookie(name=key, value=value, domain=".10.0.2.2")
            print cookie
            #requests.cookies.remove_cookie_by_name(cookiejar, key)
            #print cookiejar
            #new_cj = requests.cookies.merge_cookies(new_cj, cookie)
            new_cj.set(name=key, value=value, domain=".10.0.2.2")
            print new_cj
        print "load_cookies"
        for cookie in new_cj:
            print cookie
            for value in cookie:
                print value
        print lwpCookieJar
        print cookies_dict
        print cookiejar
        return cookiejar
    except IOError:
        #pass
        return None

load_cookies()
username = "Default User"
password = "robotics"
digest_auth = HTTPDigestAuth(username, password)
url = "http://{0}:{1}/ctrl".format("10.0.2.2", "8610")
#rqheaders = {"Connection":"close"}
#resp = requests.get(url, auth=digest_auth, headers=rqheaders, timeout=1)
resp = requests.get(url, auth=digest_auth, timeout=1)
print resp.request.headers
print resp.status_code
print resp.headers
print resp.cookies
print resp.cookies.items()
print resp.cookies.get_dict()
print resp.cookies.list_domains()
print resp.cookies.list_paths()
save_cookies(resp.cookies)
