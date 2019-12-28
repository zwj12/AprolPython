#!/usr/bin/python3
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
        self.__logger.debug(self.__ctrl["name"])
        self.__logger.debug(self.__rw)

    @staticmethod
    def get_logging():
        """get_logging

        """
        logger = logging.getLogger('WebService')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        filehandler = logging.FileHandler('/home/engin/source/repos/robot/robotwebservice.log')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        return logger

    def refresh_rw(self):
        """
        The response data format is json.
        """
        # For json format data
        url = "http://{0}:{1}/rw/system?json=1".format(self.__host, self.__port)
        resp = self.__session.get(url, cookies=self.__cookies)
        obj = json.loads(resp.text)
        self.__rw["system_name"] = obj["_embedded"]["_state"][0]["name"]
        self.__rw["rw_version"] = obj["_embedded"]["_state"][0]["rwversion"]
        self.__rw["sysid"] = obj["_embedded"]["_state"][0]["sysid"]

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
    except KeyboardInterrupt:
        web_service.close_session()


if __name__ == "__main__":
    main(sys.argv[1:])
