"""skippingComments.py
   parse a text file, skipping comments, and returning a requeste value.
   uses testfiles/skipping.txt as a test file
"""

import re,os

TEST_FILE = 'testfiles/skipping.txt'

def skippingComments(file_name):
    if not os.path.exists(file_name):
        return False
    temp = []
    with open(file_name) as text:
        for line in text.readlines():
            if re.match('^#|^[a-zA-Z]', line): continue
            temp.append(line.rsplit()[2])

    return temp

if __name__ == "__main__":
    print(skippingComments(TEST_FILE))

