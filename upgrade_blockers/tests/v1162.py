"""tests for upgrading to 62:
   + mysql 5.5+
"""

from mysqlVersion import *

def v1162():
    v1162_specific = []

    #mysql check
    mysql_version = mysqlVersion()
    if mysql_version < 5.5:
        v1162_specific.append("MySQL version " + str(mysql_version) + " is less than 5.5; 5.5+ is required")

    return v1162_specific

if __name__ == "__main__":
    print(v1162())
