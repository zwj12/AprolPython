#!/usr/bin/python
# -*- coding: utf-8 -*-

"""testwebservice
chmod a+x te*

"""

import logging

def get_logging():
    """get_logging

    """
    logger = logging.getLogger('WebService')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    #filehandler = logging.FileHandler(
    #    '/home/engin/source/repos/aprolpython/robotwebservice.log')
    filehandler = logging.FileHandler('robotwebservice.log')
    filehandler.setFormatter(formatter)
    logger.addHandler(filehandler)
    return logger

Logger = get_logging()
Logger.debug("test")
