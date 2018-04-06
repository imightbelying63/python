with open("/usr/local/cpanel/version") as version_file:
    cpanel_version = version_file.read()[:5]
