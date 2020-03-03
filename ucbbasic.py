#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ucbbasic.py
chmod a+x uc*

"""

import os
import sys
import signal
#import string


def on_term(signum, frame):
    """on_term
    """
    sys.exit(1)

def on_usr(signum, frame):
    """on_usr
    """
    pass

def signal_handling():
    """signal_handling
    """
    ######################################################################
    ### Signal handling (caused e.g. by RuntimeSystem Download)
    ######################################################################
    signal.signal(signal.SIGTERM, on_term)
    signal.signal(signal.SIGUSR2, on_usr)
    signal.signal(signal.SIGUSR1, on_usr)

def initialization_deinitialization():
    """initialization_deinitialization
    """
    ######################################################################
    ### Initialization phase (script called by UCB Server start)
    ######################################################################
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
                list_of_terminated_instances = sys.argv[4].split(',')
                for inst in list_of_terminated_instances:
                    # cleanup actions for terminated instances possible here
                    pass
        sys.exit(0)

######################################################################
### Read inputs by environment variables)
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
        print (key + "=" + str(outputs[key])) # write variable


if __name__ == "__main__":
    signal_handling()

    INSTANZ = sys.argv[0]
    INPUTS = {}
    OUTPUTS = {}

    initialization_deinitialization()

    read_inputs(INPUTS)
    OUTPUTS.update(INPUTS)
    write_outputs(OUTPUTS)
