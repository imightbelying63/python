"""tests for updating to 11.34:
   >= Centos 5
   >= mysql 5.0

   Note: we already assume centos 5 is a blocker, and all servers are 6+ anyway
         skip checking the OS, it's handled in platformDepsCheck()
"""

if __name__ == "__main__":
    import subprocess

def v1134:
    mysql_version = subprocess.getstatusoutput('mysqladmin version|grep -i "server version"')[1].split("\t")[2]
