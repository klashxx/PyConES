# -*- coding: utf-8 -*-

"""
PyConES 2016 Almería
"""

import os
import re
import shlex
from subprocess import Popen, PIPE

from custom_exceptions import ParamError


def avaliable_space(fs, host=None):
    """free space checker"""

    if host is None:
        size = os.statvfs(fs)
        return size.f_bavail * size.f_frsize
    else:
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host)

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