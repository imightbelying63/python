#!/bin/env python
"""cpanel lacks a cli for scripting thru moving accounts, eg home1 -> home2
   this handles that"""

import os,re,sys,errno,subprocess

CONST_NAME = "wwwacct.conf"

def displayUsage():
    print('Usage: ' + os.path.basename(__file__) + ' account homepart')
    print
    print('account: name of cPanel account to move')
    print('homepart: the home partition (without trailing slash) that you will be moving the account TO')
    print
    print('Ex: Moving account1 from /home to /home2: ' + os.path.basename(__file__) + ' account1 home2')

def prepareToRun(account, homepart):

    #we rely on /etc/wwwacct.conf
    try:
        os.lstat(CONST_NAME)
    except Exception:
        print('Caught error: ' + repr(os.strerror(errno.ENOENT)) + ' ' + CONST_NAME)
        exit(2)

    #we need to test that the account exists
    if(len(account) <= 0):
        displayUsage()
        sys.exit(1)

    WHMACCNT = subprocess.Popen((["whmapi1", "listaccts", "searchmethod=exact", "search="+account, "searchtype=user"]), stdout=subprocess.PIPE)
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.check_call(('grep' , 'uid'), stdout=FNULL, stdin=WHMACCNT.stdout)
    except:
        print "Account " + account + " does not exist.  exiting"
        sys.exit(3)

    #is supplied homepart a valid homedir match?
    for line in open(CONST_NAME):
        if "HOMEMATCH" in line:
            hmatch = line.split(" ")[1]
            #print "hmatch.rstrip: " + hmatch.rstrip("\n") + " and homepart: " + homepart
            if not re.match(hmatch.rstrip("\n"), homepart):
                print "Supplied partition '"+homepart+"' is not valid"
                exit(6)

    #valid homepart


    #account exists; make sure its not already under /homepart
    FULLBASE = "/"+homepart+"/"+account
    try:
        if(os.lstat(FULLBASE)):
            print "Account already exists at: " + FULLBASE
        sys.exit(4)
    except OSError:
        basepart = "/"+homepart
        if os.path.isdir(basepart):
            print "Account will be moved to: " + FULLBASE
        else:
            print basepart + " does not exist.  cannot continue"
            exit(5)
    

def doAccountMove():

    print "time to move"



try:
    len(sys.argv[1])
except:
    displayUsage()
    sys.exit(1)

accountname=sys.argv[1]
homepart=sys.argv[2]

prepareToRun(accountname, homepart)
doAccountMove()
