"""takes url input, gives a generated short link.  at present, this script:
    - is basically just a practice in modularity
    - uses a text based backend
    - doesnt actually use a fqdn
    - is a strong independent python that dont need no man
"""

import os,sys
import base64

URL_LEN = 6
STORAGE_FILE = "../text/shortener.txt"
FQDN = "https://imbl.co"

def printUsage():
    print(sys.argv[0], "usage:", """
    URL: url to be shortened
    
    takes one single URL only""") 

def generateShortURL():
    """input is irrelevant, use urandom"""

    url = base64.b64encode(os.urandom(URL_LEN)).decode()
    url = url.replace("/", "_")
    return url

def isDuplicate(short):
    """on the incredible off-chance an identical string has been generated as
       has already been stored, prevent it from being used"""

    try:
        with open(STORAGE_FILE, "r") as file:
            read_data = file.read()
            if short in read_data:
                return True
    except:
        pass
        
    return False

def urlTextFormat(url, short):
    """return the format which urls/shorts are stored in text"""
    return url + ":" + short

def saveUrl(url, short):
    """write the url/short to the text backend"""

    with open(STORAGE_FILE, "a+") as file:
        file.write(urlTextFormat(url, short) + "\n")

def printShort(short):
    """simply format and print the shortened URL"""

    return FQDN + "/" + short

if len(sys.argv) < 2:
    printUsage()
    sys.exit(1)

url = sys.argv[1]
#normally i would provide some sorta url regex validator but thats unimportant rn
short = generateShortURL()

if not isDuplicate(short):

    #save the url/short and return to user
    saveUrl(url, short)

    print(printShort(short))
