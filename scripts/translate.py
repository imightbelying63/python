""" translate input to a coded message where:
    characters are replaced with the key on the opposite side of the kb
    examples:
    
    * a = 1
    * g = v
    * q = p

"""

table = {'a' : 'l',
        'b' : 'c',
        'c' : 'b',
        'd' : 'j',
        'e' : 'i',
        'f' : 'h',
        'g' : 'v',
        'h' : 'f',
        'i' : 'e',
        'j' : 'd',
        'k' : 's',
        'l' : 'a',
        'm' : 'z',
        'n' : 'x',
        'o' : 'w',
        'p' : 'q',
        'q' : 'p',
        'r' : 'u',
        's' : 'k',
        't' : 'y',
        'u' : 'r',
        'v' : 'g',
        'w' : 'o',
        'x' : 'n',
        'y' : 't',
        'z' : 'm',
        }

message = str(input("what is your secret message?\n"))

for char in message[:]:
    if char in table.keys():
        message = message.replace(char, table[char])

print(message)
