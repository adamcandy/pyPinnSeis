#!/usr/bin/env python3
"""
pyPinnSeis: Library created with the boilerplate machine, for pyPinnSeis. 
"""

__author__ = "Dr Adam S. Candy"
__version__ = "0.0.1"
__license__ = "LGPLv3"
__copyright__ = "Copyright 2020"
__credits__ = ["Dr Adam S. Candy"]
__maintainer__ = "Dr Adam S. Candy"
__email__ = "adam@candylab.org"

from signal import signal, SIGINT, SIGTERM
from .trap import signal_handler

signal(SIGINT, signal_handler)
signal(SIGTERM, signal_handler)

################################################################################
#### Main ######################################################################
################################################################################


def main():
    """Main entry point"""
    from .options import checkOptions
    from .log import loggingInit, report
    from .trap import isTrapped
    from .pinn import Pinn

    options = checkOptions()
    log = loggingInit(options)

    c = Pinn(name="Crosswell Inversion_Acoustic")
    #c.process()
    #c.show()

    report('Complete and closed cleanly')


if __name__ == "__main__":
    main()
