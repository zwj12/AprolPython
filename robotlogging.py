#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020-3-7
# @Author  : Michael

"""robotlogging
chmod a+x we*
proxy --hostname 192.168.2.52 --port 8080

"""

import sys
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


def main(argv):
    """logging

    """
    #print (argv)
    logger = get_logging()
    logger.debug("test")
    print "test"

if __name__ == "__main__":
    main(sys.argv[1:])
else:
    pass
