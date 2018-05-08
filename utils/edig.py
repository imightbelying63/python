"""catface.jpg [8:45 AM]
I would like an extended "dig" tool, something where you put in say a domain and it says where it resolves, where mail is, who has authoritative nameservers, NS records, who owns the IP, what reverse IP is, etc
"""

import sys, socket
try:
    import dns.resolver as resolver
except ModuleNotFoundError:
    try:
        import pip
        pip.main(['install', 'dnspython'])
        import dns.resolver as resolver
    except:
        print('python dns package not found or able to be installed.  install: "dnspython" using pip or your package manager')
        sys.exit(1)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("domain", help="domain to grope for", nargs=1)
args = parser.parse_args()

#maybe add logic to validate that its a real FQDN
DOMAIN = args.domain[0]

ip = socket.gethostbyname(DOMAIN)

my_resolver = resolver.Resolver()
a_query = my_resolver.query(DOMAIN, "A")
print("IP address(es):")
for rdata in a_query:
    print(rdata.address)
print("")
mx_query = my_resolver.query(DOMAIN, "MX")
print("Mail Exchange:")
for rdata in mx_query:
    print(rdata)
print("")
ns_query = my_resolver.query(DOMAIN, 'NS')
print("Nameservers:")
for rdata in ns_query:
    print(rdata)
print("")
rev_ip = '.'.join(reversed(ip.split('.'))) + ".in-addr.arpa"
ptr_q = my_resolver.query(rev_ip, 'PTR')
print("PTR record:")
for rdata in ptr_q:
    print(rdata)
