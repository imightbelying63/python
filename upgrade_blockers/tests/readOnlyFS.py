if __name__ == "__main__":
    import os

def readOnlyFS():
    filesystems = ['/etc',
            '/var',
            '/var/lib/rpm',
            '/var/cpanel',
            '/usr/local',
            '/usr/local/cpanel',
            '/usr/local/bin',
            '/usr/bin',
            '/tmp',
            '/var/tmp']
    for fs in filesystems:
        if not os.access(fs, os.W_OK|os.X_OK):
            return False
    return True

