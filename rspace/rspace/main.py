#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyConES 2016 Almería
"""

from __future__ import division

import os
import sys
import socket
import platform

from rspace.conf import settings as conf
from rspace.common.args import get
from rspace.common.exceptions import ParamError, DBError


import rspace.common.validation as validation
import rspace.lib.logger as logger
import rspace.lib.space as space_fs


LOG = '/tmp/{0}.python.log'.format(os.path.splitext(
    os.path.basename(sys.argv[0]))[0])


def check_space(fs, local_host, remote_host):
    try:
        free = space_fs.avaliable(fs)
    except OSError as err:
        conf.log.critical("Can't get free space in {0}, "
                          "error: {1}".format(fs, err))
        sys.exit(2)

    try:
        conf.log.info('Avaliable local space (df) in '
                      '{0}: {1}'.format(fs, space_fs.df(fs)))
    except ParamError as err:
        free = 0
        conf.log.warning(err)

    conf.log.info('Host: {0} .Avaliable local space '
                  'in {1}: {2} {3:0.2f} GBs'.format(local_host,
                                                    fs,
                                                    free,
                                                    free/1024/1024/1024))

    if local_host != remote_host:
        try:
            free = space_fs.avaliable(fs, host=remote_host)
        except ParamError as err:
            free = 0
            conf.log.warning(err)

        conf.log.info('Host: {0} .Avaliable remote space '
                      'in {1}: {2} {3:0.2f} GBs'.format(remote_host,
                                                        fs,
                                                        free,
                                                        free/1024/1024/1024))
    return None


def check_db_space(dbids):

    import rspace.db.mysqlm as db

    for dbid in dbids:
        try:
            db_conn = db.connect(dbid)
        except DBError as err:
            conf.log.critical("Can't connect to {0}: {1}".format(dbid, err))
            continue

        conf.log.info('Connected to {0}'.format(dbid))

        try:
            rows = db.avaliable_space(db_conn)
        except DBError as err:
            conf.log.critical(err)
        else:
            for database, table, total in rows:
                print '{0:30s} {1:30s} {2}'.format(database, table, total)
    return None


def main():

    sys.tracebacklimit = 0
    fs, host, databases, mails = get()

    sys.tracebacklimit = 1000

    conf.log = logger.setup_logger('resp_logger', LOG)

    local_host = socket.gethostname()

    conf.log.info('Parameter validation ok')
    conf.log.info('OS: {0}'.format(platform.system()))
    conf.log.info('host: {0}'.format(host))
    conf.log.info('local_host: {0}'.format(local_host))
    conf.log.debug('fs: {0}'.format(fs))
    conf.log.debug('databases: {0}'.format(databases))
    conf.log.debug('mails: {0}'.format(mails))

    check_space(fs, local_host, host)

    if databases is not None:
        check_db_space(databases)

    return None

if __name__ == "__main__":
    main()

