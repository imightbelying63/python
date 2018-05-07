"""generates a one-time use root login session for whm"""
import subprocess

def whmBackdoor():
    cmd = "whmapi1 create_user_session user=root service=whostmgrd locale=en | grep url:"
    whmapi = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print whmapi.communicate()[0]
    return None

if __name__ == "__main__":
    whmBackdoor()
