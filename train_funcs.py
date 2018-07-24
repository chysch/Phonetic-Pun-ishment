import re
from nltk.corpus import wordnet
import nltk.corpus

# Rule: Replace a set of phonemes with a different set.
def RuleReplace(rule, line):
    res = line
    d = []
    l1 = len(line[1])
    l = len(rule[2])
    r = range(l)
    if rule[1] == 'any':
        for i in range(l1):
            if line[1][i] != rule[2][0] or i+l > l1:
                d.append(line[1][i])
                continue
            is_match = True
            for j in r:
                if line[1][i+j] != rule[2][j]:
                    is_match = False
            if is_match:
                for j in rule[3]:
                    d.append(j)
                i = i + l - 1
    elif rule[1] == 'start':
        is_match = True
        for j in r:
            if line[1][j] != rule[2][j]:
                is_match = False
        s = 0
        if is_match:
            for j in rule[3]:
                d.append(j)
            s = l
        for i in range(s,l1):
            d.append(line[1][i])
    elif rule[1] == 'end':
        is_match = True
        for j in r:
            if line[1][l1-l+j] != rule[2][j]:
                is_match = False
        e = l1
        if is_match:
            e = l1-l
        for i in range(e):
            d.append(line[1][i])
        if is_match:
            for j in rule[3]:
                d.append(j)
    else:
        d = res[1]
    res = (res[0], d)
    return res

# Rule: Test WordNet to see if word exists there.
def RuleWordNetFilter(rule, line):    
    if line[0] in RuleWordNetFilter.words:
        return line
    if line[0].lower() in RuleWordNetFilter.words:
        return line
    if len(wordnet.synsets(line[0])) == 0:
        return None
    return line

# Creates a list of rules
# Argument: List of strings, each string a rule.
# Result: List of 4-member tuples each containing:
#             1. The function applying to the rule
#             2. The location of application:
#                'start' - The first phoneme/s in each word
#                'end' - The last phoneme/s in each word
#                'any' - Any matching phoneme
#             3. Phoneme/s to which to apply
#             4. Phoneme/s to apply
def PrepareRules(rule_lines):
    res = ([],[],[])
    funcs = {"Replace":RuleReplace, \
             "WordNetFilter":RuleWordNetFilter} \
             # TODO: Add more...
    for rule in rule_lines:
        if rule.strip('\n').strip(' ') == '':
            continue
        (t,c) = rule.rstrip('\n').split('#')
        if t == 'Phon':
            (d,i) = c.split(':')
            (f,p) = d.split(',')
            (l,r) = i.split(',')
            entry = []
            entry.append(funcs[f])
            entry.append(p)
            entry.append(l.split(' '))
            entry.append(r.split(' '))
            res[0].append(tuple(entry))
        elif t == 'Word':
            entry = []
            entry.append(funcs[c])
            res[1].append(tuple(entry))
    return res

# Applies a list of rules to a dictionary pair.
def ApplyRules(rule_lines, line):
    res = line
    for rule in rule_lines[1]:
        res = rule[0](rule, res)
        if res == None:
            return res
    for rule in rule_lines[0]:
        res = rule[0](rule, res)
    return res

# Applies a list of rules to a list of dictionary pairs.
def ConvertList(rule_lines, dict_lines):
    res = []
    RuleWordNetFilter.words = set(nltk.corpus.words.words())
    for line in dict_lines:
        entry = ApplyRules(rule_lines, line)
        if entry != None:
            res.append(entry)
    RuleWordNetFilter.words = []
    return res

# Creates a list of phonetic dictionary entries.
# Argument: List of strings, each string a dictionary entry
#           with its phonetic structure.
# Result: List of pairs, each pair a word and its
#         phonetic structure in a list of phonemes.
def PrepareList(dict_lines):
    res = []
    for line in dict_lines:
        [w,d] = line.rstrip('\n').split('\t')
        # In the dictionary a multiple entry has an entry
        # number in parenthesis after it which should be
        # removed.
        m = re.fullmatch(r"(.)*(\([0-9]\))",w)
        if m:
            w = w.rstrip(m.group(2))
        d = d.split(' ')
        entry = (w,d)
        res.append(entry)
    return res

# Converts a list of dictionary pairs to a tuple with the
# lists of FORE and BACK lines.
def GetLists(data):
    res = [[],[]]
    for entry in data:
        d = ' '
        d = d.join(entry[1])
        fore = entry[0] + '\t' + d + '\n'
        back = d + '\t' + entry[0] + '\n'
        res[0].append(fore)
        res[1].append(back)
    res[0] = list(set(res[0]))
    res[1] = list(set(res[1]))
    res = tuple(res)
    return res

