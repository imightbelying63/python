"""This script will check if a cPanel update is available, and if so, are there any blockers that will prevent it from proceeding.

  TODO: probably remove any testing related code
  TODO: test on live systems

  There is a version for python2 and python3.  if python3 is an uncertainty
   default to python2

  All version specific routines are written under tests/ with python2 versions under
   tests/python2

  Current exit codes:
   0: no blocking issues detected
   1: non-root
   2: centos version too low

  Details of tests have been moved to https://github.com/imightbelying63/python/blob/master/upgrade_blockers/README
  
  Author: khughes
  Version: 0.1
  Script format: python3
"""

TESTING_MODE = 0 #remove any testing mode code

import os, sys
import re, subprocess, platform, argparse

parser = argparse.ArgumentParser(description="Iterates over all possible cPanel update blockers, and informs when one is present")
parser.add_argument("--skip-rpm-check", help="RPM check adds wait time, if you're positive RPM is working, skip this to increase the speed at which this script runs", action="store_true")
group = parser.add_mutually_exclusive_group()
group.add_argument("--raw", help="Doesn't attempt to fill the customer reply in, simply delivers the output of any given blocker.", action="store_true")
group.add_argument("--format", help="Formats the output into a pre-canned text blurb.  This is the default.", action="store_true")

args = parser.parse_args()

#This script must be run as root
if os.geteuid() > 0:
    print("Script must run as root")
    sys.exit(1)

def getHostname():
    return os.uname()[1]

def getCpanelVersion():
    version_file = '/usr/local/cpanel/version'
    if os.path.exists(version_file):
       #this is the easiest and preferred method
        with open(version_file) as file:
            version = file.readlines()[0].rstrip().split('.')
            version = '.'.join(version[:2])
    else:
        if os.path.exists('/usr/sbin/whmapi1'):
            cmd = "/usr/sbin/whmapi1 version|grep -m1 version|awk '{print $2}'|cut -d. -f1,2"
            version = sp.Popen(cmd, stdout=sp.PIPE, shell=True)
            version = version.communicate()[0].decode().rstrip()
    return version if version else "cPanel too old to reliably determine version"

def mysqlVersion():
    version = subprocess.getstatusoutput('mysqladmin version|grep -i "server version"')[1].expandtabs().split()[2]
    return float(''.join(version[:3]))

def preCannedReply(standard=[], specific=[]):
    cpanel_version = getCpanelVersion()
    hostname = getHostname()

    #build the strings for each blockers
    standard_string = str()
    specific_string = str()
    if len(standard) > 0:
        for fail in standard:
           standard_string += "- " + fail + "\n"
    if any(specific):
       for fail in specific:
           if not fail == False:
               for i in fail:
                   specific_string += "- " + i + "\n"  
        
    return """Hello,

This ticket is to notify you that your server %s is currently running cPanel version %s which is out of date and has not been receiving updates.

In the past year alone cPanel has discovered and patched more than thirty potential vulnerabilities of various levels of severity. The majority of these vulnerabilities were self-reported and therefore not a threat at the time, however because they have since been disclosed there is an elevated potential that these exploits could be used against outdated versions of the software, potentially resulting in your server itself or the sites that it hosts becoming compromised.

Because of these concerns, Liquid Web will be adopting a new policy within the next few months where our first step in troubleshooting any issue will be to ensure that the version of cPanel being used is in date, and providing assistance with the update process if it is not.

It looks like these updates are currently being held back by:

%s
%s
However it's possible that there will be other changes that need to be made along the way in order to get you to the most current version. Most of these blockers are easy enough to fix such as missing configuration options, but occasionally in order to move forward with updates, larger changes will need to be made as well.

Given the concerns listed above, would it be acceptable for us to begin addressing these issues and performing the updates necessary to get your server on a currently supported version of cPanel?""" % (hostname, cpanel_version, standard_string, specific_string)

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
    test_rpm = 'test-package2' #this is in http://syspackages.sourcedns.com/packages/stable/generic/noarch/

    #skip rpm section for testing
    if args.skip_rpm_check: return True

    if subprocess.getstatusoutput('yum -y --quiet install ' + test_rpm)[0] == 0:
        if subprocess.getstatusoutput('yum -y --quiet remove ' + test_rpm)[0] == 0:
            return True

    return False

def ftpMailserver():
    ftp_mailserver = []

    conf_file = '/var/cpanel/cpanel.config'
    ftp_regex = '(ftpserver=)\s*(pure\-ftpd|proftpd)$'
    mail_regex = '(mailserver=)\s*(dovecot|courier)$'
    ftp_is_set = False
    mailserver_is_set = False
    with open(conf_file) as conf:
        for line in conf.readlines():
            if re.search(ftp_regex, line):
                #valid configs are pure-ftpd or proftpd
                ftp_match = re.search(ftp_regex, line)
                if ftp_match.groups()[1] == "pure-ftpd" or ftp_match.groups()[1] == "proftpd":
                    ftp_is_set = True
            if re.search(mail_regex, line):
                mail_match = re.search(mail_regex, line)
                #valid configs are dovecot or courier
                if mail_match.groups()[1] == "dovecot" or mail_match.groups()[1] == "courier":
                    mailserver_is_set = True

    if not ftp_is_set:
        ftp_mailserver.append("The ftpserver value in " + conf_file + " is invalid. Valid values are pure-ftpd or proftpd.")
    if not mailserver_is_set:
        ftp_mailserver.append("The mailserver value in " + conf_file + " is invalid. Valid values are dovecot or courier")

    return ftp_mailserver if len(ftp_mailserver) > 0 else False

"""END STANDARD CHECKS ROUTINES"""

"""BEGIN VERSION-SPECIFIC CHECKS ROUTINES"""

def v1134():
    v1134_specific = []
    mysql_version = mysqlVersion()

    if mysql_version < 5.0:
        v1134_specific.append("MySQL version " + str(mysql_version) + "is less than 5.0")

    return v1134_specific if len(v1134_specific) > 0 else False

def v1136():
    v1136_specific = []

    #disk space

    stat = os.statvfs('/usr/local/cpanel')
    free = (stat.f_bfree*stat.f_bsize) / (1024**3) #converts to GB
    if free < 1.6:
        v1136_specific.append("Insufficient space under /usr/local/cpanel. " + free + "GB available, 1.6GB required")

    #services check
    cpupdate_conf = '/etc/cpupdate.conf'
    services = ['MYSQLUP', 'COURIERUP', 'DOVECOTUP', 'FTPUP', 'NSDUP', 'MYDNSUP', 'EXIMUP', 'BANDMINUP', 'PYTHONUP', 'SYSUP']
    with open(cpupdate_conf) as conf:
        for line in conf.readlines():
            for srv in services[:]:
                if srv+"=inherit" in line or srv+"=daily" in line:
                    services.remove(srv)
    #items left in services[] are either never/manual or not present at all
    #we need to remove anything not present as this is assumed to auto
    for srv in services[:]:
        if subprocess.getstatusoutput('grep '+srv+' '+cpupdate_conf)[0] > 0:
            services.remove(srv)
    #items left now are blocking
    for srv in services[:]:
        #if EXIMUP is one, check for /var/cpanel/exim.unmanaged
        if srv == "EXIMUP":
            if os.path.exists('/var/cpanel/exim.unmanaged'):
                services.remove(srv)
            else:
                v1136_specific.append(srv + " is set to manual or never in " + cpupdate_conf + ". Use WHM to set to automatic or touch /var/cpanel/exim.unmanaged")
                continue
        else:
            v1136_specific.append(srv + " is set to manual or never in " + cpupdate_conf + ". Use WHM to set to automatic")

    return v1136_specific if len(v1136_specific) > 0 else False

def v1138():
    v1138_specific = []

    #check interchange
    if os.path.exists('/usr/local/cpanel/bin/startinterchange') or os.path.exists('/etc/interchangeisevil'):
        if not os.path.exists('/etc/interchangedisable'):
            v1138_specific.append('Interchange must be disabled.  Do so in Tweak Settings')

    return v1138_specific if len(v1138_specific) > 0 else False

def v1144():
    v1144_specific = []

    #test for whmxfer
    if subprocess.getstatusoutput('mysql -Bse "show databases"|grep whmxfer')[0] == 0:
        v1144_specific.append("The whmxfer must be deleted")

    return v1144_specific if len(v1144_specific) > 0 else False

def v1146():
    v1146_specific = []

    #FP extensions
    if os.path.exists('/usr/local/frontpage/version5.0/bin/owsadm.exe'):
        v1146_specific.append("FrontPage extensions must be removed.  Use Home >> Front Page >> Uninstall FrontPage Extensions")

    #RPM target
    rpm_versions_file = '/var/cpanel/rpm.versions.d/local.versions'
    if os.path.exists(rpm_versions_file):
        with open(rpm_versions_file) as file:
            for line in file.readlines():
                if re.search('cpanel-php53:\s+(installed)', line):
                    v1146_specific.append('cpanel-php53 RPM target set to installed in ' + rpm_versions_file + """.  Remove it with:
  /scripts/update_local_rpm_versions --del target_settings.cpanel-php53
  /scripts/check_cpanel_rpms --fix""")

    return v1146_specific if len(v1146_specific) > 0 else False

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

def v1160():
    v1160_specific = []

    #SNI check
    #only test for apache, our lsws installs are all 5.0. customer-supplied lsws is not supported
    #apache 2.2.12 implies SNI

    #check if httpd or lshttpd
    web_servers = ['httpd', 'lshttpd']
    cmd = "netstat -tlpn|grep :80|head -1|awk '{print $7}'|cut -d/ -f2"
    nstat = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    server = nstat.communicate()[0].decode().rstrip()
    if server in web_servers:
        if server == web_servers[0]:
            #apache
            if os.path.exists('/etc/cpanel/ea4/is_ea4'):
                #ea4 implies apachectl
                cmd = "apachectl -V|head -1|cut -d/ -f2|awk '{print $1}'"
            else:
                #ea3 implies httpd
                cmd = "httpd -V|head -1|cut -d/ -f2|awk '{print $1}'"
            httpd = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            #python2 note: remove the decode() here:
            server_version = httpd.communicate()[0].decode().rstrip().split(".")
            if int(server_version[1]) < 4:
                if int(server_version[2]) < 12:
                    v1160_specific.append("Apache is too old, SNI unsupported.  Upgrade to 2.2.12 or greater")
        elif server == web_servers[1]:
            #lsws
            v1160_specific.append("Litespeed in use! Manually check that it supports SNI (4.1+)")
    else:
        v1160_specific.append("No listening web server on port 80")

    return v1160_specific if len(v1160_specific) > 0 else False

def v1162():
    v1162_specific = []

    #mysql check
    mysql_version = mysqlVersion()
    if mysql_version < 5.5:
        v1162_specific.append("MySQL version " + str(mysql_version) + " is less than 5.5; 5.5+ is required")

    return v1162_specific if len(v1162_specific) > 0 else False

def v1168():
    v1168_specific = []

    #lsws check
    if os.path.exists('/usr/local/lsws/'):
        #only complain about it tho
        v1168_specific.append("LiteSpeed is installed, ensure it is fully upgraded before updating cpanel")
    
    #rpm check
    if os.path.exists('/etc/cpanel/ea4/is_ea4'):
        cmd = "rpm -q ea-apache24-config-runtime"
        rpm = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        runtime_version = rpm.communicate()[0].decode().rstrip()
        runtime_release_maj = int(runtime_version.split("-")[5].split('.')[0])
        if runtime_release_maj < 113:
            v1168_specific.append("The EasyApache 4 ea-apache24-config-runtime package must be version 1.0-113 or later.  Use yum update")

    return v1168_specific if len(v1168_specific) > 0 else False

"""END VERSION-SPECIFIC CHECKS ROUTINES"""

"""START TESTS"""

standard_blockers = []
specific_blockers = []

if not licenseCheck():
    standard_blockers.append('Invalid cPanel license')
if not readOnlyFS():
    standard_blockers.append('One or more required filesystems are currently read-only.  Refer to: https://documentation.cpanel.net/display/68Docs/Upgrade+Blockers#UpgradeBlockers-Read-onlyfilesystems')
if not rpmCheck():
    standard_blockers.append('The RPM databases is corrupt, or yum is currently unusable')

#begin tests that return data types rather than True/False
specific_blockers.extend( (ftpMailserver(), v1134(), v1136(), v1138(), v1144(), v1146(), v1158(), v1160(), v1162(), v1168()) )


"""END TESTS"""

"""PRINT GENERATED OUTPUT"""

#generic/standards

if not any(standard_blockers) and not any(specific_blockers):
    print("No issues found, exiting")
    sys.exit(0)

if not args.raw:
    print(preCannedReply(standard_blockers, specific_blockers))
else:
    if any(standard_blockers):
        print("Generic update blockers:\n\n")
        for fail in standard_blockers:
            print("+ " + fail)
        print("\n\n")

    if any(specific_blockers):
        print("Version specific update blockers:\n\n")
        for fail in specific_blockers:
            if not fail == False:
                for i in fail:
                    print("+ " + i)

