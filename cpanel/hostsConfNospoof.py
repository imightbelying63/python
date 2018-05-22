"""
    This file searches for an old directive in hosts.conf 'nospoof' and removes it
    if it's found.  otherwise, do nothing
"""

import re,os
try:
    import shutil
except:
    pass

HOSTS_CONF = '/etc/hosts.conf'
HOSTS_CONF_BAK = HOSTS_CONF+".bak"

def hostsConfNospoof():
    if not os.path.exists(HOSTS_CONF):
        print HOSTS_CONF + " does not exist.  nothing to do"
        return None

    cleaned_file = False
    
    spoof_regex = re.compile('nospoof\s+.+')
    with open(HOSTS_CONF) as conf:
        lines = conf.readlines()

    for line in lines:
        if spoof_regex.search(line.rstrip()):
            #if we can, lets make a backup copy
            try:
                shutil.copyfile(HOSTS_CONF, HOSTS_CONF_BAK)
            except:
                pass
            lines.remove(line)
            cleaned_file = True
            break

    with open(HOSTS_CONF, "w") as conf:
        for line in lines:
            conf.write(line)

    if cleaned_file:
        if os.path.exists(HOSTS_CONF_BAK):
            print "backed up original to " + HOSTS_CONF_BAK 
        print "Cleaned nospoof from " + HOSTS_CONF
    else:
        print "nospoof not found in " + HOSTS_CONF + ". nothing to do"


if __name__ == "__main__":
    hostsConfNospoof()
