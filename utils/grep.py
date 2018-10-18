import re

def grep(search, file, count=-1):
    output = []
    with open(file) as f:
        for line in f:
            if re.search(search, line):
                if count >= 1:
		    output.append(line)
                    count -= 1
		    continue
                elif count == 0: return output
		else:
		    output.append(line)
		    continue
	return output

    return None
