from tree import *

# Parses the phonemes and the words they represent into
# a tree where the inner nodes are phonemes and the
# leaves are words.
def PrepareBackData(back_lines):
    res = Tree()
    res.head.label = 'back_data'
    for line in back_lines:
        [d,w] = line.rstrip('\n').split('\t')
        c = res.head
        d = d.split(' ')
        for p in d:
            c = c.Child(p)
            c.data.type = 'phoneme'
        c = c.Child(w)
        c.data.type = 'word'
    return res

# Creates a phonetic match list from the lines of a
# phonetic output file.
def PreparePhonData(phon_lines):
    res = []
    i = 0
    while i<len(phon_lines):
        if phon_lines[i] == '\n':
            i = i + 1
            continue
        line = phon_lines[i]
        i = i + 1
        num = int(phon_lines[i])
        d = []
        for j in range(num):
            d.append(phon_lines[i+j+1])
        entry = (line,d)
        res.append(entry)
        i = i + num + 1
    return res

# Recursively calculates the phonetically matching
# sentences for a given phoneme list.
# Arguments:
#     1. Phoneme tree
#     2. List of phonemes to match
#     3. Accumuative current match sentence string
#     4. Index of phoneme currently being checked
def CalcMatches(back, phons, match, i):
    res = []

    # Case 1: End of sentence
    if i >= len(phons):
        for child in back.children:
            if child.data.type == 'word':
                full_match = match
                if not full_match == '':
                    full_match = full_match + ' '
                full_match = full_match + child.data.label
                full_match = full_match + '\n'
                res.append(full_match)
        return res

    # Case 2: End of word
    for child in back.children:
        if child.data.type == 'word':
            full_match = match
            if not full_match == '':
                full_match = full_match + ' '
            full_match = full_match + child.data.label
            res = res + CalcMatches(back.head, \
                                    phons,     \
                                    full_match, i)
    # Case 3: Existing word start
    if back.ChildExists(phons[i]):
        res = res + CalcMatches(back.Child(phons[i]), \
                                phons,                \
                                match, i+1)
    
    # Case 4: Word was not in phon-dictionary
    if phons[i] == '---' and back == back.head:
        full_match = match
        if not full_match == '':
            full_match = full_match + ' '
        full_match = full_match + '---'
        res = res + CalcMatches(back.head, \
                                phons,                \
                                full_match, i+1)

    return res

# Gets phonetically matching senteces for a sentence.
def GetMatches(phon, back):
    res = CalcMatches(back.head,                    \
                      phon.rstrip('\n').split(' '), \
                      '', 0)
    res = list(set(res))
    return res
