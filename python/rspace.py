#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyConES 2016 Almería
"""

from __future__ import division

__author__ = 'Juan Diego Godoy Robles'
__version__ = '0.1'


import os
import sys
import socket
import argparse
import platform

import validation
import logger
import db
from lib import avaliable_space, df
from custom_exceptions import ParamError

LOG = './tmp/{0}.python.log'.format(os.path.splitext(
    os.path.basename(sys.argv[0]))[0])


def arguments():
    """Funcion que recoge los argumentos parseados"""

    parser = argparse.ArgumentParser(
        description='Database space inspector.',
        epilog='PyConES 2016 - Almería')

    parser.add_argument('fs',
                        help='Target filesystem.',
                        type=validation.filesystem,
                        action='store')

    parser.add_argument('host',
                        nargs='?',
                        help='Target host.',
                        default=socket.gethostname(),
                        action='store')

    parser.add_argument('-d', '--databases',
                        action='append',
                        dest='databases',
                        help='Target database/s.',
                        choices=['pymysql', 'dev'])

    parser.add_argument('-m', '--mails',
                        action='append',
                        dest='mails',
                        type=validation.mail,
                        help='Notification mails.')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s v{0}'.format(__version__))
    return parser


def check_space(log, fs, local_host, remote_host):
    try:
        free = avaliable_space(fs)
    except OSError as err:
        log.critical("Can't get free space in {0}, "
                     "error: {1}".format(fs, err))
        sys.exit(2)

    try:
        log.info('Avaliable local space (df) in '
                 '{0}: {1}'.format(fs, df(fs)))
    except ParamError as err:
        log.warning(err)

    log.info('Host: {0} .Avaliable local space '
             'in {1}: {2} {3:0.2f} GBs'.format(local_host,
                                               fs,
                                               free,
                                               free/1024/1024/1024))

    if local_host != remote_host:
        free = avaliable_space(fs, host=remote_host)
        log.info('Host: {0} .Avaliable remote space '
                 'in {1}: {2} {3:0.2f} GBs'.format(remote_host,
                                                   fs,
                                                   free,
                                                   free/1024/1024/1024))
    return None


def check_db_space(log, dbids):

    for dbid in dbids:
        try:
            db_conn = db.connect(dbid)
        except DBError as err:
            log.critical("Can't connect to {0}: {1}".format(dbid, err))
            continue

        log.info('Connected to {0}'.format(dbid))

        try:
            rows = db.avaliable_space(db_conn)
        except DBError as err:
            log.critical(err)
        else:
            for database, table, total in rows:
                print '{0:30s} {1:30s} {2}'.format(database, table, total)

    return None


def main():
    args = arguments().parse_args()

    if args.mails is None:
        args.mails = ['pyconesal@gmail.com']

    log = logger.setup_logger('rspace', LOG)
    local_host = socket.gethostname()

    log.info('Parameter validation ok')
    log.info('OS: {0}'.format(platform.system()))
    log.info('host: {0}'.format(args.host))
    log.info('local_host: {0}'.format(local_host))
    log.debug('fs: {0}'.format(args.fs))
    log.debug('databases: {0}'.format(args.databases))
    log.debug('mails: {0}'.format(args.mails))

    check_space(log, args.fs, local_host, args.host)

    if args.databases is not None:
        check_db_space(log, args.databases)

    return None

if __name__ == "__main__":
    main()
