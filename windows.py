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

import utils


def admin_priv_check():
    import ctypes
    if ctypes.windll.shell32.IsUserAnAdmin() == 0:
        print('[X] This program should run with administrator in order to edit system hosts file')
        exit(1)


def main():
    source = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts'
    hosts = 'c:\\Windows\\System32\\Drivers\\etc\\hosts'
    backup_suffix = '.blocknsbackup'

    if not os.path.isfile(hosts):
        print('[X] This version only supports Windows!')
        exit(3)

    admin_priv_check()

    print('[*] Using hosts file: ' + hosts)

    if os.path.isfile(hosts + backup_suffix):  # Backup present
        print('[Status: APPLIED]')
        print('[*] Press [ENTER] to restore default hosts file')
        utils.prompt()

        shutil.move(hosts + backup_suffix, hosts)
        print('[+] Blocklist restored successfully, probably a restart is required!')

    else:
        print('[Status: NOT APPLIED]')
        print('[*] Press [ENTER] to download and install system DNS ad blocker')
        utils.prompt()

        shutil.copy(hosts, hosts + backup_suffix)
        print('[+] Fetching %s' % source)
        data, tt = utils.download_blocklist(source)
        print('[*] %s bytes downloaded in %f seconds' % (len(data), tt))
        with open(hosts, 'wb') as f:
            f.write(data.encode('utf-8'))
        print('[+] Blocklist applied successfully, probably a restart is required!')


if __name__ == '__main__':
    main()
