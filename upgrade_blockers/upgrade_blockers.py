"""This script will check if a cPanel update is available, and if so, are there any blockers that will prevent it from proceeding.

  TODO: ensure run as root (DONE)
  TODO: verify license file
  TODO: check write-access to required file systems
  TODO: ensure rpm integrity
  TODO: plethora of version specific checks

  This will work around python3 unavailability on cent 4/5 because those are guaranteed blockers anyway

  At present, most code is separated out into single test files stored under tests/

  Current exit codes:
   1: non-root
   2: python or centos version too low



  TESTS:
    script specific:
     +  platformDepsCheck(): checks that OS is centos 6 or greater,
                           checks that python is 3

    standard checks:
     +  licenseCheck(): simply checks that a license file exists,
                      an invalid lisc implies a larger problem than the scope of this script
     + readOnlyFS(): various filesystems / dirs need to be writable
     + rpmCheck(): verifies validity of rpmdb with a yum install/remove

  Author: khughes
  Version: 0.1
"""

TESTING_MODE = 1

import os, sys
import re, subprocess, platform

#This script must be run as root
if os.geteuid() > 0:
    print("Script must run as root")
    sys.exit(1)

def platformDepsCheck():
    try:
        if float(platform.linux_distribution()[1]) < 6:
            print("CentOS 6 or above is required")
            sys.exit(2)
        if int(sys.version[:1]) < 3:
            print("Python3 is required")
            sys.exit(2)
    except:
        print("Python 3 is required")
        sys.exit(2)

"""BEGIN STANDARD CHECKS ROUTINES"""

def licenseCheck():
    if os.path.isfile("/usr/local/cpanel/cpanel.lisc"):
        return True
    else:
        return False

def readOnlyFS():
    #this could probably do more to inform which fs is unwritable
    filesystems = ['/etc',
            '/var',
            '/var/lib/rpm',
            '/var/cpanel',
            '/usr/local',
            '/usr/local/cpanel',
            '/usr/local/bin',
            '/usr/bin',
            '/tmp',
            '/var/tmp']
    for fs in filesystems:
        if not os.access(fs, os.W_OK|os.X_OK):
            return False
    return True

def rpmCheck():
    if TESTING_MODE == 1:
        #yum takes too long, im impatient
        return True
    test_rpm = 'sl' #DO NOT USE IN PRODUCTION, sl IS IN EPEL

    if subprocess.getstatusoutput('yum -y --quiet install sl')[0] == 0:
        if subprocess.getstatusoutput('yum -y --quiet remove sl')[0] == 0:
            return True

    return False

"""END STANDARD CHECKS ROUTINES"""

"""BEGIN VERSION-SPECIFIC CHECKS ROUTINES"""

"""END VERSION-SPECIFIC CHECKS ROUTINES"""

"""START TESTS"""

platformDepsCheck() #this kills processing now if not passed

standard_blockers = []
specific_blockers = []

if not licenseCheck():
    standard_blockers.append('Invalid cPanel license')
if not readOnlyFS():
    standard_blockers.append('One or more required filesystems are currently read-only.  Refer to: https://documentation.cpanel.net/display/68Docs/Upgrade+Blockers#UpgradeBlockers-Read-onlyfilesystems')
if not rpmCheck():
    standard_blockers.append('The RPM databases is corrupt, or yum is currently unusable')


"""END TESTS"""

print(standard_blockers,specific_blockers)
