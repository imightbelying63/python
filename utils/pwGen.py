""" generate a psuedo-random password """

from random import *
import argparse as ap

PASSWORD_LENGTH = 13
EXTENDED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_!@#$%^&*()+'
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_'

#argument handling
p = ap.ArgumentParser()
p.add_argument("-l", "--length", type=int, help="set password length. default: "+str(PASSWORD_LENGTH))
p.add_argument('-e', '--extended', action='store_true', help='use extended non-alphanum chars')
args = p.parse_args()
if args.length: PASSWORD_LENGTH = args.length if args.length > 0 else PASSWORD_LENGTH
if args.extended is True: CHARACTERS = EXTENDED_CHARACTERS

count = 0
new_password = ''
while count < PASSWORD_LENGTH:
    rand_char = randrange(len(CHARACTERS)-1) #len() produces index of string+1
    new_password += CHARACTERS[rand_char]
    count += 1

print(new_password)
