"""this just parses and pretty-formats some short notes I was generating about certain customers.
   really i just wanted an excuse to mess around with format spec mini-lang
   """

import re
import os,sys

TICKETFILE = sys.argv[1] if len(sys.argv) > 1 else "ticketcrawl.txt"

def printHeaders():
    headers = ['date', 'ticket #', 'title', 'from', 'summary']
    print('{0:<11}{0:<10}{0:<20}{0:<10} {0:^5}'.format('-'*6))
    print('{0:<11}{1:<10}{2:<20}{3:<10} {4:^5}'.format(*headers))
    print('{0:<11}{0:<10}{0:<20}{0:<10} {0:^5}'.format('-'*6))

if not os.path.isfile(TICKETFILE):
    sys.exit('No such ticket text file: ' + TICKETFILE)

billing_line_regex = re.compile('^https:\/\/')

with open(TICKETFILE) as ticket:
    line_count = 0
    for line in ticket.readlines():
        #break out if eof to ensure pretty formatting
        if billing_line_regex.match(line):
            print(line)
            #print a new header here and reset line counter
            printHeaders()
            line_count = 0
            continue
        data = line.split('-')
        #skip newlines
        if re.match('^\n', data[0]):
            continue
        print('{0[0]:<10}{0[1]:>10}{0[2]:<20}{0[3]:<10}{0[4]}'.format(data))
        #print(data)
        line_count += 1
        if line_count == 1:
            printHeaders()
            line_count = 0
