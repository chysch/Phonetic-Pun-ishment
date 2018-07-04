import re

def RuleReplace(rule, line):
    res = line
    # TODO: Implement...
    return res

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

def ApplyRules(rule_lines, line):
    res = line
    for rule in rule_lines:
        res = rule[0](rule, res)
    return res

def ConvertList(rule_lines, dict_lines):
    res = []
    for line in dict_lines:
        res.append(ApplyRules(rule_lines, line))
    return res

def PrepareList(dict_lines):
    res = []
    for line in dict_lines:
        [w,d] = line.rstrip('\n').split('\t')
        m = re.fullmatch(r"(.)*(\([0-9]\))",w)
        if m:
            w = w.rstrip(m.group(2))
        d = d.split(' ')
        entry = (w,d)
        res.append(entry)
    return res

def GetLists(data):
    res = ([],[])
    for entry in data:
        d = ' '
        d = d.join(entry[1])
        fore = entry[0] + '\t' + d + '\n'
        back = d + '\t' + entry[0] + '\n'
        if not fore in res[0]:
            res[0].append(fore)
        if not back in res[1]:
            res[1].append(back)
    return res

