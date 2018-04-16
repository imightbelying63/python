import subprocess

def mysqlVersion():
    cmd = "mysqladmin version|grep 'Server version'"
    mysqladmin = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    mysql_version = mysqladmin.communicate()[0].expandtabs().rstrip().split()[2]
    return float(''.join(mysql_version[:3]))

if __name__ == "__main__":
    print mysqlVersion()
