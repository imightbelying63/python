""" generate a psuedo-random password """

from random import *

PASSWORD_LENGTH = 13
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_!@#$%^&*()+'

count = 0
new_password = ''
while count < PASSWORD_LENGTH:
    rand_char = randrange(len(CHARACTERS)-1) #len() produces index of string+1
    new_password += CHARACTERS[rand_char]
    count += 1

print(new_password)
