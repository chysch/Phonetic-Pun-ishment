import re

# Rule: Replace a set of phonemes with a different set.
def RuleReplace(rule, line):
    res = line
    # TODO: Implement...
    return res

# Creates a list of rules
# Argument: List of strings, each string a rule.
# Result: List of 4-member tuples each containing:
#             1. The function applying to the rule
#             2. The location of application:
#                'Start' - The first phoneme/s in each word
#                'End' - The last phoneme/s in each word
#                'Any' - Any matching phoneme
#             3. Phoneme/s to which to apply
#             4. Phoneme/s to apply
def PrepareRules(rule_lines):
    res = []
    funcs = {"Replace":RuleReplace} # TODO: Add more...
    for rule in rule_lines:
        (d,i) = rule.split(':')
        (f,p) = d.split(',')
        (l,r) = i.split(',')
        entry = []
        entry.append(funcs[f])
        entry.append(i)
        entry.append(l.split(' '))
        entry.append(r.split(' '))
        res.append(tuple(entry))
    return res

# Applies a list of rules to a dictionary pair.
def ApplyRules(rule_lines, line):
    res = line
    for rule in rule_lines:
        res = rule[0](rule, res)
    return res

# Applies a list of rules to a list of dictionary pairs.
def ConvertList(rule_lines, dict_lines):
    res = []
    for line in dict_lines:
        res.append(ApplyRules(rule_lines, line))
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

