if __name__ == "__main__":
    import os

def licenseCheck():
    if os.path.isfile("/usr/local/cpanel/cpanel.lisc"):
        return True
    else:
        return False
