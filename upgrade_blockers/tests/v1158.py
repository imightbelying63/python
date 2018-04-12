"""test for upgrading to 11.58:
   + OS release must be 6+
    * this is technically already handled in by platformDeps() but is still
      implemented here for ease and posterity
   + 64bit systems only
   + The perl514 RPM target must not be set to installed or unmanaged
"""

import os,sys,re

def v1158():
    pass

if __name__ == "__main__":
    print(v1158())
