import subprocess

def findCpanelTiers():
    cmd = 'curl -s http://httpupdate.cpanel.net/cpanelsync/TIERS'
    curl = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    data = curl.communicate()[0]
    tiers_list = data.splitlines()[1:5]

    tiers = {}
    for t in tiers_list:
        tiers[t.split(":")[0]] = t.split(":")[1]

    return tiers
    

if __name__ == "__main__":
    print(findCpanelTiers())
