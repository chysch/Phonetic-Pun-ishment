def PrepareForeData(fore_lines):
    res = {}
    for line in fore_lines:
        [w,d] = line.rstrip('\n').split('\t')
        if not w in res:
            res[w] = []
        res[w].append(d)
    return res

def GetPhonMatchList(fore_data, words, i, line):
    res = []
    if i >= len(words):
        line = line + '\n'
        return [line]
    if not words[i] in fore_data:
        print("No match found for: " + words[i])
        return GetPhonMatchList(    \
            fore_data, words,       \
            i + 1, line + ' ---')
    for match in fore_data[words[i]]:
        nl = line
        if nl != '':
            nl = nl + ' '
        res = res + GetPhonMatchList( \
            fore_data, words,         \
            i + 1, nl + match)
    return res

def AnalyzeLine(fore_data, line):
    res = []
    res.append(line.rstrip('\n')+'\n')
    lst = GetPhonMatchList(fore_data, \
                           line.rstrip('\n').split(' '), \
                           0, '')
    lst = list(set(lst))
    res.append(str(len(lst)) + '\n')
    res = res + lst
    res.append('\n')
    return res
