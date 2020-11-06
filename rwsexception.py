#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020-3-7
# @Author  : Michael

"""RWSException
chmod a+x we*

"""

class RWSException(Exception):
    """RWSException
    """

    ErrorGetCookies = 1
    ErrorGetSession = 2
    ErrorTimeOut = 3
    ErrorConnection = 4
    ErrorSaveCookies = 5
    ErrorRefreshPriorityLow = 6
    ErrorRefreshPriorityMedium = 7
    ErrorRefreshPriorityHigh = 8
    ErrorRefreshSignals = 9
    ErrorRefreshResources = 10
    ErrorGetSymbolData = 11
    ErrorGetJsonValue = 12
    ErrorRefreshXmlCtrl = 13
    ErrorRefreshCfg = 14
    ErrorRefreshElog = 15
    ErrorRefreshElogMessages = 16

    def __init__(self, error_code, error_message, response_status_code):
        Exception.__init__(self)
        self.error_code = error_code
        self.error_message = error_message
        self.response_status_code = response_status_code

    def __str__(self):
        """__str__
        """
        return str({"error_code":self.error_code \
                    , "error_message":self.error_message \
                    , "response_status_code":self.response_status_code})
