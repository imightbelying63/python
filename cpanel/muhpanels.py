"""Collection of cPanel related commands but wrapped in python for ease of use.
    Python 2 compatible because most cPanel servers default to python2

   TODO: add pecl handling in EA4
   TODO: show if is ea3 or 4

   This uses argparse in a slightly unconventional way by displaying positional args
   as script commands, but just parsing the input of the first positional (args.check)
   in order to control script flow
"""
import os, sys, subprocess
import argparse as ap

parser = ap.ArgumentParser()
parser._positionals.title = "Script Commands"
parser.add_argument("check", help="invoke cPanel SSP server checking util", nargs='?', default=False)
parser.add_argument("whm_backdoor", help="generates a root login session to WHM", nargs='?', default=False)
parser.add_argument("domains", help="extract domains from httpd and report if resolve locally or not", nargs='?', default=False)
args = parser.parse_args()


def cpanelCheckSsp():
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

def domains():
    RAW_DOMAINS = 'https://raw.githubusercontent.com/imightbelying63/python/master/cpanel/domains2.py'
    try:
        import domains2
    except ImportError:
        try:
           urllib.urlretrieve(RAW_DOMAINS, 'domains2.py')
           import domains2
           #clean up the downloaded files
           domains2_file = RAW_DOMAINS.split(os.path.sep)[-1]
           if os.path.exists(domains2_file):
               os.remove(domains2_file)
               if os.path.exists(domains2_file + 'c'):
                   os.remove(domains2_file + 'c')
        except:
            print 'unable to retrieve required script'    
    return None

def main():
    #work down the list of potential commands
    if args.check == "check":
        cpanelCheckSsp()
    elif args.check == 'whm_backdoor':
        whmBackdoor()
    elif args.check == 'domains':
        domains()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

