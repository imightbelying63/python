"""curl https://ssp.cpanel.net/run | sh"""
import subprocess, sys

def cpanel_check_ssp():
    print "One moment..."
    print ""
    cmd = "curl https://ssp.cpanel.net/run -s| sh"
    ssp = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print ssp.communicate()[0]

if __name__ == "__main__":
    cpanel_check_ssp()
