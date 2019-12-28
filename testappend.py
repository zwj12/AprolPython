import sys

sys.path.append('/home/engin/source/repos/aprolpython')

import webservice

try:
    web_service = webservice.WebService(port=8610)
    print (web_service.get_ctrl())
    print (web_service.get_rw())
except KeyboardInterrupt:
    web_service.close_session()

