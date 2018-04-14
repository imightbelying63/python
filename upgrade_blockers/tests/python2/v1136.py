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
TESTING = 1

import os,subprocess

def v1136():
    v1136_specific = []

    #disk space

    stat = os.statvfs('/usr/local/cpanel')
    free = (stat.f_bfree*stat.f_bsize) / (1024**3) #converts to GB
    if free < 1.6:
        v1136_specific.append("Insufficient space under /usr/local/cpanel. " + free + "GB available, 1.6GB required")

    #services check
    cpupdate_conf = '/etc/cpupdate.conf' if not TESTING else '/root/python/upgrade_blockers/tests/testfiles/cpupdate.conf'
    services = ['MYSQLUP', 'COURIERUP', 'DOVECOTUP', 'FTPUP', 'NSDUP', 'MYDNSUP', 'EXIMUP', 'BANDMINUP', 'PYTHONUP', 'SYSUP']
    with open(cpupdate_conf) as conf:
        for line in conf.readlines():
            for srv in services[:]:
                if srv+"=inherit" in line or srv+"=daily" in line:
                    services.remove(srv)
    #items left in services[] are either never/manual or not present at all
    #we need to remove anything not present as this is assumed to auto
    for srv in services[:]:
        if subprocess.getstatusoutput('grep '+srv+' '+cpupdate_conf)[0] > 0:
            services.remove(srv)
    #items left now are blocking
    for srv in services[:]:
        #if EXIMUP is one, check for /var/cpanel/exim.unmanaged
        if srv == "EXIMUP":
            if os.path.exists('/var/cpanel/exim.unmanaged'):
                services.remove(srv)
            else:
                v1136_specific.append(srv + " is set to manual or never in " + cpupdate_conf + ". Use WHM to set to automatic or touch /var/cpanel/exim.unmanaged")
                continue
        v1136_specific.append(srv + " is set to manual or never in " + cpupdate_conf + ". Use WHM to set to automatic")

    return v1136_specific

if __name__ == "__main__":
    print(v1136())
