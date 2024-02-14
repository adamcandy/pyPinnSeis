#!/usr/bin/env python3
"""
pyPinnSeis: Library created with the boilerplate machine, for pyPinnSeis. 

#This code uses Physics-Informed Neural Networks PINNs (Raissi et al., 2019) to solve the inverse 
#acoustic problem for an elliposidal low velocity anomaly in the domain with a point source (Synthetic Crosswell). 
#See Case study 3 from our paper Rasht-Behesht et al., 2021 for a full description of all parameters involved 
#Note we use input data from SPECFEM2D (Komatitsch  and  Tromp,  1999;  Tromp  et  al.,  2008) for training the PINN 

# python -m pip install numpy scipy matplotlib tensorflow SALib
"""

__author__ = "Dr Adam S. Candy"
__version__ = "0.1.0"
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
    c.process()
    c.show()

    report('Complete and closed cleanly')


if __name__ == "__main__":
    main()
