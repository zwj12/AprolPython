#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020-3-7
# @Author  : Michael

"""RobotWebService
chmod a+x we*
pylint robotwebservice.py
proxy --hostname 192.168.2.52 --port 8080
"""

import sys
import re
import json
import xml.etree.ElementTree as ET
import cookielib
import MySQLdb
from requests.auth import HTTPDigestAuth
import requests
from rwsexception import RWSException

class RobotWebService(object):
    """RobotWebService
    The subset of RobotWebService is similar of web services resources
    which is described at http://developercenter.robotstudio.com/webservice/api_reference
    |___rw
        |___cfg
            |___sio
            |___sys
            |___eio
            |___moc
            |___proc
            |___mmc
        |___iosystem
            |___signals
        |___rapid
            |___execution
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
        |___elog
    |___symboldata
        |___T_ROB1
            |___user
    |___ctrl
        |___ctrl-name
        |___ctrl-type
    """
    __namespace = '{http://www.w3.org/1999/xhtml}'

    def __init__(self
                 , host="10.0.2.2"
                 , port=80
                 , username="Default User"
                 , password="robotics"
                 , **kwargs):
        """Create Session and get the robot's overview information
        """
        self.__host = host
        self.__port = port
        self.__digest_auth = HTTPDigestAuth(username, password)
        self.__timeout = kwargs.get("timeout", 0.5)
        self.__proxies = kwargs.get("proxies", None)
        if self.__timeout < 0.1:
            self.__timeout = 0.5
        self.__session = None

        self.__root = {"ctrl":{}, "rw":{}, "symboldata":{}}
        self.__root["rw"] = {"panel":{}, "cfg":{}, "rapid":{},
                             "system":{}, "iosystem":{}, "elog":{}}
        self.__root["rw"]["cfg"] = {"moc":{}, "eio":{}, "sio":{}, "sys":{}, "mmc":{}, "proc":{}}
        self.__root["rw"]["rapid"] = {"execution":{}}
        self.__root["rw"]["iosystem"] = {"signals":{}}
        self.__root["symboldata"] = {"T_ROB1":{}}
        self.__root["symboldata"]["T_ROB1"] = {"user":{}}

    def get_session(self):
        """RobotWebService

        """
        if self.__session is None:
            session = requests.Session()
            session.cookies = RobotWebService.get_cookies(self.__host, self.__port)
            # by xml format data
            url = "http://{0}:{1}/ctrl".format(self.__host, self.__port)
            try:
                resp = session.get(url, timeout=self.__timeout, proxies=self.__proxies)
                if resp.status_code == 401:
                    session.cookies = requests.cookies.RequestsCookieJar()
                    resp = session.get(url, auth=self.__digest_auth,
                                       timeout=self.__timeout, proxies=self.__proxies)
                    if resp.status_code == 200:
                        RobotWebService.save_cookies(session.cookies, self.__host, self.__port)
                if resp.status_code == 200:
                    self.__session = session
                    xml_response = ET.fromstring(resp.text)
                    self.refresh_xml_ctrl(xml_response)
                else:
                    raise RWSException(RWSException.ErrorGetSession
                                       , "get_session", resp.status_code)
            except requests.Timeout:
                raise RWSException(RWSException.ErrorTimeOut, "get_session", -1)
            except requests.ConnectionError:
                raise RWSException(RWSException.ErrorConnection, "get_session", -1)
            except Exception, exception:
                if isinstance(exception, RWSException):
                    raise
                raise RWSException(RWSException.ErrorGetSession, "get_session", -1)
        return self.__session

    def refresh_xml_ctrl(self, xml_data):
        """get_xml_ctrl
        """
        try:
            if xml_data.findall(".//{0}li[@class='ctrl-identity-info-li']"
                                .format(self.__namespace)):
                self.__root["ctrl"]["ctrl-name"] = xml_data.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-name']"
                    .format(self.__namespace)).text
                self.__root["ctrl"]["ctrl-type"] = xml_data.find(
                    ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-type']"
                    .format(self.__namespace)).text
                if self.__root["ctrl"]["ctrl-type"] == "Real Controller":
                    self.__root["ctrl"]["ctrl-id"] = xml_data.find(
                        ".//{0}li[@class='ctrl-identity-info-li']/{0}span[@class='ctrl-id']"
                        .format(self.__namespace)).text
        except:
            raise RWSException(RWSException.ErrorRefreshXmlCtrl, "xml_data", -1)

    def close_session(self):
        """RobotWebService

        """
        if self.__session is not None:
            self.__session.close()

    @staticmethod
    def save_cookies(cookies, host, port):
        """save_cookies

        """
        try:
            lwp_cookie_jar = cookielib.LWPCookieJar(
                filename="robot_" + host + "_" + str(port) + ".txt")
            for cookie in cookies:
                lwp_cookie_jar.set_cookie(cookie)
            lwp_cookie_jar.save(ignore_discard=True)
        except:
            raise RWSException(RWSException.ErrorSaveCookies, "save_cookies", -1)

    @staticmethod
    def get_cookies(host, port):
        """load_cookies

        """
        try:
            lwp_cookie_jar = cookielib.LWPCookieJar(
                filename="robot_" + host + "_" + str(port) + ".txt")
            lwp_cookie_jar.load(ignore_discard=True)
            cookies = requests.cookies.RequestsCookieJar()
            for cookie in lwp_cookie_jar:
                #cookies.set(name=cookie.name, value=cookie.value, domain="." + host)
                cookies.set_cookie(cookie)
            return cookies
        except:
            return requests.cookies.RequestsCookieJar()
            #raise RWSException(RWSException.ErrorGetCookies, "get_cookies", -1)

    def refresh_priority_low(self):
        """refresh_priority_low

        """
        try:
            self.refresh_resources( \
                "rw/system" \
                , ("name", "sysid", "rwversion", "starttm") \
                , self.__root["rw"]["system"])
            #Bugs found when robot with positioner A750
            #self.refresh_resources( \
            #    "rw/system/robottype" \
            #    , ("robot-type",) \
            #    , self.__root["rw"]["system"])
            self.refresh_resources( \
                "rw/system/options" \
                , ("option",) \
                , self.__root["rw"]["system"])
            self.refresh_cfg( \
                "moc" \
                , "ROBOT_SERIAL_NUMBER" \
                , self.__root["rw"]["cfg"]["moc"])
            self.refresh_elog()
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshPriorityLow, "refresh_priority_low", -1)

    def refresh_priority_medium(self):
        """refresh_priority_medium

        """
        try:
            self.__root["symboldata"]["T_ROB1"]["user"].update(self.get_symbol_data(\
                "T_ROB1", "user", ("reg1", "reg2", "reg3", "reg4", "reg5")))
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshPriorityMedium
                               , "refresh_priority_medium", -1)

    def refresh_priority_high(self):
        """refresh_priority_high

        """
        try:
            self.refresh_resources( \
                ("rw/panel/ctrlstate", "rw/panel/opmode", "rw/panel/speedratio") \
                , ("ctrlstate", "opmode", "speedratio") \
                , self.__root["rw"]["panel"])
            self.refresh_resources( \
                "rw/rapid/execution" \
                , ("ctrlexecstate", "cycle") \
                , self.__root["rw"]["rapid"]["execution"])
            self.refresh_signals(self.__root["rw"]["iosystem"]["signals"])
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshPriorityHigh, "refresh_priority_high", -1)

    def refresh_signals(self, signals):
        """refresh_signals
        """
        try:
            self.get_session()
            url = "http://{0}:{1}/rw/iosystem/signals?json=1".format(self.__host, self.__port)
            resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
            if resp.status_code == 200:
                obj = json.loads(resp.text)
                for state in obj["_embedded"]["_state"]:
                    #signals[state["name"]] = {}
                    #signals[state["name"]]["name"] = state["name"]
                    #signals[state["name"]]["type"] = state["type"]
                    #signals[state["name"]]["lvalue"] = state["lvalue"]
                    signals[state["name"]] = state
                while "next" in obj["_links"]:
                    url = obj["_links"]["base"]["href"] + obj["_links"]["next"]["href"]
                    resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
                    if resp.status_code == 200:
                        obj = json.loads(resp.text)
                        for state in obj["_embedded"]["_state"]:
                            signals[state["name"]] = state
            else:
                raise RWSException(RWSException.ErrorRefreshSignals
                                   , "status_code", resp.status_code)
        except requests.Timeout:
            raise RWSException(RWSException.ErrorTimeOut, "refresh_signals", -1)
        except requests.ConnectionError:
            raise RWSException(RWSException.ErrorConnection, "refresh_signals", -1)
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshSignals, "refresh_signals", -1)

    def refresh_resources(self, resources, keys, values):
        """refresh_resources
        the key/value pairs can be in one resource or one resources tuple
        """
        try:
            self.get_session()
            if isinstance(resources, tuple):
                for resource, key in zip(resources, keys):
                    url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resource)
                    resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
                    if resp.status_code == 200:
                        obj = json.loads(resp.text)
                        values[key] = RobotWebService.get_json_value(obj, key)
                    else:
                        raise RWSException(RWSException.ErrorRefreshResources
                                           , "status_code", resp.status_code)
            else:
                url = "http://{0}:{1}/{2}?json=1".format(self.__host, self.__port, resources)
                resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
                if resp.status_code == 200:
                    obj = json.loads(resp.text)
                    for key in keys:
                        values[key] = RobotWebService.get_json_value(obj, key)
                else:
                    raise RWSException(RWSException.ErrorRefreshResources
                                       , "status_code", resp.status_code)
        except requests.Timeout:
            raise RWSException(RWSException.ErrorTimeOut, "refresh_resources", -1)
        except requests.ConnectionError:
            raise RWSException(RWSException.ErrorConnection, "refresh_resources", -1)
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshResources, "refresh_resources", -1)

    @staticmethod
    def get_json_value(json_data, key):
        """
        {
            "_links": {
                "base": {
                    "href": "http://127.0.0.1:8610/rw/rapid/"
                }
            },
            "_embedded": {
                "_state": [
                    {
                        "_type": "rap-execution",
                        "_title": "execution",
                        "ctrlexecstate": "stopped",
                        "cycle": "forever"
                    }
                ]
            }
        }
        """
        try:
            state_values = []
            for state in json_data["_embedded"]["_state"]:
                if key in state:
                    state_values.append(state[key])
            if len(state_values) == 1:
                return state_values[0]
            return state_values
        except:
            raise RWSException(RWSException.ErrorGetJsonValue, str(json_data), -1)

    def get_symbol_data(self, task, module, names):
        """get_symbol_data
        """
        try:
            self.get_session()
            symbols = {}
            for name in names:
                url = "http://{0}:{1}/rw/rapid/symbol/data/RAPID/{2}/{3}/{4}?json=1"\
                    .format(self.__host, self.__port, task, module, name)
                resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
                if resp.status_code == 200:
                    obj = json.loads(resp.text)
                    symbols[name] = obj["_embedded"]["_state"][0]["value"]
                else:
                    raise RWSException(RWSException.ErrorGetSymbolData
                                       , "status_code", resp.status_code)
            return symbols
        except requests.Timeout:
            raise RWSException(RWSException.ErrorTimeOut, "get_symbol_data", -1)
        except requests.ConnectionError:
            raise RWSException(RWSException.ErrorConnection, "get_symbol_data", -1)
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorGetSymbolData, "get_symbol_data", -1)

    def refresh_cfg(self, domain, domain_type, domain_values):
        """refresh_cfg
        rw/cfg/moc/MOTION_PLANNER/instances
        """
        try:
            self.get_session()
            domain_values[domain_type] = {}
            url = "http://{0}:{1}/rw/cfg/{2}/{3}/instances?json=1".format(
                self.__host, self.__port, domain, domain_type)
            resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
            if resp.status_code == 200:
                obj = json.loads(resp.text)
                for state in obj["_embedded"]["_state"]:
                    domain_values[domain_type][state["_title"]] = {}
                    for attrib in state["attrib"]:
                        domain_values[domain_type][state["_title"]][attrib["_title"]] \
                            = attrib["value"]
            else:
                raise RWSException(RWSException.ErrorRefreshCfg
                                   , "status_code", resp.status_code)
        except requests.Timeout:
            raise RWSException(RWSException.ErrorTimeOut, "refresh_cfg", -1)
        except requests.ConnectionError:
            raise RWSException(RWSException.ErrorConnection, "refresh_cfg", -1)
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshCfg, "refresh_cfg", -1)

    def refresh_elog(self):
        """refresh_elog
        rw/elog
        """
        try:
            self.get_session()
            url = "http://{0}:{1}/rw/elog".format(
                self.__host, self.__port)
            resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
            if resp.status_code == 200:
                xml_data = ET.fromstring(resp.text)
                for domain_data in xml_data.findall( \
                    ".//{0}li[@class='elog-domain-li']".format(self.__namespace)):
                    domain = {domain_data.attrib["title"]:{}}
                    numevts = domain_data.find(
                        "{0}span[@class='numevts']"
                        .format(self.__namespace)).text
                    buffsize = domain_data.find(
                        "{0}span[@class='buffsize']"
                        .format(self.__namespace)).text
                    domain[domain_data.attrib["title"]] = {"numevts":numevts, "buffsize":buffsize}
                    self.__root["rw"]["elog"].update(domain)
            else:
                raise RWSException(RWSException.ErrorRefreshElog
                                   , "status_code", resp.status_code)
        except requests.Timeout:
            raise RWSException(RWSException.ErrorTimeOut, "refresh_elog", -1)
        except requests.ConnectionError:
            raise RWSException(RWSException.ErrorConnection, "refresh_elog", -1)
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshElog, "refresh_elog", -1)

    def refresh_elog_messages(self, domain, elogseqnum_start, resource):
        """refresh_elog_messages
        rw/elog/0?elogseqnum=4&lang=en&resource=title&json=1
        """
        try:
            self.get_session()
            pattern_elogseqnum = re.compile(r'/(\d+)$')
            messages = {}
            url_base = "http://{0}:{1}/rw/elog/{2}".format(self.__host, self.__port, domain)
            while len(messages) < int(self.__root["rw"]["elog"][domain]["numevts"]):
                if resource == "title":
                    url = url_base + "?elogseqnum={0}&lang=en&resource=title&json=1" \
                        .format(elogseqnum_start)
                else:
                    url = url_base + "?elogseqnum={0}&json=1".format(elogseqnum_start)
                resp = self.__session.get(url, timeout=self.__timeout, proxies=self.__proxies)
                if resp.status_code == 200:
                    obj = json.loads(resp.text)
                    for state in obj["_embedded"]["_state"]:
                        message = {}
                        message["code"] = int(state["code"])
                        message["tstamp"] = state["tstamp"]
                        match_elogseqnum = pattern_elogseqnum.search(state["_title"])
                        message["elogseqnum"] = int(match_elogseqnum.group(1))
                        elogseqnum_start = message["elogseqnum"] + 1
                        if resource == "title":
                            message["msg-type"] = int(state["msg-type"])
                            message["title"] = state["title"]
                        else:
                            message["msg-type"] = int(state["msgtype"])
                            message["src-name"] = state["src-name"]
                            message["argc"] = state["argc"]
                            if message["argc"] != "0":
                                message["argv"] = state["argv"]
                        messages[message["elogseqnum"]] = message
                    if len(obj["_embedded"]["_state"]) < 50:
                        break
                elif resp.status_code == 204:
                    break
                else:
                    raise RWSException(RWSException.ErrorRefreshElog
                                       , "status_code", resp.status_code)
            self.__root["rw"]["elog"][domain]["messages"] = messages
        except requests.Timeout:
            raise RWSException(RWSException.ErrorTimeOut, "refresh_elog_messages", -1)
        except requests.ConnectionError:
            raise RWSException(RWSException.ErrorConnection, "refresh_elog_messages", -1)
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorRefreshElogMessages, "refresh_elog_messages", -1)

    def clear_mariadb_elog(self
                           , host="localhost"
                           , username="buradmin"
                           , password=".buradmin"
                           , database="BUR_PDA"):
        """clear_mariadb_elog

        """
        try:
            mariadb = MySQLdb.connect(host, username, password, database, charset='utf8')
            cursor = mariadb.cursor()
            sql = "DELETE FROM `robot_elog` WHERE ip_address='%s' AND system_name='%s'" \
                % (self.__host, self.__root["rw"]["system"]["name"])
            cursor.execute(sql)
            mariadb.commit()
            mariadb.close()
        except Exception, exception:
            raise RWSException(RWSException.ErrorClearMariadbElog
                               , "clear_mariadb_elog", -1)

    def get_mariadb_last_elogseqnum(self
                                    , host="localhost"
                                    , username="buradmin"
                                    , password=".buradmin"
                                    , database="BUR_PDA"):
        """get_mariadb_last_elogseqnum

        """
        try:
            mariadb = MySQLdb.connect(host, username, password, database, charset='utf8')
            cursor = mariadb.cursor()
            sql = "SELECT MAX(elogseqnum) FROM `robot_elog`" \
                + " WHERE ip_address='%s' AND system_name='%s'" \
                % (self.__host, self.__root["rw"]["system"]["name"])
            cursor.execute(sql)
            last_elogseqnum = cursor.fetchone()[0]
            mariadb.close()
            if last_elogseqnum is None:
                last_elogseqnum = 0
            return last_elogseqnum
        except Exception, exception:
            raise RWSException(RWSException.ErrorGetMariadbLastElogseqnum
                               , "get_mariadb_last_elogseqnum", -1)

    def update_mariadb_elog_messages(self
                                     , host="localhost"
                                     , username="buradmin"
                                     , password=".buradmin"
                                     , database="BUR_PDA"):
        """update_mariadb_elog_messages

        """
        try:
            serial_number_dict = self.__root["rw"]["cfg"]["moc"]["ROBOT_SERIAL_NUMBER"]["rob_1"]
            serial_number = serial_number_dict["robot_serial_number_high_part"] \
                + "-" +serial_number_dict["robot_serial_number_low_part"]
            sysid = self.__root["rw"]["system"]["sysid"][1:-1]
            last_elogseqnum = 0
            mariadb = MySQLdb.connect(host, username, password, database, charset='utf8')
            cursor = mariadb.cursor()
            try:
                for message in self.__root["rw"]["elog"]["0"]["messages"].values():
                    values = (self.__host
                              , serial_number
                              , self.__root["ctrl"]["ctrl-name"]
                              , self.__root["rw"]["system"]["name"]
                              , sysid
                              , message["tstamp"].replace(" T ", " ")
                              , message["elogseqnum"]
                              , message["title"]
                              , message["code"]
                              , message["msg-type"])
                    sql = "INSERT INTO `robot_elog`"
                    sql += " (ip_address,serial_number,controller_name,system_name,sysid \
                    ,tstamp,elogseqnum,title,code,msg_type)"
                    sql += " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', %d, %d)" % values
                    cursor.execute(sql)
                    if last_elogseqnum < message["elogseqnum"]:
                        last_elogseqnum = message["elogseqnum"]
                mariadb.commit()
            except:
                mariadb.rollback()
                raise RWSException(RWSException.ErrorUpdateMariadbElogMessages
                                   , "update_mariadb_elog_messages rollback", -1)
            mariadb.close()
            return last_elogseqnum
        except Exception, exception:
            if isinstance(exception, RWSException):
                raise
            raise RWSException(RWSException.ErrorUpdateMariadbElogMessages
                               , "update_mariadb_elog_messages", -1)

    def get_host(self):
        """RobotWebService

        """
        return self.__host

    def get_port(self):
        """RobotWebService

        """
        return self.__port

    def get_root(self):
        """RobotWebService

        """
        return self.__root

    def show_tree(self, obj, layer, max_layer=3):
        """RobotWebService

        """
        if isinstance(obj, dict):
            for key, value in obj.items():
                if layer == 1:
                    print "|___" + key
                    #print (u"└───" + key)
                elif layer <= max_layer:
                    print "    "* (layer-1) + "|___"  + key
                    #print ("    "* (layer-1) + u"└───"  + key)
                self.show_tree(value, layer+1, max_layer)


def main(argv):
    """RobotWebService

    """
    #print (argv)
    try:
        proxies = {
            "http": "http://192.168.2.52:8600",
            "https": "http://192.168.2.52:8600",
            }
        #web_service = RobotWebService(host="192.168.2.52", port=8612, timeout=1, proxies=proxies)
        web_service = RobotWebService(host="10.0.2.2", port=46112, timeout=2)
        web_service.refresh_priority_high()
        web_service.refresh_priority_medium()
        web_service.refresh_priority_low()
        last_elogseqnum = web_service.get_mariadb_last_elogseqnum()
        web_service.clear_mariadb_elog()
        elogseqnum = int(web_service.get_root()["rw"]["elog"]["0"]["numevts"]) - 50
        elogseqnum = last_elogseqnum+1
        web_service.refresh_elog_messages("0", elogseqnum, "title")
        last_elogseqnum = web_service.update_mariadb_elog_messages()
        print last_elogseqnum
        web_service.close_session()
        #serial_number = web_service.get_root()["rw"]["cfg"]["moc"]["ROBOT_SERIAL_NUMBER"]["rob_1"]
        #sss = serial_number["robot_serial_number_high_part"] \
            #+ "-" +serial_number["robot_serial_number_low_part"]
        signals = web_service.get_root()["rw"]["iosystem"]["signals"]
        print len(signals)
        #signal = signals["doSysOutTaskExecuting"]
        #print signal
        #signal_value = signal["lvalue"]
        #print signal_value
        """
        value = web_service.get_root()["symboldata"]["T_ROB1"]
        print value
        names = ("numPartCount",)
        values = web_service.get_symbol_data( \
            "T_ROB1", "OpcUaModule", names)
        print int(float(values["numPartCount"]))
        print int(float("6.3"))
        """
        #print web_service.get_root()["rw"]["cfg"]
        #print web_service.get_root()["rw"]["elog"]["0"]
        #web_service.show_tree(web_service.get_root(), 1)
    except Exception, exception:
        print exception
    finally:
        #web_service.close_session()
        pass

if __name__ == "__main__":
    main(sys.argv[1:])
else:
    pass
