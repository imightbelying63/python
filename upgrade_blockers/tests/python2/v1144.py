"""tests for upgrading to 11.44:
   + the rare occasion that whmxfer exists, it must be deleted
"""

import subprocess

def v1144():
    v1144_specific = []

    #test for whmxfer
    cmd = "myslshow | grep whmxfer"
    mysqladmin = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not mysqladmin.communicate()[0] == '':
        v1144_specific.append("The whmxfer must be deleted")

    return v1144_specific

if __name__ == "__main__":
    print(v1144())
