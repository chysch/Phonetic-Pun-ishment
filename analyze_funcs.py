# Creates a list of words and there phonetic structures.
# Argument: List of strings, each string a dictionary entry
#           with its phonetic structure.
# Result: Dictionary where each key is a word and its
#         value a list of phonetic structures, each in a
#         list of phonemes.
def PrepareForeData(fore_lines):
    res = {}
    for line in fore_lines:
        [w,d] = line.rstrip('\n').split('\t')
        if not w in res:
            res[w] = []
        res[w].append(d)
    return res

# Recursively generates a list of phonemes for a given
# list of words.
# Arguments:
#     1. Word phonetic structure data
#     2. List of words to match
#     3. Index of word being analyzed
#     4. Accumulative output sentence string
# Result: List of phoneme strings.
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

# Generates phonetical structures for a sentence string.
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