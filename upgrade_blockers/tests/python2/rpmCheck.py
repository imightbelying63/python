"""this tests to ensure that RPM is working by installing and removing a simple rpm.
   I'll use yum; yum working implies a healthy rpm db
"""

import subprocess

def rpmCheck():
    #test_rpm = 'sl' #DO NOT USE IN PRODUCTION, sl IS IN EPEL 
    #might be wise to write and deploy my own sample RPM
    test_rpm = 'test-package2'

    cmd1 = "yum -y --quiet install " + test_rpm
    cmd2 = "yum -y --quiet remove " + test_rpm

    rpm1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if not rpm1.communicate()[1]:
        rpm2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not rpm2.communicate()[1]:
            #rpm check successfull
            return True


    return False

if __name__ == "__main__":
    print(rpmCheck())