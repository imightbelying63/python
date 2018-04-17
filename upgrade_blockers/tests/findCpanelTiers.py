import subprocess

def findCpanelTiers():
    proc = subprocess.run(['curl', 'http://httpupdate.cpanel.net/cpanelsync/TIERS', '-s'], stdout=subprocess.PIPE)
    tiers_list = proc.stdout.decode().splitlines()[1:5]

    tiers = {}
    for t in tiers_list:
        tiers[t.split(":")[0]] = t.split(":")[1]

    return tiers
    

if __name__ == "__main__":
    print(findCpanelTiers())
