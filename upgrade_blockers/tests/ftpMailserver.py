"""tests for the existance of ftpserver and mailserver in
    /var/cpanel/cpanel.config
"""

import re, os

def ftpMailserver():
    ftp_mailserver = []

    conf_file = '/var/cpanel/cpanel.config'
    ftp_regex = '(ftpserver=)\s*(pure\-ftpd|proftpd)'
    mail_regex = '(mailserver=)\s*(dovecot|courier)'
    ftp_is_set = False
    mailserver_is_set = False
    with open(conf_file) as conf:
        for line in conf.readlines():
            ftp_match = re.search(ftp_regex, line)
            #valid configs are pure-ftpd or proftpd
            if ftp_match.groups()[1] == "pure-ftpd" or ftp_match.groups()[1] == "proftpd":
                ftp_is_set = True
            mail_match = re.search(mail_regex, line)
            #valid configs are dovecot or courier
            if mail_match.groups()[1] == "dovecot" or mail_match.groups()[1] == "courier":
                mailserver_is_set = True

    if not ftp_is_set:
        ftp_mailserver.append("The ftpserver value in " + conf_file + " is invalid. Valid values are pure-ftpd or proftpd.")
    if not mailserver_is_set:
        ftp_mailserver.append("The mailserver value in " + conf_file + " is invalid. Valid values are dovecot or courier")

    return ftp_mailserver

if __name__ == "__main__":
    print(ftpMailserver())
