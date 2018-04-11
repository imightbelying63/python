"""tests for upgrading to 11.36:
   + >= 1.6GB available in /usr/local/cpanel
   + /usr/local/cpanel/scripts/sysup is disabled
   + any of the following are not automatic or inherit in /etc/cpupdate.conf:
     * mysql
     * courier
     * dovecot
     * ftp
     * nsd
     * mydns
     * exim
     * bandmin
     * python
   + if EXIMUP is set to never, /var/cpanel/exim.unmanaged must exist
"""

import os,re

def v1136():
    pass

if __name__ == "__main__":
    print(v1136())
