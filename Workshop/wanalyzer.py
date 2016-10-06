# -*- coding: utf-8 -*-
"""
Workshop Python for System administration

psutil

PyConES 2016 Almería
"""

__author__ = 'Juan Diego Godoy Robles'
__version__ = '0.1'

import re
from datetime import datetime, timedelta
from flask import Flask, flash, redirect, render_template, request
import psutil
import platform


class State(object):

    def __init__(self):
        self.host_name = None
        self.system = None
        self.release = None
        self.version = None
        self.machine = None
        self.processor = None
        self.cpu_count = None
        self.virtual_memory = None
        self.swap_memory = None
        self.partitions = []
        self.users = []
        self.processes = []

        return None

    def host(self):

        self.host_name = platform.node()
        self.system = platform.system()
        self.release = platform.release()
        self.version = platform.version()
        self.machine = platform.machine()
        self.processor = platform.processor()
        self.cpu_count = psutil.cpu_count()
        self.virtual_memory = psutil.virtual_memory()
        self.swap_memory = psutil.swap_memory()

        return None

    def disk_info(self):

        for partition in psutil.disk_partitions():
            ocupation = psutil.disk_usage(partition.mountpoint).percent
            self.partitions.append({'device': partition.device,
                                    'mount': partition.mountpoint,
                                    'ocupation': ocupation,
                                    'type': partition.fstype,
                                    'opts': partition.opts})
            return None

    @staticmethod
    def unix_time2str(unix_time, mask='%Y/%m/%d %H:%M:%S'):
        return datetime.fromtimestamp(unix_time).strftime(mask)

    def user_info(self):

        for user in psutil.users():
            self.users.append({'name': user.name,
                               'terminal': user.terminal,
                               'started': self.unix_time2str(user.started),
                               'host': user.host})
            return None


    @staticmethod
    def duration(unix_time):
        tot = abs(datetime.now() - datetime.fromtimestamp(unix_time))
        return str(timedelta(seconds=(tot.seconds + tot.days * 24 * 3600)))


    def process_info(self, pid):
        """Process info"""
        for pr in psutil.process_iter():
            if pid is not None and int(pid) == pr.pid:
                try:
                    memory_info = pr.memory_info()
                except:
                    memory_info = None
                try:
                    open_files = pr.open_files()
                except:
                    open_files = None
                try:
                    threads = pr.threads()
                except:
                    threads = None
                try:
                    connections = pr.connections()
                except:
                    connections = None

                self.processes.append({'name': pr.name(),
                                       'user': pr.username(),
                                       'term': pr.terminal(),
                                       'status': pr.status(),
                                       'time': self.duration(pr.create_time()),
                                       'cmd': pr.cmdline(),
                                       'memory': memory_info,
                                       'open_files': open_files,
                                       'threads': threads,
                                       'connections': connections})
        return None


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        data=[{'name': 'disk'}, {'name': 'users'}, {'name': 'state'}])


@app.route("/analyzer", methods=['GET', 'POST'])
def analyzer():
    action = request.form.get('comp_select')

    data = State()

    if action == 'state':
        data.host()
    elif action == 'disk':
        data.disk_info()
    elif action == 'users':
        data.user_info()

    return render_template('{0}.html'.format(action), data=data)

@app.route("/pid", methods=['POST'])
def pid():
    pid_numer = request.form['pid']

    data = State()
    data.process_info(pid_numer)
    return render_template('pid.html', data=data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_500(e):
    return render_template('404.html'), 500



if __name__ == '__main__':
    app.run()

