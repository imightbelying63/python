"""THIS IS NO LONGER NEEDED"""
if __name__ == "__main__":
    import subprocess, re
    
def findReleaseVersion():
    proc = subprocess.run(['curl', 'http://httpupdate.cpanel.net/cpanelsync/TIERS', '-s'], stdout=subprocess.PIPE)
    tiers_list = proc.stdout.decode().splitlines()

    regex = re.compile("^release:(.*)?")
    for t in tiers_list:
        if regex.match(t):
            release = regex.match(t).group(1)
            return release

    return None

