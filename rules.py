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
    if len(wordnet.synsets(line[0])) == 0:
        return None
    return line

# Creates a list of rules
# Argument: List of strings, each string a rule.
# Result:
#     Tuple ("Phon" rules, "Word" rules, "Sent" rules).
#     "Phon" rules:
#         List of 4-member tuples each containing:
#             1. The function applying to the rule
#             2. The location of application:
#                'start' - The first phoneme/s in each word
#                'end' - The last phoneme/s in each word
#                'any' - Any matching phoneme
#             3. Phoneme/s to which to apply
#             4. Phoneme/s to apply
#     "Word" rules:
#         List of 1-member tuples each containing a rule
#         function.
#     "Sent" rules:
#         List of tuples (name, value).
def PrepareRules(rule_lines):
    res = ([],[],{})
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
        elif t == 'Sent':
            entry = c.split(':')
            res[2][entry[0]] = entry[1]
    return res

# Creates a uppercase word set for filtering.
def CreateWordSet():
    res = []
    contractions = [\
        "'em", "ain't", "aren't", "can't", "can't've", \
        "'cause", "could've", "couldn't", "couldn't've", \
        "didn't", "doesn't", "don't", "hadn't", \
        "hadn't've", "hasn't", "haven't", "he'd", \
        "he'd've", "he'll", "he'll've", "he's", "how'd", \
        "how'd'y", "how'll", "how's", "I'd", "I'd've", \
        "I'll", "I'll've", "I'm", "I've", "isn't", "it'd", \
        "it'd've", "it'll", "it'll've", "it's", "let's", \
        "ma'am", "mayn't", "might've", "mightn't", \
        "mightn't've", "must've", "mustn't", "mustn't've", \
        "needn't", "needn't've", "o'clock", "oughtn't", \
        "oughtn't've", "shan't", "sha'n't", "shan't've", \
        "she'd", "she'd've", "she'll", "she'll've", \
        "she's", "should've", "shouldn't", "shouldn't've", \
        "so've", "so's", "that'd", "that'd've", "that's", \
        "there'd", "there'd've", "there's", "they'd", \
        "they'd've", "they'll", "they'll've", "they're", \
        "they've", "to've", "wasn't", "we'd", "we'd've", \
        "we'll", "we'll've", "we're", "we've", "weren't", \
        "what'll", "what'll've", "what're", "what's", \
        "what've", "when's", "when've", "where'd", \
        "where's", "where've", "who'll", "who'll've", \
        "who's", "who've", "why's", "why've", "will've", \
        "won't", "won't've", "would've", "wouldn't", \
        "wouldn't've", "y'all", "y'all'd", "y'all'd've", \
        "y'all're", "y'all've", "you'd", "you'd've",\
        "you'll", "you'll've", "you're", "you've"]
    res = res + nltk.corpus.words.words()
    res = res + contractions
    res = list(set(res))
    for i in range(len(res)):
        res[i] = res[i].upper()
    res = set(res)
    return res

# Initializes data needed for rule application (useful for
# reducing complexity).
def RulesBegin():
    RuleWordNetFilter.words = CreateWordSet()

# Clears initializes data for memory saving.
def RulesEnd():
    RuleWordNetFilter.words = []
