if __name__ == "__main__":
    import subprocess

def mysqlVersion():
    version = subprocess.getstatusoutput('mysqladmin version|grep -i "server version"')[1].expandtabs().split()[2]
    return ''.join(version[:3])

if __name__ == "__main__":
    print(mysqlVersion())
