if __name__ == "__main__":
    import platform, sys

"""this module will detect that python3 is available, and the OS is at least centos6"""

def platformDepsCheck():
    if float(platform.linux_distribution()[1]) < 6:
        print("CentOS 6 or above is required")
        sys.exit(2)
    if int(sys.version[:1]) < 3:
        print("Python3 is required")
        sys.exit(2)

