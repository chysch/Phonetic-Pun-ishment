# Creates a match list from the lines of an
# output file of the format <line>/n<num of results>/n<result lines>/n
def PrepareData(lines):
    res = []
    i = 0
    while i<len(lines):
        if lines[i] == '\n':
            i = i + 1
            continue
        line = lines[i]
        i = i + 1
        num = int(lines[i])
        d = []
        for j in range(num):
            d.append(lines[i+j+1])
        entry = (line,d)
        res.append(entry)
        i = i + num + 1
    return res
