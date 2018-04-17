"""test for upgrading to 11.58:
   + OS release must be 6+
    * this is technically already handled in by platformDeps() but is still
      implemented here for ease and posterity
   + 64bit systems only
   + The perl514 RPM target must not be set to installed or unmanaged
"""

import os,sys,re

def v1158():
    v1158_specific = []

    #OS and Arch
    kernel = os.uname()[2]
    release,arch = kernel.split(".")[-2:][0], kernel.split(".")[-2:][1]
    if not release == "el6" and not release == "el7":
        v1158_specific.append("CentOS 5 and below are no loner supported")
    if not arch == "x86_64" and not sys.maxsize > (2**32):
        v1158_specific.append("32-bit systems are no longer supported")

    #RPM target
    rpm_versions_file = '/var/cpanel/rpm.versions.d/local.versions'
    if os.path.exists(rpm_versions_file):
        with open(rpm_versions_file) as file:
            for line in file.readlines():
                if re.search('perl514:\s+(installed|unmanaged)', line):
                    v1158_specific.append('The perl514 RPM target is set to installed or unmanaged in ' + rpm_versions_file + """.  Remove it with:
  /scripts/update_local_rpm_versions --del target_settings.perl514
  /scripts/check_cpanel_rpms --fix

Ensure no *.versions file under /var/cpanel/rpm.versions.d/ has this set""")

    return v1158_specific if len(v1158_specific) > 0 else False

if __name__ == "__main__":
    print(v1158())
