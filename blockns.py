#!/usr/bin/python3

"""

# Requires: requests

"""

from os.path import isfile


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    GOOD = OKGREEN + '[+] ' + ENDC
    DOT = OKBLUE + '[*] ' + ENDC
    BAD = FAIL + '[-] ' + ENDC

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def find_hosts_file():
    from platform import system
    sys = system()
    # Determine by OS
    if sys == 'Linux':
        return '/etc/hosts'
    elif sys == 'Windows':
        return 'c:\Windows\System32\Drivers\etc\hosts'
    elif sys == 'Android':
        return '/system/etc/hosts'
    else:
        print(bcolors.BAD + 'Only supported systems are Windows, Linux and Android!')
        exit(4)


HOSTS = find_hosts_file()
print(bcolors.DOT + 'Using hosts file: ' + HOSTS)
BACKUP_SUFFIX = '.blockerback'


def download_blocklist():
    source = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts'
    from requests import get

    print(bcolors.GOOD + 'Downloading blocklist..')
    resp = get(source)
    if resp.status_code != 200:
        print(bcolors.BAD + 'Bad status code received from endpoint!', resp.status_code)
        exit(2)
    return resp.text


def apply(text):
    from shutil import copy
    copy(HOSTS, HOSTS + BACKUP_SUFFIX)

    with open(HOSTS, 'a') as f:
        f.write('\n##### AD BLOCKER STARTS HERE\n')
        f.write(text)
    print(bcolors.GOOD + 'Blocklist applied successfully!')


def restore():
    if not isfile(HOSTS + BACKUP_SUFFIX):
        print('FATAL! no backup file found!!')
        exit(3)
    from shutil import move
    move(HOSTS + BACKUP_SUFFIX, HOSTS)
    print(bcolors.GOOD + 'Blocklist restored successfully!')


if __name__ == '__main__':

    def prompt():
        try:
            input()
            return True
        except KeyboardInterrupt:
            return False


    from os import getuid

    if getuid() != 0:
        print(bcolors.BAD + 'This program should run as root in order to edit system hosts file')
        exit(1)

    if isfile(HOSTS + BACKUP_SUFFIX):
        print(bcolors.DOT + 'Status: %sAPPLIED' % bcolors.OKGREEN + bcolors.ENDC)
        print(bcolors.DOT + 'Press [ENTER] to restore default hosts file')
        if prompt():
            restore()
    else:
        print(bcolors.DOT + 'Status: %sNOT APPLIED' % bcolors.FAIL + bcolors.ENDC)
        print(bcolors.DOT + 'Press [ENTER] to download and install system ad blocker patch')
        if prompt():
            lst = download_blocklist()
            apply(lst)
