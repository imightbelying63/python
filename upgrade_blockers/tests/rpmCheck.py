"""this tests to ensure that RPM is working by installing and removing a simple rpm.
   I'll use yum; yum working implies a healthy rpm db
"""

if __name__ == "__main__":
    import subprocess

def rpmCheck():
    #test_rpm = 'sl' #DO NOT USE IN PRODUCTION, sl IS IN EPEL
    #built a test rpm for myself
    #test_rpm = 'http://45.55.22.33:8063/kh-upgrade_blockers-test-1.0-1.noarch.rpm'
    test_rpm = 'test-package2'

    if subprocess.getstatusoutput('yum -y --quiet install sl')[0] == 0:
        if subprocess.getstatusoutput('yum -y --quiet remove sl')[0] == 0:
            return True

    return False

if __name__ == "__main__":
    print(rpmCheck())
