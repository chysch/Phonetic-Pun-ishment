# Creates a sentence match list from the lines of a
# sentence output file.
def PrepareRawData(raw_lines):
    res = []
    i = 0
    while i<len(raw_lines):
        if raw_lines[i] == '\n':
            i = i + 1
            continue
        line = raw_lines[i]
        i = i + 1
        num = int(raw_lines[i])
        d = []
        for j in range(num):
            d.append(raw_lines[i+j+1])
        entry = (line,d)
        res.append(entry)
        i = i + num + 1
    return res

# Returns True if a given list of words can be punctuated
# correctly and logically and False otherwise.
def CanPunctuate(match):
    res = False
    return res

# Returns a list of correctly punctuated sentences for a
# given unpunctuated sentence.
def GetPunctuations(match):
    res = []
    return res
