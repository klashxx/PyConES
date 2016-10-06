#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Workshop Python for System administration

psutil

PyConES 2016 Almería
"""

__author__ = 'Juan Diego Godoy Robles'
__version__ = '0.1'


import psutil
import re
import datetime
import argparse
import pprint


def parameters():
    """parsed parameters processing"""

    parser = argparse.ArgumentParser(
                        add_help=True,
                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--pid=',
                        help='Process PID.',
                        dest='pid')

    parser.add_argument('--pattern=',
                        help='Process search pattern.',
                        dest='pattern')

    parser.add_argument('--action=',
                        help=('Accion over captured processes.'
                              'kill needs tty parameter.'),
                        choices=['info', 'kill'],
                        default='info',
                        dest='action')

    parser.add_argument('--terminal=',
                        help='Process source terminal.',
                        default=None,
                        dest='terminal')
    try:
        modif = parser.parse_args()
    except Exception, err:
        parser.error(err)

    if modif.action == 'kill' and not modif.terminal:
        parser.error('kill needs tty parameter')

    return modif


def disk_info():
    """Shown disk info on your tty"""
    for particion in psutil.disk_partitions():
        ocupacion = psutil.disk_usage(particion.mountpoint).percent
        print('device:{0:40} mount:{1:20} ocup:{2:6} tipo:{3:10} '
              'ops:{4}'.format(particion.device,
                               particion.mountpoint,
                               ocupacion,
                               particion.fstype,
                               particion.opts))


def user_info():
    """Users info"""
    for usuario in psutil.users():
        pprint.pprint(usuario)


def process_handler(pid, pattern=None, action='info', terminal=None):
    """Process info"""

    now = datetime.datetime.now()
    count = 0

    for p in psutil.process_iter():
        try:
            process_name = p.name()
        except:
            continue

        found = False
        if pid is not None and int(pid) == p.pid:
            found = True
        elif pattern is not None:
            found = re.search(pattern, process_name)

        if found:
            count += 1
            print('User:{0}'.format(p.username()))
            print('Terminal:{0}'.format(p.terminal()))
            print('Status:{0}'.format(p.status()))
            begin = datetime.datetime.fromtimestamp(p.create_time())
            total = abs(now - begin)
            seconds = (total.seconds + total.days * 24 * 3600)
            print('Time:{0}'.format(str(datetime.timedelta(seconds=seconds))))
            print('cmd:{0}'.format(p.cmdline()))
            try:
                print p.memory_info()
            except:
                pass
            try:
                pprint.pprint(p.open_files())
            except:
                pass
            try:
                pprint.pprint(p.threads())
            except:
                pass
            try:
                print p.connections()
            except:
                pass
            if action == 'kill' and p.terminal == terminal:
                try:
                    p.kill()
                except Exception as err:
                    print('Error "{0}" when '
                          'killing process'.format(str(err)))
                print('Process killed')
            print('- +' * 30)

    if not count:
        print('No processes matched')
    else:
        print('Total processes: {0:d}'.format(count))

    return None


def main():
    m = parameters()

    print('CPU Number: {0:d}'.format(psutil.cpu_count()))
    print('Memory: {0}'.format(psutil.virtual_memory()))
    print('Swap: {0}'.format(psutil.swap_memory()))
    print('-' * 100)
    print('Disk info')
    print('-' * 100)
    disk_info()
    print('-' * 100)
    print('Users')
    print('-' * 100)
    user_info()

    if m.pid or m.pattern:
        print('Processes info')
        print('-' * 100)
        process_handler(pid=m.pid,
                        pattern=m.pattern,
                        action=m.action,
                        terminal=m.terminal)

    return None


if __name__ == '__main__':
    main()
