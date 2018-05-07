"""catface.jpg [8:45 AM]
I would like an extended "dig" tool, something where you put in say a domain and it says where it resolves, where mail is, who has authoritative nameservers, NS records, who owns the IP, what reverse IP is, etc
"""

import dns.resolver as resolver
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("domain", help="domain to grope for")
args = parser.parse_args()
