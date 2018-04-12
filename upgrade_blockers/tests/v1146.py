"""tests for upgrading to 11.46:
   + frontpage extensions must be removed
    * https://documentation.cpanel.net/display/CKB/11.46+FrontPage+Update+Blocker
   + The cpanel-php53 RPM target must be not be set to installed in 
     /var/cpanel/rpm.versions.d/local.versions
"""

import os

def v1146():
    pass

if __name__ == "__main__":
    print(v1146())
