#!/usr/bin/python
# -*- coding: utf-8 -*-

"""RobotWebService
chmod a+x we*

"""

import sys
import json
import xml.etree.ElementTree as ET
from requests.auth import HTTPDigestAuth
import requests
import cookielib

class RobotWebService(object):
    """RobotWebService
    The subset of RobotWebService is similar of web services resources
    which is described at http://developercenter.robotstudio.com/webservice/api_reference
    |___rw
        |___rapid
            |___execution
        |___iosystem
            |___signals
        |___system
            |___option
            |___robot-type
            |___sysid
            |___starttm
            |___rwversion
            |___name
        |___panel
            |___speedratio
            |___opmode
            |___ctrlstate
    |___symboldata
        |___T_ROB1
            |___user
    |___ctrl
        |___ctrl-name
        |___ctrl-type
    """
    __namespace = '{http://www.w3.org/1999/xhtml}'

    def __init__(self, host="10.0.2.2", port=80, username="Default User", password="robotics", timeout=0.5):
        """Create Session and get the robot's overview information
        """
        self.__host = host
        self.__port = port
        self.__digest_auth = HTTPDigestAuth(username, password)
        self.__timeout = timeout
        if self.__timeout < 0.1:
            self.__timeout = 0.5
        self.__session = None

        self.__root = {"ctrl":{}, "rw":{}, "symboldata":{}}
        self.__root["rw"] = {"panel":{}, "rapid":{}, "system":{}, "iosystem":{}}
        self.__root["rw"]["rapid"] = {"execution":{}}
        self.__root["rw"]["iosystem"] = {"signals":{}}
        self.__root["symboldata"] = {"T_ROB1":{}}
        self.__root["symboldata"]["T_ROB1"] = {"user":{}}

    def get_session(self):
        """RobotWebService

        """
        if self.__session is None:
            self.__session = requests.Session()
            self.load_cookies()
            # by xml format data
            url = "http://{0}:{1}/ctrl".format(self.__host, self.__port)
            resp = self.__session.get(url, timeout=self.__timeout)
            if resp.status_code==401:
                self.__session.cookies = requests.cookies.RequestsCookieJar()
                resp = self.__session.get(url, auth=self.__digest_auth, timeout=self.__timeout)
                if resp.status_code == 200:
                    self.save_cookies()
            if resp.status_code == 200:
                xml_response = ET.fromstring(resp.text)
                if xml_response.findall(".//{0}li[@class='ctrl-identity-info-li']".format(self.__namespace)):
                    self.__root["ctrl"]["ctrl-name"] = xml_response.find(
                        ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-name']"
                        .format(self.__namespace)).text
                    self.__root["ctrl"]["ctrl-type"] = xml_response.find(
                        ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-type']"
                        .format(self.__namespace)).text
                    if self.__root["ctrl"]["ctrl-type"] == "Real Controller":
                        self.__root["ctrl"]["ctrl-id"] = xml_response.find(
                            ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-id']"
                            .format(self.__namespace)).text
            else:
                raise Exception("status_code: " + str(resp.status_code))
        return self.__session

    def close_session(self):
        """RobotWebService

        """
        if self.__session is not None:
            self.__session.close()

    def save_cookies(self):
        """save_cookies

        """
        lwpCookieJar = cookielib.LWPCookieJar(filename="robot_" + self.__host + ".txt")
        for cookie in self.__session.cookies:
            lwpCookieJar.set_cookie(cookie)
        lwpCookieJar.save(ignore_discard=True)

    def load_cookies(self):
        """load_cookies

        """
        try:
            lwpCookieJar = cookielib.LWPCookieJar(filename="robot_" + self.__host + ".txt")
            lwpCookieJar.load(ignore_discard=True)
            #requestsCookieJar = requests.cookies.RequestsCookieJar()
            for cookie in lwpCookieJar:
                #requestsCookieJar.set(name=cookie.name, value=cookie.value, domain=".10.0.2.2")
                self.__session.cookies.set_cookie(cookie)
        except IOError:
            pass

    def refresh_priority_low(self):
        try:
            self.refresh_rws_resources("rw/system", \
                ("name", "sysid", "rwversion", "starttm"), \
                self.__root["rw"]["system"])
            self.refresh_rws_resources("rw/system/robottype", ("robot-type",), self.__root["rw"]["system"])
            self.refresh_rws_resources("rw/system/options", ("option",), self.__root["rw"]["system"])
            return True
        except Exception:
            self.__session = None
            return False

    def refresh_priority_medium(self):
        try:
            self.__root["symboldata"]["T_ROB1"]["user"].update(self.get_rws_symbol_data(\
                "T_ROB1", "user", "reg1"))
            self.__root["symboldata"]["T_ROB1"]["user"].update(self.get_rws_symbol_data(\
                "T_ROB1", "user", ("reg2", "reg3", "reg4", "reg5")))
            return True
        except Exception, var:
            self.__session = None
            print var
            return False

    def refresh_priority_high(self):
        try:
            self.refresh_rws_resources(\
                ("rw/panel/ctrlstate", "rw/panel/opmode", "rw/panel/speedratio"), \
                ("ctrlstate", "opmode", "speedratio"), \
                self.__root["rw"]["panel"])
            self.refresh_rws_resources("rw/rapid/execution", \
                ("ctrlexecstate", "cycle"), self.__root["rw"]["rapid"]["execution"])
            self.refresh_signals(self.__root["rw"]["iosystem"]["signals"])
            return True
        except Exception:
            self.__session = None
            return False

    def refresh_signals(self, signals):
        """refresh_signals
        """
        self.get_session()
        url = "http://{0}:{1}/rw/iosystem/signals?json=1".format(self.__host, self.__port)
        resp = self.__session.get(url, timeout=self.__timeout)
        if resp.status_code==200:
            obj = json.loads(resp.text)
            for state in obj["_embedded"]["_state"]:
                #signals[state["name"]] = {}
                #signals[state["name"]]["name"] = state["name"]
                #signals[state["name"]]["type"] = state["type"]
                #signals[state["name"]]["lvalue"] = state["lvalue"]
                signals[state["name"]] = state
        else:
            raise Exception("status_code: " + str(resp.status_code))

    def refresh_rws_resources(self, resources, keys, values):
        """refresh_rws_resources
        """
        self.get_session()
        if isinstance(resources, tuple):
            for resource, key in zip(resources, keys):
                url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resource)
                resp = self.__session.get(url, timeout=self.__timeout)
                if resp.status_code==200:
                    obj = json.loads(resp.text)
                    state_values = []
                    for state in obj["_embedded"]["_state"]:
                        if key in state:
                            state_values.append(state[key])
                    if len(state_values) == 1:
                        values[key] = state_values[0]
                    else:
                        values[key] = state_values
                else:
                    raise Exception("status_code: " + str(resp.status_code))
        else:
            url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resources)
            resp = self.__session.get(url, timeout=self.__timeout)
            if resp.status_code==200:
                obj = json.loads(resp.text)
                for key in keys:
                    #values[key] = obj["_embedded"]["_state"][0][key]
                    state_values = []
                    for state in obj["_embedded"]["_state"]:
                        if key in state:
                            state_values.append(state[key])
                    if len(state_values) == 1:
                        values[key] = state_values[0]
                    else:
                        values[key] = state_values
            else:
                raise Exception("status_code: " + str(resp.status_code))

    def get_rws_symbol_data(self, task, module, names):
        """get_rws_symbol_data
        """
        self.get_session()
        sysbols = {}
        if isinstance(names, tuple):
            for name in names:
                url = "http://{0}:{1}/rw/rapid/symbol/data/RAPID/{2}/{3}/{4}?json=1"\
                    .format(self.__host, self.__port, task, module, name)
                resp = self.__session.get(url, timeout=self.__timeout)
                if resp.status_code==200:
                    obj = json.loads(resp.text)
                    sysbols[name] = obj["_embedded"]["_state"][0]["value"]
                else:
                    raise Exception("status_code: " + str(resp.status_code))
        else:
            url = "http://{0}:{1}/rw/rapid/symbol/data/RAPID/{2}/{3}/{4}?json=1"\
                .format(self.__host, self.__port, task, module, names)
            resp = self.__session.get(url, timeout=self.__timeout)
            if resp.status_code==200:
                obj = json.loads(resp.text)
                sysbols[names] = obj["_embedded"]["_state"][0]["value"]
            else:
                raise Exception("status_code: " + str(resp.status_code))
        return sysbols

    def get_rws_resource(self, resource, key):
        """get_rws_resource
        """
        self.get_session()
        url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resource)
        resp = self.__session.get(url, timeout=self.__timeout)
        if resp.status_code==200:
            obj = json.loads(resp.text)
            return obj["_embedded"]["_state"][0][key]
        else:
            raise Exception("status_code: " + str(resp.status_code))

    def get_host(self):
        """RobotWebService

        """
        if self.__host is None:
            raise Exception("No Host!")
        else:
            return self.__host

    def get_port(self):
        """RobotWebService

        """
        if self.__port is None:
            raise Exception("No Port!")
        else:
            return self.__port

    def get_root(self):
        """RobotWebService

        """
        return self.__root

    def show_tree(self, vars, layer, max_layer=3):
        """RobotWebService

        """
        if isinstance(vars, dict):
            for key, value in vars.items():
                if layer==1:
                    print ("|___" + key)
                    #print (u"└───" + key)
                elif layer<=max_layer:
                    print ("    "* (layer-1) + "|___"  + key)
                    #print ("    "* (layer-1) + u"└───"  + key)
                self.show_tree(value, layer+1, max_layer)


def main(argv):
    """RobotWebService

    """
    #print (argv)
    try:
        web_service = RobotWebService(host="10.0.2.2", port=8610, timeout=1)
        result = web_service.refresh_priority_high()
        result = web_service.refresh_priority_medium()
        result = web_service.refresh_priority_low()
        web_service.close_session()
        print (web_service.get_root())
        if result:
            web_service.show_tree(web_service.get_root(), 1)
            pass
    except requests.ConnectionError:
        print ("ConnectionError")
    except requests.Timeout:
        print ("TimeoutError")
    except requests.RequestException, var:
        print (var)
    #except Exception, var:
        #print (var)
#    finally:
#       web_service.close_session()

if __name__ == "__main__":
    main(sys.argv[1:])
else:
    pass
