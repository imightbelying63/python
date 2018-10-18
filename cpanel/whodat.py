import sys,re,subprocess
import dns.resolver
from os import path
from glob import glob

NORMAL = '\033[0m'
BOLD = '\033[1m'

def usage():
    print "Usage:\twhodat domain.com [--verbose]\n",

def grep(search, file, count=-1):
    output = []
    with open(file) as f:
        for line in f:
            if re.search(search, line):
                if count >= 1:
                    output.append(line)
                    count -= 1
                    continue
                elif count == 0: return output
                else:
                    output.append(line)
                    continue
        return output

    return None

# End definitions; begin main

print
domain = sys.argv[1] if len(sys.argv) > 1 else None

#Make sure a domain name has been provided
if not domain:
    print "ERROR: No domain specified!"
    usage()
    sys.exit(1)

#This is meant for cpanel only. Check if the server is a cpanel server. Exit if not.
if not path.exists('/usr/local/cpanel'):
    print "cPanel is required to use this script!"
    sys.exit(1)

#Convert any UPPERCASE to lowercase.
domain = domain.lower()

#Strip the protocol, www, and trailing slash or URI from the domain
domain = re.sub('^https?://', '', domain)
domain = re.sub('^www\.', '', domain)
domain = re.sub('/.*$', '', domain)

#detect EA version
if path.exists('/etc/cpanel/ea4/is_ea4'):
    ea_ver = 4
    apache_conf = '/etc/apache2/conf/httpd.conf'
    apachectl_command = "apachectl -M"
else:
    ea_ver = 3
    apache_conf = '/usr/local/apache/conf/httpd.conf'
    apachectl_command = "httpd -M"

#Assign a variable for the cpanel userdata, to be called for many things later on
userdatadomain = grep("^"+domain+":", "/etc/userdatadomains")[0]

#Make sure the user exists on the system. 
if userdatadomain is not None:
    cpuser = userdatadomain.split('=')[0].split(' ')[1]
    #Grab the docroot and PHP version from /etc/userdatadomains
    docroot = userdatadomain.split('=')[8]
else:
    print "ERROR: "+domain+" not found in /etc/userdatadomains"
    sys.exit(1)

#Gather PHP version based on EA4 or 3
if ea_ver == 4:
    php_ver = userdatadomain.split("=")[18] if len(userdatadomain.split("=")) > 17 else None
    #If using inherit, the above will not properly determine the version, and the php_ver var will be empty. If thats the case, just use the default:
    if (php_ver == None) or  (php_ver.strip() == 'inherit'):
        php_ver = grep('default:', '/etc/cpanel/ea4/php.conf')[0].split(' ')[1].strip()
elif ea_ver == 3:
    php = subprocess.Popen("php -v |head -1 |awk '{print $2}'", shell=True, stdout=subprocess.PIPE)
    php_ver = php.communicate()[0]

#Grabs the FPM status for the domain from whmapi1:
#https://documentation.cpanel.net/display/DD/WHM+API+1+Functions+-+php_get_vhost_versions
#Do this only if EA4
if ea_ver == 4:
    fpm = subprocess.Popen('whmapi1 php_get_vhost_versions | grep -E "(vhost:|php_fpm:)" | grep -E -B1 "vhost: '+domain+'$" | grep php_fpm | sed "s/php_fpm: 1/Enabled/" | sed "s/php_fpm: 0/Disabled/" | tr -d " "', shell=True, stdout=subprocess.PIPE)
    fpm_status = fpm.communicate()[0]

#Get the IP that WHM has configured for the domain in /etc/userdatadomains
whm_ip = userdatadomain.split('=')[10].split(':')[0]

#resolve the A record
try:
    for rdata in dns.resolver.query(domain, 'A'):
        a_record = rdata
except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
    a_record = "MISSING"

#Get the type of domain from /etc/userdatadomains. Main, sub, addon, alias.
domain_type = userdatadomain.split('=')[4]

#Check for a AAAA DNS record.
try:
    for rdata in dns.resolver.query(domain, 'AAAA'):
        AAAA_record = rdata
except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
    AAAA_record = None

#Determine the handler:
php = subprocess.Popen("/usr/local/cpanel/bin/rebuild_phpconf --current |grep '"+php_ver+"' | awk '{print $NF}' | tail -1", shell=True, stdout=subprocess.PIPE)
php_handler = php.communicate()[0]

#If EA3, $php_handler will be empty at this point, since we get the full version from php -v. Grab the handler from /usr/local/cpanel/bin/rebuild_phpconf --current
if ea_ver == 3:
    php = subprocess.Popen("/usr/local/cpanel/bin/rebuild_phpconf --current |grep 'PHP5 SAPI' | awk '{print $NF}'", shell=True, stdout=subprocess.PIPE)
    php_handler = php.communicate()[0]

#Output the info
print "Username:\t", cpuser
print BOLD+"Docroot:\t", docroot+NORMAL
print "Domain:\t\t", domain, "("+domain_type+" domain)"
print "Configured IP:\t", whm_ip
print "A Record:\t", a_record

#Only print the ipv6 AAAA records if they exist
if AAAA_record is not None:
    print "AAAA Record:\t", AAAA_record,

print "PHP Version:\t", php_ver,

#Logic to display the PHP Handler
if fpm_status.strip() == "Enabled":
    print "PHP Handler:\tPHP-FPM ", fpm_status,
elif php_handler.strip() == "dso":
    #determine if mod_ruid is in place
    if subprocess.Popen("apachectl -M 2>&1 | grep ruid", shell=True, stdout=subprocess.PIPE).communicate()[0] != '':
        ruid_status = "With Mod_RUID (PHP runs as user)"
    else:
        ruid_status = "Without Mod_RUID (PHP run as nobody, NOT the user)"
    if ea_ver == 3:
        ruid_status = subprocess.Popen('/usr/local/cpanel/bin/rebuild_phpconf --current |grep RUID2', shell=True, stdout=subprocess.PIPE).communicate()[0]
    print "PHP Handler:\tDSO ", ruid_status,
elif php_handler.strip() == "suphp":
    print "PHP Handler:\tSuPHP",
elif php_handler.strip() == "cgi":
    #determine if SuExec is in place
    if subprocess.Popen("apachectl -M 2>&1 | grep suexec", shell=True, stdout=subprocess.PIPE).communicate()[0] != '':
        suexec_status = "- With SuExec"
    else:
        suexec_status = "- WITHOUT SuExec"
    if ea_ver == 3:
        suexec_status = subproces.Popen("/usr/local/cpanel/bin/rebuild_phpconf --current |grep SUEXEC", shell=True, stdout=subprocess.PIPE).communicate()[0]
    print "PHP Handler:\tCGI ", suexec_status,
elif php_handler.strip() == "fcgi":
    #determine if SuExec is in place
    if subprocess.Popen("apachectl -M 2>&1 | grep suexec", shell=True, stdout=subprocess.PIPE).communicate()[0] != '':
        suexec_status = "- With SuExec"
    else:
        suexec_status = "- WITHOUT SuExec"
    if ea_ver == 3:
        suexec_status = subproces.Popen("/usr/local/cpanel/bin/rebuild_phpconf --current |grep SUEXEC", shell=True,     stdout=subprocess.PIPE).communicate()[0]
    print "PHP Handler:\tFast CGI ", suexec_status,
elif php_handler.strip() == "none":
    print "PHP Handler:\tNONE - Is this intended?",
    
#Check for userdata Apache includes for the domain.
#Need to check the subdomain for the include of an addon domain
if domain_type.strip() == "addon":
    include_domain = userdatadomain.split('=')[6]
else:
    include_domain = domain

active_includes = []
active_includes_list = grep(include_domain, apache_conf)
for i in active_includes_list:
    if re.match('^Include\s+.*', i.lstrip()):
        active_includes.append(i.split('"')[1])

if len(active_includes):
    for include in active_includes:
        if glob(include):
	    for glob_include in glob(include):
	        print "VHOST INCLUDE:\t", glob_include

