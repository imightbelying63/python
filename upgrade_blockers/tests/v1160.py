"""tests for 1160:
   + SNI webserver Apache (httpd) 2.2.12, Litespeed 4.1, or Openlitespeed 1.4.12 or greater
    * this will only handle apache, our lsws installs are almost always 5.0 anyway
"""

import subprocess,os

def v1160():
    v1160_specific = []

    #SNI check
    #only test for apache, our lsws installs are all 5.0. customer-supplied lsws is not supported
    #apache 2.2.12 implies SNI

    #check if httpd or lshttpd
    web_servers = ['httpd', 'lshttpd']
    cmd = "netstat -tlpn|grep :80|head -1|awk '{print $7}'|cut -d/ -f2"
    nstat = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    server = nstat.communicate()[0].decode().rstrip()
    if server in web_servers:
        if server == web_servers[0]:
            #apache
            if os.path.exists('/etc/cpanel/ea4/is_ea4'):
                #ea4 implies apachectl
                cmd = "apachectl -V|head -1|cut -d/ -f2|awk '{print $1}'"
            else:
                #ea3 implies httpd
                cmd = "httpd -V|head -1|cut -d/ -f2|awk '{print $1}'"
            httpd = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            #python2 note: remove the decode() here:
            server_version = httpd.communicate()[0].decode().rstrip().split(".")
            if int(server_version[1]) < 4:
                if int(server_version[2]) < 12:
                    v1160_specific.append("Apache is too old, SNI unsupported.  Upgrade to 2.2.12 or greater")
        elif server == web_servers[1]:
            #lsws
            v1160_specific.append("Litespeed in use! Manually check that it supports SNI (4.1+)")
    else:
        v1160_specific.append("No listening web server on port 80")

    return v1160_specific

if __name__ == "__main__":
    print(v1160())
