#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ucbbasic.py
chmod a+x uc*

"""

import os
import sys
import signal
import string


######################################################################
### Signal handling (caused e.g. by RuntimeSystem Download)
######################################################################
def on_term(signum, frame):
    """on_term
    """
    sys.exit(1)

def on_usr(signum, frame):
    """on_usr
    """
    pass

def ucb_basic():
    """ucb_basic
    """

    if len(sys.argv) > 2 and sys.argv[2] == '-init':
        sys.exit(0)

    ######################################################################
    ### De-Initialization phase (script called by UCB Server stop)
    ######################################################################
    if len(sys.argv) > 2 and sys.argv[2] == '-deinit':
        ######################################################################
        ### Forced termination phase (script called by forced UCB Server termination)
        ######################################################################
        if len(sys.argv) > 3 and sys.argv[3] == '-forced':
            if len(sys.argv) > 4:
                list_of_terminated_instances = string.split(sys.argv[4], ',')
                for inst in list_of_terminated_instances:
                    # cleanup actions for terminated instances possible here
                    pass
        sys.exit(0)

######################################################################
### Read inputs 8environment variables)
######################################################################
def read_inputs(inputs):
    """read_input
    """
    #inputs['DevName'] = unicode(os.environ['DevName'], "utf-8")
    for key in os.environ:
        inputs[key] = os.environ[key]

######################################################################
### Check how often UCB-script was run
######################################################################
def write_outputs(outputs):
    """write_outputs
    """
    #LoopCnt = int(os.environ['LoopCnt']) # read variable
    #LoopCnt = LoopCnt + 1 # increment variable
    for key in outputs:
        print key + "=" + str(outputs[key]) # write variable

signal.signal(signal.SIGTERM, on_term)
signal.signal(signal.SIGUSR2, on_usr)
signal.signal(signal.SIGUSR1, on_usr)

######################################################################
### Initialization phase (script called by UCB Server start)
######################################################################
INSTANZ = sys.argv[0]
INPUTS = {}
OUTPUTS = {}

ucb_basic()
read_inputs(INPUTS)
OUTPUTS.update(INPUTS)
write_outputs(OUTPUTS)
