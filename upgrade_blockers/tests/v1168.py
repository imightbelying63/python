"""tests for upgrading to 68:
   + lsws 5.2.1 build 2 or later
   + if EA4, ea-apache24-config-runtime >= 1.0-113
"""

import subprocess, os

def v1168():
    v1168_specific = []

    #lsws check
    if os.path.exists('/usr/local/lsws/'):
        #only complain about it tho
        v1168_specific.append("LiteSpeed is installed, ensure it is fully upgraded before updating cpanel")
    
    #rpm check
    if os.path.exists('/etc/cpanel/ea4/is_ea4'):
        cmd = "rpm -q ea-apache24-config-runtime"
        rpm = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        runtime_version = rpm.communicate()[0].decode().rstrip()
        runtime_release_maj = int(runtime_version.split("-")[5].split('.')[0])
        if runtime_release_maj < 113:
            v1168_specific.append("The EasyApache 4 ea-apache24-config-runtime package must be version 1.0-113 or later.  Use yum update")

    return v1168_specific

if __name__ == "__main__":
    print(v1168())
