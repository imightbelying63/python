"""tests for upgrading to 11.44:
   + the rare occasion that whmxfer exists, it must be deleted
"""

import subprocess

def v1144():
    v1144_specific = []

    #test for whmxfer
    if subprocess.getstatusoutput('mysql -Bse "show databases"|grep whmxfer')[0] == 0:
        v1144_specific.append("The whmxfer must be deleted")

    return v1144_specific if len(v1144_specific) > 0 else False

if __name__ == "__main__":
    print(v1144())
