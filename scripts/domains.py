"""This will look at all domains listed in apache httpd.conf 
   and return if it resolves to the server or not"""

from subprocess import check_output
import re
import dns.resolver
import os,sys

#server_ip_addr = os.popen('ip addr show eth0').read().split('inet ')[1].split("/")[0]
#need to have all IPs actually
ips = check_output(['hostname', '--all-ip-addresses']).decode().split(" ")[:-1]

#at some point add logic for non-cpanel servers
APACHECONF = '/etc/apache2/conf/httpd.conf'

if not os.path.isfile(APACHECONF):
    sys.exit(APACHECONF + ' does not exist; cannot proceed')

#regex tests for ServerName and ServerAlias
regex_servername = re.compile("\s*ServerName(\s)+(.*)")
regex_serveralias = re.compile("\s*ServerAlias(\s)+(.*)")
#regex for IP testing -- its a shitty regex but its sufficient here
regex_ipaddr = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

server_names = []
server_aliases = []

#test for aliases, but modprob not even use
with open(APACHECONF) as conf_file:
    for line in conf_file:
        if regex_servername.match(line):
            server_names.append(regex_servername.match(line).group(2))
        elif regex_serveralias.match(line):
            server_aliases.append(regex_serveralias.match(line).group(2).split(" "))

#filter out raw IPs, and sort into unique entries
server_names = list(set(filter(lambda x: not regex_ipaddr.match(x), server_names)))
#sort into unique entries only
#server_names = list(set(server_names))

#DNS look ups
local_domains = []
remote_domains = []
nx_domains = []
if len(server_names) == 0:
    sys.exit('No ServerNames found in ' + APACHECONF)

for domain in server_names:
    answer = []
    try:
        answer = dns.resolver.query(domain, 'A')
    except:
        nx_domains.append(domain)
        continue
    #if len(answer) == 0:
        #nx_domains.append(domain)
        #continue
    if answer[0].to_text() in ips:
        local_domains.append(domain)
    else:
        remote_domains.append(domain)

local_domains.sort()
remote_domains.sort()
nx_domains.sort()

print("Local Domains", "-"*12, sep="\n")
print("\n".join(" {1}".format(*k) for k in enumerate(local_domains)), " ", sep="\n")
print("Remote Domains", "-"*12, sep="\n")
print("\n".join(" {1}".format(*k) for k in enumerate(remote_domains)), " ", sep="\n")
print("Do not resolve", "-"*12, sep="\n")
print("\n".join(" {1}".format(*k) for k in enumerate(nx_domains)), " ", sep="\n")
