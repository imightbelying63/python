import re

def grep(search, file, count=-1):
    output = ''
    with open(file) as f:
        for line in f:
            if re.search(search, line):
                if count >= 1:
		    output += line
                    count -= 1
		    continue
                elif count == 0: return output
		else:
		    output += line
		    continue
	return output

    return None
