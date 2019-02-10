"""
!! Python 3 !!

A script that will download, backup and install hosts file in order to block ads globally

! Requires:
*  urllib3

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
from sys import exit

from utils import download_blocklist, prompt


def admin_priv_check():
    import ctypes
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print('[X] This program should run with administrator in order to edit system hosts file')
        exit(1)


def main():
    hosts = 'c:\\Windows\\System32\\Drivers\\etc\\hosts'
    backup_suffix = '.blocknsbackup'
    source = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'

    if not os.path.isfile(hosts):
        print('[X] This version only supports Windows!')
        exit(3)

    admin_priv_check()

    print('[*] Using hosts file: ' + hosts)

    if os.path.isfile(hosts + backup_suffix):
        print('Status: APPLIED')
        print('[*] Press [ENTER] to restore default hosts file')
        prompt()

        shutil.move(hosts + backup_suffix, hosts)
        print('[+] Blocklist restored successfully, probably a restart is required!')

    else:
        print('[Status: NOT APPLIED]')
        print('[*] Press [ENTER] to download and install system DNS ad blocker')
        prompt()

        shutil.copy(hosts, hosts + backup_suffix)
        print('[+] Fetching: %s' % source)
        data, tt = download_blocklist(source)
        print('[*] %s bytes downloaded in %f seconds' % (len(data), tt))
        with open(hosts, 'a') as f:
            f.write('\n##### BLOCKNS STARTS HERE\n')
            f.write(data)
        print('[+] Blocklist applied successfully, probably a restart is required!')


if __name__ == '__main__':
    main()
