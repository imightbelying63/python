"""tests for updating to 11.34:
   >= Centos 5
   >= mysql 5.0

   Note: we already assume centos 5 is a blocker, and all servers are 6+ anyway
         skip checking the OS, it's handled in platformDepsCheck()
"""

from mysqlVersion import *
    

def v1134():
    v1134_specific = []
    mysql_version = mysqlVersion()

    if mysql_version < 5.0:
        v1134_specific.append("MySQL version " + str(mysql_version) + "is less than 5.0")

    return v1134_specific

if __name__ == "__main__":
    print(v1134())
