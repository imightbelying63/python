"""This script will check if a cPanel update is available, and if so, are there any blockers that will prevent it from proceeding.

  TODO: ensure run as root (DONE)
  TODO: verify license file
  TODO: check write-access to required file systems
  TODO: ensure rpm integrity
  TODO: plethora of version specific checks

  This will work around python3 unavailability on cent 4/5 because those are guaranteed blockers anyway

  Current exit codes:
   1: non-root

  Author: khughes
  Version: 0.1
"""

import os, sys
import requests, re

#This script must be run as root
if os.geteuid() > 0:
    print("Script must run as root")
    sys.exit(1)

with open("/usr/local/cpanel/version") as version_file:
    cpanel_version = version_file.read()[:5]
print(cpanel_version)

def findReleaseVersion():
    tier_request = requests.get("http://httpupdate.cpanel.net/cpanelsync/TIERS")
    if tier_request.status_code == 200:
        release_regex = re.compile("^release:(.*)?")
        tier_returns = tier_request.text.splitlines()
        for tier in tier_returns:
            if release_regex.match(tier):
                release_tier_version = release_regex.match(tier).group(1)
                return release_tier_version
    else:
        return print("Unable to download cpanel tiers")
