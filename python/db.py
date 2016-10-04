# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""

import cx_Oracle

from auth import decode_pass


USER = 'pycones'
DOMAIN = '.domdesa'
SECRET = './pass.ssl'
PRIV =  './pycones.priv'


def get_pass():
    return decode_pass(SECRET, PRIV)


def connect(log, dbid):

    try:
        oracle = cx_Oracle.connect('{0}/{1}@{2}{3}'.format(USER,
                                                           get_pass(),
                                                           dbid,
                                                           DOMAIN))
    except cx_Oracle.DatabaseError as err:
        err, = err.args
        try:
            sql_error_code = err.code
        except AttributeError:
            sql_error_code = 'Unknow'

        try:
            sql_error_context = err.context
        except AttributeError:
            sql_error_context = 'Unknow'

        try:
            sql_error_msj = str(err.message).rstrip()
        except AttributeError:
            sql_error_msj = err

        log.error('sql_error_code: '
                   '{0}'.format(str(sql_error_code)))
        log.error('sql_error_context: '
                   '{0}'.format(str(sql_error_context)))
        log.error('sql_error_msj: '
                   '{0}'.format(str(sql_error_msj)))

        return None

    return oracle


def avaliable_space(log, db_conn):

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
            log.error('You do not have enough access privileges '
                      'for this operation.')
        else:
            log.error(err.message)

        return None

    return cursor


