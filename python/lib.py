# -*- coding: utf-8 -*-
"""
PyConES 2016 Almería
"""

import os
import re
import shlex
import logging
from subprocess import Popen, PIPE

import settings
from custom_exceptions import ParamError

IDLOG = 'rspace'


def avaliable_space(fs, host=None):
    """free space checker"""

    if host is None:
        size = os.statvfs(fs)
        settings.log.warn('Esto es un test.')

        logging.getLogger(IDLOG).warn('Esto es otro test.')


        return size.f_bavail * size.f_frsize
    else:
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
           ssh.connect(host)
        except:
            raise ParamError("Can't connect to {0}.".format(host))


        _, stdout, _ = ssh.exec_command('df -P -B 1 {0}'.format(fs))
        returncode = stdout.channel.recv_exit_status()

        if returncode:
            raise ParamError('Bad exit code from df: {0}'.format(returncode))

        return int(re.search(r'(\d+)\s+\d+%', stdout.read()).group(1))


def df(fs):
    args_df = shlex.split('df -P -B 1 {0}'.format(fs))

    df_proc = Popen(args_df,  stdout=PIPE,  stderr=PIPE, preexec_fn=os.setsid)
    out, err = df_proc.communicate()

    if df_proc.returncode:
        raise ParamError('Bad exit code from df!')

    return int(re.search(r'(\d+)\s+\d+%', out).group(1))
