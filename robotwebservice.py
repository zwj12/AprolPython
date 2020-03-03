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
    #__host = "10.0.2.2"
    #__port = 80
    #__timeout = 0.5
    #__username = "Default User"
    #__password = "robotics"
    #__session = None
    #__cookies = None
    #__ctrl = {}
    #__rw = {}

    def __init__(self, host="10.0.2.2", port=80, username="Default User", password="robotics", timeout=0.5):
        """Create Session and get the robot's overview information
        """
        self.init_data_structure()
        self.__host = host
        self.__port = port
        if timeout < 0.1:
            self.__timeout = 0.5
        else:
            self.__timeout = timeout
        self.__session = requests.Session()
        digest_auth = HTTPDigestAuth(username, password)
        # by xml format data
        url = "http://{0}:{1}/ctrl".format(self.__host, self.__port)
        resp = self.__session.get(url, auth=digest_auth, timeout=self.__timeout)
        self.__cookies = resp.cookies
        root = ET.fromstring(resp.text)
        if root.findall(".//{0}li[@class='ctrl-identity-info-li']".format(self.__namespace)):
            self.__ctrl["ctrl-name"] = root.find(
                ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-name']"
                .format(self.__namespace)).text
            self.__ctrl["ctrl-type"] = root.find(
                ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-type']"
                .format(self.__namespace)).text
            if self.__ctrl["ctrl-type"] == "Real Controller":
                self.__ctrl["ctrl-id"] = root.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-id']"
                    .format(self.__namespace)).text
        self.refresh_rw()
        self.refresh_data()

    def init_data_structure(self):
        """init_data_structure
        df
        """
        self.__ctrl = {}
        self.__rw = {"system":{}, "panel":{}, "iosystem":{}, "rapid":{}}
        self.__rw["iosystem"] = {"signals":{}}
        self.__rw["rapid"] = {"execution":{}}
        self.__symboldata = {"T_ROB1":{}}
        self.__symboldata["T_ROB1"] = {"user":{}}
        self.__root = {}
        self.__root["ctrl"] = self.__ctrl
        self.__root["rw"] = self.__rw
        self.__root["symboldata"] = self.__symboldata

    def refresh_rw(self):
        """
        The response data format is json.
        """
        # For json format data
        #url = "http://{0}:{1}/rw/system?json=1".format(self.__host, self.__port)
        #resp = self.__session.get(url, cookies=self.__cookies, timeout=self.__timeout)
        #obj = json.loads(resp.text)
        #self.__rw["system_name"] = obj["_embedded"]["_state"][0]["name"]
        #self.__rw["rw_version"] = obj["_embedded"]["_state"][0]["rwversion"]
        #self.__rw["sysid"] = obj["_embedded"]["_state"][0]["sysid"]
        #self.__rw["system_name"] = self.get_rws_resource("rw/system", "name")

        self.refresh_rws_resources("rw/system", \
            ("name", "sysid", "rwversion", "starttm"), \
            self.__rw["system"])
        self.refresh_rws_resources("rw/system/robottype", ("robot-type",), self.__rw["system"])
        self.refresh_rws_resources("rw/system/options", ("option",), self.__rw["system"])
        #self.__rw["panel"]["ctrlstate"] = self.get_rws_resource("rw/panel/ctrlstate", "ctrlstate")
        #self.__rw["panel"]["opmode"] = self.get_rws_resource("rw/panel/opmode", "opmode")
        #self.__rw["panel"]["speedratio"] = \
        #    self.get_rws_resource("rw/panel/speedratio", "speedratio")
        self.refresh_rws_resources(\
            ("rw/panel/ctrlstate", "rw/panel/opmode", "rw/panel/speedratio"), \
            ("ctrlstate", "opmode", "speedratio"), \
            self.__rw["panel"])
        self.refresh_rws_resources("rw/rapid/execution", \
            ("ctrlexecstate", "cycle"), self.__rw["rapid"]["execution"])
        self.refresh_signals(self.__rw["iosystem"]["signals"])

    def refresh_data(self):
        """refresh_symboldata
        """
        self.__symboldata["T_ROB1"]["user"].update(self.get_rws_symbol_data(\
            "T_ROB1", "user", "reg1"))
        self.__symboldata["T_ROB1"]["user"].update(self.get_rws_symbol_data(\
            "T_ROB1", "user", ("reg2", "reg3", "reg4", "reg5")))

    def refresh_signals(self, signals):
        """refresh_signals
        """
        url = "http://{0}:{1}/rw/iosystem/signals?json=1".format(self.__host, self.__port)
        resp = self.__session.get(url, cookies=self.__cookies, timeout=self.__timeout)
        obj = json.loads(resp.text)
        for state in obj["_embedded"]["_state"]:
            #signals[state["name"]] = {}
            #signals[state["name"]]["name"] = state["name"]
            #signals[state["name"]]["type"] = state["type"]
            #signals[state["name"]]["lvalue"] = state["lvalue"]
            signals[state["name"]] = state

    def get_rws_resource(self, resource, key):
        """get_rws_resource
        """
        url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resource)
        resp = self.__session.get(url, cookies=self.__cookies, timeout=self.__timeout)
        obj = json.loads(resp.text)
        return obj["_embedded"]["_state"][0][key]

    def refresh_rws_resources(self, resources, keys, values):
        """refresh_rws_resources
        """
        if isinstance(resources, tuple):
            for resource, key in zip(resources, keys):
                url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resource)
                resp = self.__session.get(url, cookies=self.__cookies, timeout=self.__timeout)
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
            url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resources)
            resp = self.__session.get(url, cookies=self.__cookies, timeout=self.__timeout)
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

    def get_rws_symbol_data(self, task, module, names):
        """get_rws_symbol_data
        """
        sysbols = {}
        if isinstance(names, tuple):
            for name in names:
                url = "http://{0}:{1}/rw/rapid/symbol/data/RAPID/{2}/{3}/{4}?json=1"\
                    .format(self.__host, self.__port, task, module, name)
                resp = self.__session.get(url, cookies=self.__cookies, timeout=self.__timeout)
                obj = json.loads(resp.text)
                sysbols[name] = obj["_embedded"]["_state"][0]["value"]
        else:
            url = "http://{0}:{1}/rw/rapid/symbol/data/RAPID/{2}/{3}/{4}?json=1"\
                .format(self.__host, self.__port, task, module, names)
            resp = self.__session.get(url, cookies=self.__cookies, timeout=self.__timeout)
            obj = json.loads(resp.text)
            sysbols[names] = obj["_embedded"]["_state"][0]["value"]
        return sysbols

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

    def get_session(self):
        """RobotWebService

        """
        if self.__session is None:
            raise Exception("No Session!")
        else:
            return self.__session

    def get_cookies(self):
        """RobotWebService

        """
        if self.__cookies is None:
            raise Exception("No Cookies!")
        else:
            return self.__cookies

    def get_root(self):
        """RobotWebService

        """
        return self.__root

    def get_ctrl(self):
        """RobotWebService

        """
        return self.__ctrl

    def get_rw(self):
        """RobotWebService

        """
        return self.__rw

    def get_symboldata(self):
        """RobotWebService

        """
        return self.__symboldata

    def close_session(self):
        """RobotWebService

        """
        self.__session.close()

    def show_tree(self, vars, layer, max_layer=3):
        """RobotWebService

        """
        if isinstance(vars, dict):
            for key, value in vars.items():
                if layer==1:
                    print ("|___" + key)
                elif layer<=max_layer:
                    print ("    "* (layer-1) + "|___"  + key)
                self.show_tree(value, layer+1, max_layer)


def main(argv):
    """RobotWebService

    """
    print (argv)
    try:
        web_service = RobotWebService(host="10.0.2.2", port=8610, timeout=1)
        #web_service = WebService(port=8610, timeout=0.001)
        print (web_service.get_ctrl())
        #lists = {"one1":{}, "one2":{"two1":{},"two2":{}}, "one3":{"two1":{"three1":{},"three2":{}},"two2":{}}}
        web_service.show_tree(web_service.get_root(), 1)
        #print (web_service.get_rw())
        #print (web_service.get_rw()["system"])
        #print (web_service.get_symboldata())
        web_service.close_session()
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
