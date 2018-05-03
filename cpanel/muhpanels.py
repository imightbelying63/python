"""Collection of cPanel related commands but wrapped in python for ease of use.
    Python 2 compatible because most cPanel servers default to python2

   TODO: add pecl handling in EA4
   TODO: show if is ea3 or 4
"""
import os, sys, subprocess
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument("check", help="invoke cPanel SSP server checking util", nargs='?', default=False)
parser.add_argument("whm_backdoor", help="generates a root login session to WHM", nargs='?', default=False)
args = parser.parse_args()


def cpanel_check_ssp():
    print "One moment..."
    print ""
    cmd = "curl https://ssp.cpanel.net/run -s| sh"
    ssp = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print ssp.communicate()[0]

def whmBackdoor():
    cmd = "whmapi1 create_user_session user=root service=whostmgrd locale=en | grep url:"
    whmapi = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print whmapi.communicate()[0]
    return None

print args.check, args.whm_backdoor
