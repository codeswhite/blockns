#!/usr/bin/python3

"""
A script that will download, backup and install hosts file in order to block ads globally

! Requires:
*  requests
*  termcolor

# Exit codes:
* -1 => User exit
*  0 => OK
*  1 => Root required
*  2 => Couldn't download blocklist
*  3 => System unsupported

~=~ TODO
* Add a configuration file which will contain preferred blocklist source(s)
* Implement argument parsing via argparse
"""

import os
import shutil


class Term:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    GOOD = OKGREEN + '[+] ' + ENDC
    DOT = OKBLUE + '[*] ' + ENDC
    BAD = FAIL + '[-] ' + ENDC


def pr(text, m):
    print(getattr(Term, m) + text)


def prompt():
    try:
        input()
        return True
    except KeyboardInterrupt:
        exit(-1)


def find_hosts_file():
    # Determine by OS
    from platform import system
    sys = system()
    if sys == 'Linux':
        return '/etc/hosts'
    elif sys == 'Android':
        return '/system/etc/hosts'
    else:
        pr('Only supported systems are Linux and Android!', 'BAD')
        exit(3)


def download_blocklist():
    from urllib.request import urlopen
    from time import time

    pr('Connecting to: %s' % source, 'GOOD')
    data = []
    last_time = time()
    with urlopen(source) as stream:
        pr('Connection took %f seconds' % (time() - last_time), 'DOT')
        pr('Downloading blocklist..', 'GOOD')
        last_time = time()
        for line in stream:
            data.append(line.decode())
        pr('%s lines downloaded in %f seconds' % (len(data), time() - last_time), 'DOT')
    return ''.join(data)


if __name__ == '__main__':

    if os.getuid() != 0:
        pr('This program should run as root in order to edit system hosts file', 'BAD')
        exit(1)

    backup_suffix = '.blocknsbackup'
    source = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'

    hosts = find_hosts_file()
    pr('Using hosts file: ' + hosts, 'DOT')

    if os.path.isfile(hosts + backup_suffix):
        pr('Status: %s' % (Term.OKGREEN + Term.BOLD + 'APPLIED' + Term.ENDC), 'DOT')
        pr('Press [ENTER] to restore default hosts file', 'DOT')
        prompt()

        shutil.move(hosts + backup_suffix, hosts)
        pr('Blocklist restored successfully, probably a restart is required!', 'GOOD')

    else:
        pr('Status: %s' % (Term.FAIL + Term.BOLD + 'NOT APPLIED' + Term.ENDC), 'DOT')
        pr('Press [ENTER] to download and install system DNS ad blocker', 'DOT')
        prompt()

        shutil.copy(hosts, hosts + backup_suffix)
        with open(hosts, 'a') as f:
            f.write('\n##### AD BLOCKER STARTS HERE\n')
            f.write(download_blocklist())
        pr('Blocklist applied successfully, probably a restart is required!', 'GOOD')
