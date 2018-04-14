"""this tests to ensure that RPM is working by installing and removing a simple rpm.
   I'll use yum; yum working implies a healthy rpm db
"""

import subprocess

def rpmCheck():
    test_rpm = 'sl' #DO NOT USE IN PRODUCTION, sl IS IN EPEL 

    cmd1 = "yum -y --quiet install " + test_rpm
    cmd2 = "yum -y --quiet remove " + test_rpm

    rpm1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
    rpm2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)

    install = rpm1.communicate

    if subprocess.getstatusoutput('yum -y --quiet install sl')[0] == 0:
        if subprocess.getstatusoutput('yum -y --quiet remove sl')[0] == 0:
            return True

    return False

if __name__ == "__main__":
    print(rpmCheck())
