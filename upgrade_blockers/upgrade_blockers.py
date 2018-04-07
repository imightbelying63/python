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

  Author: khughes
  Version: 0.1
"""

import os, sys, re, subprocess

#This script must be run as root
if os.geteuid() > 0:
    print("Script must run as root")
    sys.exit(1)

#tests/findCpanelVersion()
#tests/findReleaseVersion()
