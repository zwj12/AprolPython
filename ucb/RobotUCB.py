#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import ucbbasic
import robotwebservice
import robotlogging
from rwsexception import RWSException
#import robotlogging

######################################################################
### Read inputs by environment variables)
######################################################################
def read_inputs(inputs, outputs):
    """read_input
    """
    inputs['Debug'] = int(os.environ['Debug'])
    inputs['IPAddress'] = os.environ['IPAddress']
    inputs['Port'] = int(os.environ['Port'])
    inputs['UserName'] = os.environ['UserName']
    inputs['Password'] = os.environ['Password']
    inputs['Timeout'] = float(os.environ['Timeout'])
    inputs['PriorityHigh'] = int(os.environ['PriorityHigh'])
    inputs['PriorityMedium'] = int(os.environ['PriorityMedium'])
    inputs['PriorityLow'] = int(os.environ['PriorityLow'])
    inputs['ClearElog'] = int(os.environ['ClearElog'])
    inputs['ProxyServer'] = os.environ['ProxyServer']
    inputs['ProxyPort'] = int(os.environ['ProxyPort'])
    inputs['DioSignalName_1'] = os.environ['DioSignalName_1']
    inputs['DioSignalName_2'] = os.environ['DioSignalName_2']
    inputs['DioSignalName_3'] = os.environ['DioSignalName_3']
    inputs['DioSignalName_4'] = os.environ['DioSignalName_4']
    inputs['DioSignalName_5'] = os.environ['DioSignalName_5']
    inputs['GioSignalName_1'] = os.environ['GioSignalName_1']
    inputs['GioSignalName_2'] = os.environ['GioSignalName_2']
    inputs['GioSignalName_3'] = os.environ['GioSignalName_3']
    inputs['GioSignalName_4'] = os.environ['GioSignalName_4']
    inputs['GioSignalName_5'] = os.environ['GioSignalName_5']
    inputs['AioSignalName_1'] = os.environ['AioSignalName_1']
    inputs['AioSignalName_2'] = os.environ['AioSignalName_2']
    inputs['AioSignalName_3'] = os.environ['AioSignalName_3']
    inputs['AioSignalName_4'] = os.environ['AioSignalName_4']
    inputs['AioSignalName_5'] = os.environ['AioSignalName_5']
    outputs['LoopCnt'] = int(os.environ['LoopCnt'])
    outputs["ControllerName"] = os.environ['ControllerName']
    outputs["SystemID"] = os.environ['SystemID']
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
    outputs['LastElogseqnum'] = int(os.environ['LastElogseqnum'])

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
OUTPUTS["PriorityStatus"] = INPUTS["PriorityHigh"] + 2 * INPUTS["PriorityMedium"] + 4 * INPUTS["PriorityLow"]
Logger = None
if INPUTS['Debug']:
    Logger = robotlogging.get_logging()
    Logger.debug("Start to log debug data:")
    Logger.debug(OUTPUTS)

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
        SYMBOL_NAMES = ("numPartCount",)
        SYMBOL_VALUES = WS.get_symbol_data("T_ROB1", "OpcUaModule", SYMBOL_NAMES)
        if float(SYMBOL_VALUES["numPartCount"]) >= 0:
            OUTPUTS["numPartCount"] = int(float(SYMBOL_VALUES["numPartCount"]))

    if INPUTS['PriorityMedium']:
        WS.refresh_priority_medium()

    if INPUTS['PriorityLow']:
        WS.refresh_priority_low()
        if INPUTS['ClearElog']:
            WS.clear_mariadb_elog()
            OUTPUTS['LastElogseqnum'] = 0
        else:
            OUTPUTS['LastElogseqnum'] = WS.get_mariadb_last_elogseqnum()
            WS.refresh_elog_messages("0", OUTPUTS['LastElogseqnum']+1, "title")
            LastElogseqnum = WS.update_mariadb_elog_messages()
            if LastElogseqnum > 0:
                OUTPUTS['LastElogseqnum'] = LastElogseqnum
    WS.close_session()

    if Logger is not None:
        Logger.debug(WS.get_root()["rw"]["system"])
        Logger.debug(WS.get_root()["rw"]["panel"])
        Logger.debug(WS.get_root()["rw"]["rapid"])
        Logger.debug(WS.get_root()["rw"]["cfg"])
        Logger.debug(WS.get_root()["rw"]["iosystem"])
        Logger.debug(WS.get_root()["ctrl"])
        Logger.debug(WS.get_root()["symboldata"])

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
        OUTPUTS["doSysOutTaskExecuting"] = \
            int(WS.get_root()["rw"]["iosystem"]["signals"]["doSysOutTaskExecuting"]["lvalue"])
        OUTPUTS["PFdoIdle_1"] = int(WS.get_root()["rw"]["iosystem"]["signals"]["PFdoIdle_1"]["lvalue"])
        OUTPUTS["PFdoExecuting_1"] = int(WS.get_root()["rw"]["iosystem"]["signals"]["PFdoExecuting_1"]["lvalue"])
        OUTPUTS["PFgoActiveOrder_1"] = int(WS.get_root()["rw"]["iosystem"]["signals"]["PFgoActiveOrder_1"]["lvalue"])
        OUTPUTS["PFdoActiveOrderIsService_1"] = \
            int(WS.get_root()["rw"]["iosystem"]["signals"]["PFdoActiveOrderIsService_1"]["lvalue"])
        if INPUTS['DioSignalName_1'].strip() != "":
            OUTPUTS["DioSignalValue_1"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['DioSignalName_1']]["lvalue"])
        if INPUTS['DioSignalName_2'].strip() != "":
            OUTPUTS["DioSignalValue_2"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['DioSignalName_2']]["lvalue"])
        if INPUTS['DioSignalName_3'].strip() != "":
            OUTPUTS["DioSignalValue_3"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['DioSignalName_3']]["lvalue"])
        if INPUTS['DioSignalName_4'].strip() != "":
            OUTPUTS["DioSignalValue_4"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['DioSignalName_4']]["lvalue"])
        if INPUTS['DioSignalName_5'].strip() != "":
            OUTPUTS["DioSignalValue_5"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['DioSignalName_5']]["lvalue"])

        if INPUTS['GioSignalName_1'].strip() != "":
            OUTPUTS["GioSignalValue_1"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['GioSignalName_1']]["lvalue"])
        if INPUTS['GioSignalName_2'].strip() != "":
            OUTPUTS["GioSignalValue_2"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['GioSignalName_2']]["lvalue"])
        if INPUTS['GioSignalName_3'].strip() != "":
            OUTPUTS["GioSignalValue_3"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['GioSignalName_3']]["lvalue"])
        if INPUTS['GioSignalName_4'].strip() != "":
            OUTPUTS["GioSignalValue_4"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['GioSignalName_4']]["lvalue"])
        if INPUTS['GioSignalName_5'].strip() != "":
            OUTPUTS["GioSignalValue_5"] = \
                int(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['GioSignalName_5']]["lvalue"])

        if INPUTS['AioSignalName_1'].strip() != "":
            OUTPUTS["AioSignalValue_1"] = \
                float(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['AioSignalName_1']]["lvalue"])
        if INPUTS['AioSignalName_2'].strip() != "":
            OUTPUTS["AioSignalValue_2"] = \
                float(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['AioSignalName_2']]["lvalue"])
        if INPUTS['AioSignalName_3'].strip() != "":
            OUTPUTS["AioSignalValue_3"] = \
                float(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['AioSignalName_3']]["lvalue"])
        if INPUTS['AioSignalName_4'].strip() != "":
            OUTPUTS["AioSignalValue_4"] = \
                float(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['AioSignalName_4']]["lvalue"])
        if INPUTS['AioSignalName_5'].strip() != "":
            OUTPUTS["AioSignalValue_5"] = \
                float(WS.get_root()["rw"]["iosystem"]["signals"][INPUTS['AioSignalName_5']]["lvalue"])

    if Logger is not None:
        Logger.debug(OUTPUTS)

    if INPUTS['PriorityMedium']:
        OUTPUTS["PriorityMediumCnt"] = OUTPUTS["PriorityMediumCnt"] + 1

    if Logger is not None:
        Logger.debug(OUTPUTS)

    if INPUTS['PriorityLow']:
        OUTPUTS["ControllerName"] = WS.get_root()["ctrl"]["ctrl-name"]
        OUTPUTS["SystemID"] = WS.get_root()["rw"]["system"]["sysid"]
        OUTPUTS["SystemName"] = WS.get_root()["rw"]["system"]["name"]
        OUTPUTS["RobotWare"] = WS.get_root()["rw"]["system"]["rwversion"]
        SERIAL_NUMBER = WS.get_root()["rw"]["cfg"]["moc"]["ROBOT_SERIAL_NUMBER"]["rob_1"]
        OUTPUTS["SerialNumber"] = SERIAL_NUMBER["robot_serial_number_high_part"] \
            + "-" +SERIAL_NUMBER["robot_serial_number_low_part"]
        OUTPUTS["PriorityLowCnt"] = OUTPUTS["PriorityLowCnt"] + 1

    if Logger is not None:
        Logger.debug(OUTPUTS)

    OUTPUTS["LnkStat"] = 1
except RWSException, exception:
    OUTPUTS["ErrorCode"] = exception.error_code
    OUTPUTS["ResponseCode"] = exception.response_status_code

OUTPUTS["LoopCnt"] = OUTPUTS["LoopCnt"] + 1

if Logger is not None:
    Logger.debug(OUTPUTS)

write_outputs(OUTPUTS)
