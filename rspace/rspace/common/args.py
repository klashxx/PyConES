# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""

import socket
import argparse

import rspace
import rspace.common.validation as validate


def parser_generator():
    """Funcion que recoge los argumentos parseados"""

    parser = argparse.ArgumentParser(
        description='Database space inspector.',
        epilog='PyConES 2016 - Almería')

    parser.add_argument('fs',
                        help='Target filesystem.',
                        type=validate.filesystem,
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
                        choices=['pymysql', 'pyoracle', 'dev'])

    parser.add_argument('-m', '--mails',
                        action='append',
                        dest='mails',
                        type=validate.mail,
                        help='Notification mails.')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s v{0}'.format(rspace.__version__))

    return parser


def get():

    args = parser_generator().parse_args()

    if args.mails is None:
        args.mails = ['pyconesal@gmail.com']

    return args.fs, args.host, args.databases, args.mails
