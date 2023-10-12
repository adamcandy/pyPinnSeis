#!/usr/bin/env python3

from .log import error

################################################################################
#### Global variables ##########################################################
################################################################################

trapped = False

################################################################################
#### General routines ##########################################################
################################################################################


def signal_handler(signal, frame):
    """Process a signal event"""
    from sys import exit

    global trapped
    if not trapped:
        trapped = True
        error("Ouch!")
    else:
        exit(1)


def isTrapped():
    """Check if a signal event has been received"""
    global trapped
    return trapped
