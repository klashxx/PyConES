# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""

import re
import os
import stat


def mail(mail):
    """``mail`` *regex* checker."""

    buzon = re.compile(r'''
                        \A                  # Comienzo
                        [\w\d]+[\w\d._-]+   # Usuario
                        @
                        ([\w\d.]+\.)+       # Prefijo dominio
                        ([\w\d.]+\.)?       # Subprefijo dominio opcional
                        (es|com|int)        # Dominio
                        \Z                  # Fin
                        ''', re.IGNORECASE | re.VERBOSE)

    if not buzon.match(mail):
        raise TypeError('Email address {0} is invalid.'.format(mail))

    return mail


def filesystem(fs):
    """``FS`` checker."""

    fs = os.path.normpath(os.path.expanduser(os.path.expandvars(fs)))
    try:
        statcmd = os.stat(fs)
        if not stat.S_ISDIR(os.stat(fs)[stat.ST_MODE]):
            raise TypeError('Invalid FS: {0}')
    except OSError:
        raise TypeError('Invalid FS: {0}')

    return os.path.abspath(fs)
