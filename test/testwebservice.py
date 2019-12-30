#!/usr/bin/python
# -*- coding: utf-8 -*-

"""testwebservice
chmod a+x te*

"""

import sys
sys.path.append('/home/engin/source/repos/aprolpython')
import webservice
import requests


def main(argv):
    """main

    """
    print (argv)
    try:
        web_service = webservice.WebService(port=8610)
        print (web_service.get_ctrl())
        print (web_service.get_rw())
        print (web_service.get_symboldata())
        web_service.close_session()
    except requests.ConnectionError:
        print ("ConnectionError")


if __name__ == "__main__":
    main(sys.argv[1:])
