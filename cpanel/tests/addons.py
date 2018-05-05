"""
>>> with open('tests/main') as file:
...   for line in file:
...     if reg.match(line):
...       set_addons = 1
...       continue
...     if set_addons == 1:
...       if "main_domain" not in line:
...         addons.append(line)
...       else:
...         set_addons = 0
"""

import re,os

def addonDomains(user='imightbe'):
    addon_reg = re.compile("^addon_domains:\s*$")
    userdata_file = '/var/cpanel/userdata/'+user+'/main'
    if not os.path.exists(userdata_file): return False

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
    return addons

if __name__ == "__main__":
    print addonDomains()
