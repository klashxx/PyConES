# -*- coding: utf-8 -*-

"""
PyConES 2016 Almería
"""

import sys
import logging


def setup_logger(id_logger, log_file):
    """Logger configuration"""

    logging.basicConfig(level=logging.DEBUG,
                        format=('%(asctime)s %(funcName)-12s %(levelname)-8s'
                                '%(lineno)5d - %(message)s'),
                        datefmt='%y-%m-%d %H:%M:%S',
                        filename=log_file,
                        filemode='w')

    # Terminal output via stdout and not debug messages
    terminal = logging.StreamHandler(sys.stdout)
    terminal.setLevel(logging.INFO)

    # A basic formatting
    terminal.setFormatter(logging.Formatter('%(levelname)-8s: %(message)s'))

    log = logging.getLogger(id_logger)
    log.addHandler(terminal)

    return log
