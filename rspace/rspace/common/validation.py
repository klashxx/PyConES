# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""

import re
import os
import stat

from rspace.common.exceptions import ParamError


def mail(maddress):
    """mail *regex* **validator**.

    Args:
        maddress (str): mail to check.

    Returns:
        maddress (str): validated mail string.

    Raises:
        ParamError: if *mail address* **is not valid**.

    Examples:
        >>> from rspace.common.validation import mail
        >>> mail('jdiego_godoy@cajamar.es')
        'jdiego_godoy@cajamar.es'
        >>> mail('jdiego_godoy@cajamar')
        rspace.common.exceptions.ParamError: Email address is invalid.
    """

    buzon = re.compile(r'''
                        \A                  # Comienzo
                        [\w\d]+[\w\d._-]+   # Usuario
                        @
                        ([\w\d.]+\.)+       # Prefijo dominio
                        ([\w\d.]+\.)?       # Subprefijo dominio opcional
                        (es|com|int)        # Dominio
                        \Z                  # Fin
                        ''', re.IGNORECASE | re.VERBOSE)

    if not buzon.match(maddress):
        raise ParamError('Email address {0} is invalid.'.format(maddress))

    return maddress


def filesystem(fs):
    """Directory accessibility checker.

    Args:
        fs (str): ``path`` to check.

    Returns:
        str: validated ``path``.

    Raises:
        ParamError: if ``FS`` **is not reachable**.

    Examples:
        >>> from rspace.common.validation import filesystem
        >>> filesystem('/tmp')
        '/tmp'
        >>> filesystem('~')
        '/home/klashxx'
        >>> filesystem('~/invented')
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "../rspace/common/validation.py", line 75, in filesystem
            raise ParamError('Invalid FS: {0}'.format(fs))
        rspace.common.exceptions.ParamError: Invalid FS: /home/klashxx/invented
    """

    fs = os.path.normpath(os.path.expanduser(os.path.expandvars(fs)))

    try:
        _ = os.stat(fs)
        if not stat.S_ISDIR(os.stat(fs)[stat.ST_MODE]):
            raise ParamError('Invalid FS: {0}'.format(fs))
    except OSError:
        raise ParamError('Invalid FS: {0}'.format(fs))

    return os.path.abspath(fs)
