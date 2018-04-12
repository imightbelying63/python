"""tests for upgrading to 11.38:
   + interchange must be disabled
    * as far as I can tell, /etc/interchangeisevil and /etc/interchangedisable exists if so, or neither
      do. documentation is sparse on this tho. this will also check for the existence of
      /usr/local/cpanel/bin/startinterchange
"""

import os

def v1138():
    v1138_specific = []

    #check interchange
    if os.path.exists('/usr/local/cpanel/bin/startinterchange') or os.path.exists('/etc/interchangeisevil'):
        if not os.path.exists('/etc/interchangedisable'):
            v1138_specific.append('Interchange must be disabled.  Do so in Tweak Settings')

    return v1138_specific

if __name__ == "__main__":
    print(v1138())
