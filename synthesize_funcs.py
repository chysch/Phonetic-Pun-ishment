from tree import *
import queue

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
            duo = phon_lines[i+j+1].rstrip('\n')\
                           .split('[')
            (start,rest) = ('',duo[0])
            if len(duo) == 2:
                (start,rest) = duo
            duo = rest.split(']')
            (rest,end) = (duo[0],'')
            if len(duo) == 2:
                (rest,end) = duo
            trio = (start,rest,end)
            d.append(trio)
        entry = (line,d)
        res.append(entry)
        i = i + num + 1
    return res

# Class for calculating sentence matches from phonemes.
class MatchMaker:

    # Initializes the object.
    # Arguments:
    #     1. Phoneme tree
    #     2. List of phonemes to match
    #     3. Max. number of matches to return or 0 to ignore
    def __init__(self, back, phon, rules):
        self.back = back
        self.onePhonWords = self.MakeOnePhonList()
        self.phons = phon
        self.trunc = 0
        if 'Trunc' in rules:
            self.trunc = int(rules['Trunc'])
        self.stickyAdd = False
        self.stickyRem = False
        if 'Sticky' in rules:
            if rules['Sticky']=='Both'\
               or rules['Sticky']=='Add':
                self.stickyAdd = True
            if rules['Sticky']=='Both'\
               or rules['Sticky']=='Rem':
                self.stickyRem = True
        if 'StickyAddSkip' in rules:
            self.stickyAddSkip = rules['StickyAddSkip']\
                                 .split(' ')
            self.stickyAddSkip = set(self.stickyAddSkip)

    # Traverses the back tree on a given route returning
    # the node at the end of the route or None.
    def Traverse(self, route):
        node = self.back
        for step in route:
            if not node.ChildExists(step):
                return None
            node = node.Child(step)
        return node

    def MakeOnePhonList(self):
        res = []
        for node in self.back.children:
            for child in node.children:
                if child.data.type == 'word':
                    res.append(node.data.label)
        res = list(set(res))
        return res

    # Calculates the phonetically matching sentences for
    # the phoneme list.
    def CalcMatches(self):
        res = []
        Q = queue.LifoQueue()
        start = ([], 0, '')
        Q.put(start)
        count = 0
        while not Q.empty():
            top = Q.get()
            node = self.Traverse(top[0])

            # Case 1: End of sentence
            if top[1] >= len(self.phons):
                for child in node.children:
                    if child.data.type == 'word':
                        full_match = top[2]
                        if not full_match == '':
                            full_match = full_match + ' '
                        full_match = full_match + child.data.label
                        full_match = full_match + '\n'
                        res.append(full_match)
                        count = count + 1
                        if count%50000 == 0:
                            res = list(set(res))
                            print(len(res), "matches created.")
                        if self.trunc > 0:
                            if len(res) >= self.trunc:
                                print("Truncated results.")
                                return res

                continue

            # Case 2: End of word
            for child in node.children:
                if child.data.type == 'word':
                    full_match = top[2]
                    if not full_match == '':
                        full_match = full_match + ' '                        
                    full_match = full_match + child.data.label
                    trio = ([], top[1], full_match)
                    Q.put(trio)
                    # Handle "Sticky Words"
                    if self.stickyAdd:
                        A = self.phons[top[1]-1]
                        B = self.phons[top[1]]
                        if A != B and \
                           not A in self.stickyAddSkip and\
                           not A in self.onePhonWords:
                            trio = ([], top[1]-1, full_match)
                            Q.put(trio)

            # Case 3: Existing word start
            if node.ChildExists(self.phons[top[1]]):
                route = list(top[0])
                route.append(self.phons[top[1]])
                trio = (route, top[1]+1, top[2])
                Q.put(trio)
                # Handle "Sticky Words"
                if self.stickyRem:
                    if top[1]+1 < len(self.phons):
                        B = self.phons[top[1]]
                        C = self.phons[top[1]+1]
                        if B == C:
                            trio = (top[0], top[1]+1, top[2])
                            Q.put(trio)                    

            # Case 4: Word was not in phon-dictionary
            if self.phons[top[1]] == '---' and top[0] == []:
                full_match = top[2]
                if not full_match == '':
                    full_match = full_match + ' '
                full_match = full_match + '---'
                trio = ([], top[1]+1, full_match)
                Q.put(trio)

        return res

# Recursively calculates the phonetically matching
# sentences for a given phoneme list.
# Arguments:
#     1. Phoneme tree
#     2. List of phonemes to match
#     3. Accumuative current match sentence string
#     4. Index of phoneme currently being checked
#     5. Max. number of matches to return or 0 to ignore
def CalcMatches(back, phons, match, i, rules):
    res = []

    sticky = 'None'
    if 'Sticky' in rules:
        sticky = rules['Sticky']
    
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
            res = res + CalcMatches(back.head,     \
                                    phons,         \
                                    full_match, i, rules)
            # Handle "Sticky Words"
            if sticky == 'Both' or sticky == 'Word':
                A = phons[i-1]
                B = phons[i]
                if A != B:
                    ii = i-1
                else:
                    ii = i+1
                if ii >= 0 and ii < len(self.phons):
                    res = res + CalcMatches(back.head,\
                                            phons,\
                                            full_match,\
                                            ii, rules)
        if 'Trunc' in rules:
            trunc = int(rules['Trunc'])
            if trunc > 0:
                if len(res) >= trunc:
                    print("Truncated results")
                    return res

    # Case 3: Existing word start
    if back.ChildExists(phons[i]):
        res = res + CalcMatches(back.Child(phons[i]), \
                                phons,                \
                                match, i+1, rules)
        # Handle "Sticky Words"
        if sticky == 'Both' or sticky == 'Phon':
            if i+1<len(phons):
                B = phons[i]
                C = phons[i+1]
                if B == C:
                    res = res + CalcMatches( \
                        back,                \
                        phons,               \
                        match, i+1, rules)                    

    # Case 4: Word was not in phon-dictionary
    if phons[i] == '---' and back == back.head:
        full_match = match
        if not full_match == '':
            full_match = full_match + ' '
        full_match = full_match + '---'
        res = res + CalcMatches(back.head,            \
                                phons,                \
                                full_match, i+1, rules)

    return res

# Gets phonetically matching senteces for a sentence.
def GetMatches(phon, back, rules):
#    res = CalcMatches(back.head, phon[1], '', 0, rules)
    maker = MatchMaker(back.head, phon[1].split(' '), rules)
    res = maker.CalcMatches()
    res = list(set(res))
    return res
