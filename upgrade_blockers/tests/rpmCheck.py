"""this tests to ensure that RPM is working by installing and removing a simple rpm.
   I'll use yum; yum working implies a healthy rpm db
"""

if __name__ == "__main__":
    import subprocess

def rpmCheck():
    test_rpm = 'sl' #DO NOT USE IN PRODUCTION, sl IS IN EPEL

    if subprocess.getstatusoutput('yum -y --quiet install sl')[0] == 0:
        if subprocess.getstatusoutput('yum -y --quiet remove sl')[0] == 0:
            return True

    return False

if __name__ == "__main__":
    print(rpmCheck())
