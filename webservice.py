#!/usr/bin/python
# -*- coding: utf-8 -*-

"""RobotWebService
chmod a+x we*

"""

import sys
import json
import xml.etree.ElementTree as ET
import logging
from requests.auth import HTTPDigestAuth
import requests
#from aprolpython.robotresource import RobotResource


class WebService(object):
    """RobotWebService

    """
    __namespace = '{http://www.w3.org/1999/xhtml}'
    #__host = "10.0.2.2"
    #__port = 80
    #__username = "Default User"
    #__password = "robotics"
    #__session = None
    #__cookies = None
    #__ctrl = {}
    #__rw = {}

    def __init__(self, host="10.0.2.2", port=80, username="Default User", password="robotics"):
        """Create Session and get the robot's overview information
        """
        self.__host = host
        self.__port = port
        self.__session = requests.Session()
        digest_auth = HTTPDigestAuth(username, password)
        # by xml format data
        url = "http://{0}:{1}/ctrl".format(self.__host, self.__port)
        resp = self.__session.get(url, auth=digest_auth)
        self.__cookies = resp.cookies
        root = ET.fromstring(resp.text)
        self.__ctrl = {}
        self.__rw = {}
        if "system" not in self.__rw:
            self.__rw["system"] = {}
        if "panel" not in self.__rw:
            self.__rw["panel"] = {}
        if "rapid" not in self.__rw:
            self.__rw["rapid"] = {}
        if "execution" not in self.__rw["rapid"]:
            self.__rw["rapid"]["execution"] = {}

        if root.findall(".//{0}li[@class='ctrl-identity-info-li']".format(self.__namespace)):
            self.__ctrl["name"] = root.find(
                ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-name']"
                .format(self.__namespace)).text
            controller_type = root.find(
                ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-type']"
                .format(self.__namespace)).text
            if controller_type == "Virtual Controller":
                self.__ctrl["type"] = True
            elif controller_type == "Real Controller":
                self.__ctrl["type"] = False
                self.__ctrl["id"] = root.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-id']"
                    .format(self.__namespace)).text
        self.refresh_rw()

        self.__logger = WebService.get_logging()
        self.__logger.debug(self.__ctrl)
        self.__logger.debug(self.__rw)

    @staticmethod
    def get_logging():
        """get_logging

        """
        logger = logging.getLogger('WebService')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler(
            '/home/engin/source/repos/aprolpython/robotwebservice.log')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

    def refresh_rw(self):
        """
        The response data format is json.
        """
        # For json format data
        #url = "http://{0}:{1}/rw/system?json=1".format(self.__host, self.__port)
        #resp = self.__session.get(url, cookies=self.__cookies)
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

    def get_rws_resource(self, resource, key):
        """get_rws_resource
        """
        url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resource)
        resp = self.__session.get(url, cookies=self.__cookies)
        obj = json.loads(resp.text)
        return obj["_embedded"]["_state"][0][key]

    def refresh_rws_resources(self, resources, keys, values):
        """refresh_rws_resources
        """
        if isinstance(resources, tuple):
            for resource, key in zip(resources, keys):
                url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resource)
                resp = self.__session.get(url, cookies=self.__cookies)
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
            resp = self.__session.get(url, cookies=self.__cookies)
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

    def get_ctrl(self):
        """RobotWebService

        """
        return self.__ctrl

    def get_rw(self):
        """RobotWebService

        """
        return self.__rw

    def close_session(self):
        """RobotWebService

        """
        self.__session.close()


def main(argv):
    """RobotWebService

    """
    print (argv)
    try:
        web_service = WebService(port=8610)
        print (web_service.get_ctrl())
        print (web_service.get_rw())
        web_service.close_session()
    except requests.ConnectionError:
        print ("ConnectionError")


if __name__ == "__main__":
    main(sys.argv[1:])
