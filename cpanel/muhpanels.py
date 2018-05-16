"""Collection of cPanel related commands but wrapped in python for ease of use.
    Python 2 compatible because most cPanel servers default to python2

   TODO: add pecl handling in EA4
   TODO: show if is ea3 or 4

   This uses argparse in a slightly unconventional way by displaying positional args
   as script commands, but just parsing the input of the first positional (args.check)
   in order to control script flow.  second (and maybe 3rd) positional args
   are used to pass extra parameters to the script.  this is not how argparse
   was intended to be used.
"""
import os, sys, subprocess, re
import argparse as ap

#URL for domains.py on github
RAW_DOMAINS = 'https://raw.githubusercontent.com/imightbelying63/python/master/cpanel/domains2.py'

parser = ap.ArgumentParser()
parser._positionals.title = "Script Commands"
parser.add_argument("addons", help="show all addon domains on a given cpanel account", nargs='?', default=False)
parser.add_argument("check", help="invoke cPanel SSP server checking util", nargs='?', default=False)
parser.add_argument("domains", help="extract domains from httpd and report if resolve locally or not", nargs='?', default=False)
parser.add_argument("ea_version", help='is EA3 or EA4', nargs='?', default=False)
parser.add_argument("users", help="list all cpanel user account names", nargs='?', default=False)
parser.add_argument("whm_backdoor", help="generates a root login session to WHM", nargs='?', default=False)
args = parser.parse_args()

def isEA4():
    return True if os.path.exists('/etc/cpanel/ea4/is_ea4') else False

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
    try:
        import domains2
    except ImportError:
        try:
           import urllib
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

def addonDomains(user):
    #TODO: determine if domain resolves locally or not
    addon_reg = re.compile("^addon_domains:\s*$")
    userdata_file = '/var/cpanel/userdata/'+user+'/main'
    if not os.path.exists(userdata_file):
        print 'No such user '+user
        return False

    addons = []
    set_addons = 0
    with open(userdata_file) as file:
        for line in file:
            if addon_reg.match(line):
                set_addons = 1
                continue
            if set_addons == 1:
                if "main_domain" not in line:
                    addon_dom = line.strip().split(":")[0]
                    addons.append(addon_dom)
                else:
                    set_addons = 0
    print
    if len(addons) > 0:
        print 'Addon domains for account '+ user+':'
        print
        for dom in addons:
            print dom
    else:
        print 'No addons found for account '+user
    print

def cpanelUsers():
    user_dir = '/var/cpanel/users/'
    users_list = os.listdir(user_dir)
    users_list.remove('system')
    users_list.sort()

    print ''
    print 'cPanel user accounts:'
    print ''
    for user in users_list:
        print user
    print ''

def main():
    #work down the list of potential commands
    if args.check == "check":
        cpanelCheckSsp()
    elif args.check == 'whm_backdoor':
        whmBackdoor()
    elif args.check == 'domains':
        domains()
    elif args.check == 'ea_version':
        print "EasyApache4" if isEA4() == True else 'EasyApache 3'
    elif args.check == 'addons':
        if not args.whm_backdoor:
            print "must supply cpanel account"
        else:
            addonDomains(args.whm_backdoor)
    elif args.check == 'users':
        cpanelUsers()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

