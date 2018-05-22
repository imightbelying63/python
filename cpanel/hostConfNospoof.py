"""
    This file searches for an old directive in host.conf 'nospoof' and removes it
    if it's found.  otherwise, do nothing
"""

import re,os
try:
    import shutil
except:
    pass

HOST_CONF = '/etc/host.conf'
HOST_CONF_BAK = HOST_CONF+".bak"

def hostConfNospoof():
    if not os.path.exists(HOST_CONF):
        print HOST_CONF + " does not exist.  nothing to do"
        return None

    cleaned_file = False
    
    spoof_regex = re.compile('nospoof\s+.+')
    with open(HOST_CONF) as conf:
        lines = conf.readlines()

    for line in lines:
        if spoof_regex.search(line.rstrip()):
            #if we can, lets make a backup copy
            try:
                shutil.copyfile(HOST_CONF, HOST_CONF_BAK)
            except:
                pass
            lines.remove(line)
            cleaned_file = True
            break

    with open(HOST_CONF, "w") as conf:
        for line in lines:
            conf.write(line)

    if cleaned_file:
        if os.path.exists(HOST_CONF_BAK):
            print "backed up original to " + HOST_CONF_BAK 
        print "Cleaned nospoof from " + HOST_CONF
    else:
        print "nospoof not found in " + HOST_CONF + ". nothing to do"


if __name__ == "__main__":
    hostConfNospoof()
