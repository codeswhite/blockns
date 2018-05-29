#!/usr/bin/python3

"""
A script that will manage, download, backup and install hosts file in order to block ads

! Requires:
*  requests
*  termcolor

# Exit codes:
* -1 => User exit
*  0 => OK
*  1 => Root required
*  2 => Couldn't download blocklist
*  3 => System unsupported
"""

import os
import shutil

from termcolor import colored


class Term:
    GOOD = colored('[+] ', 'green')
    DOT = colored('[*] ', 'cyan')
    BAD = colored('[-] ', 'red')


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
        print(Term.BAD + 'Only supported systems are Windows, Linux and Android!')
        exit(3)


BACKUP_SUFFIX = '.blocknsbackup'
HOSTS = find_hosts_file()


def download_blocklist(source):
    from requests import get

    print(Term.GOOD + 'Downloading blocklist..')
    resp = get(source)
    if resp.status_code != 200:
        print(Term.BAD + 'Bad status code received from endpoint!', resp.status_code)
        exit(2)
    return resp.text


if __name__ == '__main__':

    if os.getuid() != 0:
        print(Term.BAD + 'This program should run as root in order to edit system hosts file')
        exit(1)

    print(Term.DOT + 'Using hosts file: ' + HOSTS)


    def prompt():
        try:
            input()
            return True
        except KeyboardInterrupt:
            exit(-1)


    if os.path.isfile(HOSTS + BACKUP_SUFFIX):
        print(Term.DOT + 'Status: %s' % colored('APPLIED', 'green', attrs=['bold']))
        print(Term.DOT + 'Press %s to restore default hosts file' % colored('[ENTER]', attrs=['bold']))
        prompt()

        shutil.move(HOSTS + BACKUP_SUFFIX, HOSTS)
        print(Term.GOOD + 'Blocklist restored successfully!')

    else:
        print(Term.DOT + 'Status: %s' % colored('NOT APPLIED', 'red', attrs=['bold']))
        print(Term.DOT + 'Press %s to download and install system DNS ad blocker' % colored('[ENTER]', attrs=['bold']))
        prompt()

        shutil.copy(HOSTS, HOSTS + BACKUP_SUFFIX)
        with open(HOSTS, 'a') as f:
            f.write('\n##### AD BLOCKER STARTS HERE\n')
            f.write(download_blocklist('https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'))
        print(Term.GOOD + 'Blocklist applied successfully!')
