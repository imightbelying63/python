"""a simple frontend wrapper to curl resources.
   lol doesnt actually use curl

   TODO: implement a curl-like -L flag (follow redirects
         custom UA string

"""

import requests, re

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'

def head(url):
    headers_send = {'user-agent': user_agent}

    if not re.match('^http(s?):\/\/', url):
        url = 'http://' + url
        print("Rewriting url to {}".format(url))

    r = requests.head(url, headers=headers_send)

    response_string = requests.status_codes._codes[r.status_code][0].replace("_", " ")

    print(r.status_code, response_string)

    for key,value in r.headers.items():
        print(key, value)



