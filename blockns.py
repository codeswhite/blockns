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
from platform import system


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


SYS = system()


def pr(text, m):
    if SYS == 'Windows':
        print(text)
    else:
        print(getattr(Term, m) + text)


def find_hosts_file():
    # Determine by OS
    if SYS == 'Linux':
        return '/etc/hosts'
    elif SYS == 'Windows':
        return 'c:\Windows\System32\Drivers\etc\hosts'
    elif SYS == 'Android':
        return '/system/etc/hosts'
    else:
        pr('Only supported systems are Windows, Linux and Android!', 'BAD')
        exit(3)


BACKUP_SUFFIX = '.blocknsbackup'
HOSTS = find_hosts_file()


def download_blocklist(source):
    from requests import get

    pr('Downloading blocklist from: %s' % source, 'GOOD')
    resp = get(source)
    if resp.status_code != 200:
        pr('Bad status code received from endpoint: %d' % resp.status_code, 'BAD')
        exit(2)
    return resp.text


def root_check():
    import ctypes 

    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def prompt():
    try:
        input()
        return True
    except KeyboardInterrupt:
        exit(-1)


if __name__ == '__main__':

    if not root_check():
        pr('This program should run as root in order to edit system hosts file', 'BAD')
        exit(1)

    pr('Using hosts file: ' + HOSTS, 'DOT')

    if os.path.isfile(HOSTS + BACKUP_SUFFIX):
        if SYS != 'Windows':
            pr('Status: %s' % (Term.OKGREEN + Term.BOLD + 'APPLIED' + Term.ENDC), 'DOT')
        else:
            print('Status: APPLIED')
        pr('Press [ENTER] to restore default hosts file', 'DOT')
        prompt()

        shutil.move(HOSTS + BACKUP_SUFFIX, HOSTS)
        pr('Blocklist restored successfully, probably a restart is required!', 'GOOD')

    else:
        if SYS != 'Windows':
            pr('Status: %s' % (Term.OKGREEN + Term.BOLD + 'NOT APPLIED' + Term.ENDC), 'DOT')
        else:
            print('Status: NOT APPLIED')
        pr('Press [ENTER] to download and install system DNS ad blocker', 'DOT')
        prompt()

        shutil.copy(HOSTS, HOSTS + BACKUP_SUFFIX)
        with open(HOSTS, 'a') as f:
            f.write('\n##### AD BLOCKER STARTS HERE\n')
            f.write(download_blocklist('https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'))
        pr('Blocklist applied successfully, probably a restart is required!', 'GOOD')
