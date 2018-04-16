"""tests for upgrading to 11.46:
   + frontpage extensions must be removed
    * https://documentation.cpanel.net/display/CKB/11.46+FrontPage+Update+Blocker
   + The cpanel-php53 RPM target must be not be set to installed in 
     /var/cpanel/rpm.versions.d/local.versions
"""

import os,re

def v1146():
    v1146_specific = []

    #FP extensions
    if os.path.exists('/usr/local/frontpage/version5.0/bin/owsadm.exe'):
        v1146_specific.append("FrontPage extensions must be removed.  Use Home >> Front Page >> Uninstall FrontPage Extensions")

    #RPM target
    rpm_versions_file = '/var/cpanel/rpm.versions.d/local.versions'
    if os.path.exsts(rpm_versions_file):
        with open(rpm_versions_file) as file:
            for line in file.readlines():
                if re.search('cpanel-php53:\s+(installed)', line):
                    v1146_specific.append('cpanel-php53 RPM target set to installed in ' + rpm_versions_file + """.  Remove it with:
  /scripts/update_local_rpm_versions --del target_settings.cpanel-php53
  /scripts/check_cpanel_rpms --fix""")

    return v1146_specific

if __name__ == "__main__":
    print(v1146())
