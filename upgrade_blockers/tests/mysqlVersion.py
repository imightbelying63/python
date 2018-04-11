if __name__ == "__main__":
    import subprocess

def mysqlVersion():
    return subprocess.getstatusoutput('mysqladmin version|grep -i "server version"')[1].split("\t")[2]

if __name__ == "__main__":
    print(mysqlVersion())
