# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""

import cx_Oracle

import rspace
from rspace.lib.auth import decode_pass
from rspace.common.exceptions import DBError


USER = 'pycones'
DOMAIN = '.domdesa'
SECRET = '{0}/secret/pass.ssl'.format(rspace.__ppath__)
PRIV = '{0}/secret/pycones.priv'.format(rspace.__ppath__)


def credential():
    return "{0}/{1}".format(USER, decode_pass(SECRET, PRIV))


def connect(dbid):

    strconn = '{0}@{1}{2}'.format(credential(), dbid, DOMAIN)
    try:
        oracle = cx_Oracle.connect(strconn)
    except cx_Oracle.DatabaseError as err:
        err, = err.args
        raise DBError(str(err.message).rstrip())

    return oracle


def avaliable_space(db_conn):

    sql = """
    SELECT FREE.tablespace_name AS "TABLESPACE",
           ROUND(FREE.free_bytes / 1024 / 1024) AS "FREEMB",
           ROUND(TOTAL.total_bytes / 1024 / 1024) AS "TOTALMB",
           ROUND((TOTAL.total_bytes -
                  FREE.free_bytes) / TOTAL.total_bytes * 100) AS "PERCENT"
      FROM (SELECT b.tablespace_name, SUM(a.bytes) free_bytes
              FROM dba_free_space A, dba_tablespaces B
             WHERE b.tablespace_name = a.tablespace_name
             GROUP BY b.tablespace_name) FREE,
           (SELECT tablespace_name, SUM(bytes) total_bytes
              FROM dba_data_files
             GROUP BY tablespace_name) TOTAL
     WHERE FREE.tablespace_name = TOTAL.tablespace_name
     ORDER BY "PERCENT" desc"""

    cursor = db_conn.cursor()

    try:
        cursor.execute(sql)
    except cx_Oracle.DatabaseError as err:
        err, = err.args

        if err.code == 942:
            raise DBError('You do not have enough access privileges '
                          'for this operation.')
        else:
            raise DBError(err.message)

    return cursor
