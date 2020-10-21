#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import ucbbasic
import robotwebservice
from rwsexception import RWSException
#import robotlogging

######################################################################
### Read inputs by environment variables)
######################################################################
def read_inputs(inputs, outputs):
    """read_input
    """
    inputs['IPAddress'] = os.environ['IPAddress']
    inputs['Port'] = int(os.environ['Port'])
    inputs['UserName'] = os.environ['UserName']
    inputs['Password'] = os.environ['Password']
    inputs['Timeout'] = float(os.environ['Timeout'])
    inputs['PriorityHigh'] = int(os.environ['PriorityHigh'])
    inputs['PriorityMedium'] = int(os.environ['PriorityMedium'])
    inputs['PriorityLow'] = int(os.environ['PriorityLow'])
    inputs['ProxyServer'] = os.environ['ProxyServer']
    inputs['ProxyPort'] = int(os.environ['ProxyPort'])
    outputs['LoopCnt'] = int(os.environ['LoopCnt'])
    outputs["ControllerName"] = os.environ['ControllerName']
    outputs["SystemName"] = os.environ['SystemName']
    outputs["RobotWare"] = os.environ['RobotWare']
    outputs["SerialNumber"] = os.environ['SerialNumber']
    outputs["ExecutionState"] = os.environ['ExecutionState']
    outputs["RunMode"] = os.environ['RunMode']
    outputs["OperatingMode"] = os.environ['OperatingMode']
    outputs["SpeedRatio"] = os.environ['SpeedRatio']
    outputs["ControllerState"] = os.environ['ControllerState']
    outputs["OperatingModeCode"] = int(os.environ['OperatingModeCode'])
    outputs["ControllerStateCode"] = int(os.environ['ControllerStateCode'])
    outputs["ExecutionStateCode"] = int(os.environ['ExecutionStateCode'])
    outputs["RunModeCode"] = int(os.environ['RunModeCode'])
    outputs['PriorityHighCnt'] = int(os.environ['PriorityHighCnt'])
    outputs['PriorityMediumCnt'] = int(os.environ['PriorityMediumCnt'])
    outputs['PriorityLowCnt'] = int(os.environ['PriorityLowCnt'])

######################################################################
### Check how often UCB-script was run
######################################################################
def write_outputs(outputs):
    """write_outputs
    """
    for key in outputs:
        print key + "=" + str(outputs[key]) # write variable


ucbbasic.signal_handling()
INSTANZ = sys.argv[0]
INPUTS = {}
OUTPUTS = {}
ucbbasic.initialization_deinitialization()

read_inputs(INPUTS, OUTPUTS)

OUTPUTS["LnkStat"] = 0
OUTPUTS["ErrorCode"] = 0
OUTPUTS["ResponseCode"] = 0

try:
#    Proxies = None
#    if INPUTS['ProxyServer'].strip()!="":
#        Proxies = {
#            "http": "http://" + INPUTS['ProxyServer'].strip() + ":" + str(INPUTS['ProxyPort']),
#            "https": "http://" + INPUTS['ProxyServer'].strip() + ":" + str(INPUTS['ProxyPort']),
#            }
    WS = robotwebservice.RobotWebService(
        host=INPUTS['IPAddress'],
        port=INPUTS['Port'],
        username=INPUTS['UserName'],
        password=INPUTS['Password'],
        timeout=INPUTS['Timeout'])
#        proxies=Proxies)
    if INPUTS['PriorityHigh']:
        WS.refresh_priority_high()
    if INPUTS['PriorityMedium']:
        WS.refresh_priority_medium()
    if INPUTS['PriorityLow']:
        WS.refresh_priority_low()
    WS.close_session()

    #Logger = robotlogging.get_logging()
    if INPUTS['PriorityHigh']:
        OUTPUTS["ExecutionState"] = WS.get_root()["rw"]["rapid"]["execution"]["ctrlexecstate"]
        if OUTPUTS["ExecutionState"]=="stopped":
            OUTPUTS["ExecutionStateCode"] = 0
        elif OUTPUTS["ExecutionState"]=="running":
            OUTPUTS["ExecutionStateCode"] = 1
        else:
            OUTPUTS["ExecutionStateCode"] = 2
        OUTPUTS["RunMode"] = WS.get_root()["rw"]["rapid"]["execution"]["cycle"]
        if OUTPUTS["RunMode"]=="forever":
            OUTPUTS["RunModeCode"] = 1
        elif OUTPUTS["RunMode"]=="asis":
            OUTPUTS["RunModeCode"] = 2
        elif OUTPUTS["RunMode"]=="once":
            OUTPUTS["RunModeCode"] = 3
        elif OUTPUTS["RunMode"]=="oncedone":
            OUTPUTS["RunModeCode"] = 4
        else:
            OUTPUTS["RunModeCode"] = 0
        OUTPUTS["OperatingMode"] = WS.get_root()["rw"]["panel"]["opmode"]
        if OUTPUTS["OperatingMode"]=="INIT":
            OUTPUTS["OperatingModeCode"] = 1
        elif OUTPUTS["OperatingMode"]=="AUTO_CH":
            OUTPUTS["OperatingModeCode"] = 2
        elif OUTPUTS["OperatingMode"]=="MANF_CH":
            OUTPUTS["OperatingModeCode"] = 3
        elif OUTPUTS["OperatingMode"]=="MANR":
            OUTPUTS["OperatingModeCode"] = 4
        elif OUTPUTS["OperatingMode"]=="MANF":
            OUTPUTS["OperatingModeCode"] = 5
        elif OUTPUTS["OperatingMode"]=="AUTO":
            OUTPUTS["OperatingModeCode"] = 6
        else:
            OUTPUTS["OperatingModeCode"] = 0
        OUTPUTS["SpeedRatio"] = int(WS.get_root()["rw"]["panel"]["speedratio"])
        OUTPUTS["ControllerState"] = WS.get_root()["rw"]["panel"]["ctrlstate"]
        if OUTPUTS["ControllerState"]=="init":
            OUTPUTS["ControllerStateCode"] = 1
        elif OUTPUTS["ControllerState"]=="motoron":
            OUTPUTS["ControllerStateCode"] = 2
        elif OUTPUTS["ControllerState"]=="motoroff":
            OUTPUTS["ControllerStateCode"] = 3
        elif OUTPUTS["ControllerState"]=="guardstop":
            OUTPUTS["ControllerStateCode"] = 4
        elif OUTPUTS["ControllerState"]=="emergencystop":
            OUTPUTS["ControllerStateCode"] = 5
        elif OUTPUTS["ControllerState"]=="emergencystopreset":
            OUTPUTS["ControllerStateCode"] = 6
        elif OUTPUTS["ControllerState"]=="sysfail":
            OUTPUTS["ControllerStateCode"] = 7
        else:
            OUTPUTS["ControllerStateCode"] = 0
        OUTPUTS["PriorityHighCnt"] = OUTPUTS["PriorityHighCnt"] + 1

    if INPUTS['PriorityMedium']:
        OUTPUTS["PriorityMediumCnt"] = OUTPUTS["PriorityMediumCnt"] + 1

    if INPUTS['PriorityLow']:
        OUTPUTS["ControllerName"] = WS.get_root()["ctrl"]["ctrl-name"]
        OUTPUTS["SystemName"] = WS.get_root()["rw"]["system"]["name"]
        OUTPUTS["RobotWare"] = WS.get_root()["rw"]["system"]["rwversion"]
        SERIAL_NUMBER = WS.get_root()["rw"]["cfg"]["moc"]["ROBOT_SERIAL_NUMBER"]["rob_1"]
        OUTPUTS["SerialNumber"] = SERIAL_NUMBER["robot_serial_number_high_part"] \
            + "-" +SERIAL_NUMBER["robot_serial_number_low_part"]
        OUTPUTS["PriorityLowCnt"] = OUTPUTS["PriorityLowCnt"] + 1


    OUTPUTS["LnkStat"] = 1
except RWSException, exception:
    OUTPUTS["ErrorCode"] = exception.error_code
    OUTPUTS["ResponseCode"] = exception.response_status_code

OUTPUTS["LoopCnt"] = OUTPUTS["LoopCnt"] + 1
write_outputs(OUTPUTS)