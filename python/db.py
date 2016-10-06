# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""

import mysql.connector
from mysql.connector import errorcode

from auth import decode_pass
from custom_exceptions import DBError


USER = 'pycones'
SECRET = 'keys/pass.ssl'
PRIV = 'keys/pycones.priv'


def get_conf(server):

    return {'user': USER,
            'password': decode_pass(SECRET, PRIV),
            'host':  server,
            'raise_on_warnings': True,
            'connection_timeout': 5}


def connect(server):

    try:
        mysqlconn = mysql.connector.connect(**get_conf(server))
    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_CONN_HOST_ERROR:
            raise DBError("Cant't connect to {0}!".format(server))
        raise DBError(err)

    return mysqlconn


def avaliable_space(db_conn):

    sql = """SELECT
     table_schema as `Database`,
     table_name AS `Table`,
     round(((data_length + index_length) / 1024 / 1024), 2) AS `MB`
       FROM information_schema.TABLES
       WHERE data_length > 0
       ORDER BY (data_length + index_length) DESC"""

    cursor = db_conn.cursor()

    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        raise DBError(err)

    return cursor
