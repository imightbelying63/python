"""tests for upgrading to 11.36:
   + >= 1.6GB available in /usr/local/cpanel
   + /usr/local/cpanel/scripts/sysup is disabled (SYSUP is never in cpupdate)
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
    v1136_specific = []

    #disk space

    stat = os.statvfs('/usr/local/cpanel')
    free = (stat.f_bfree*stat.f_bsize) / (1024**3) #converts to GB
    if free < 1.6:
        v1136_specific.append("Insufficient space under /usr/local/cpanel. " + free + "GB available, 1.6GB required")

if __name__ == "__main__":
    print(v1136())
