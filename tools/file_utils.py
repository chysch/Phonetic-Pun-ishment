import sys
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

def getListOfPronounsAndPrepositions():
    result = []
    with open('dicts/pronouns.txt', 'r') as pronounsFile:
        pronouns = pronounsFile.readlines()
        for line in pronouns:
            result.append(line.strip())
    with open('dicts/prepositions.txt', 'r') as prepositionsFile:
        prepositions = prepositionsFile.readlines()
        for line in prepositions:
            result.append(line.strip())
    return result

# Outputs a list of google query urls for an input list of sentences to query.
def getGoogleQueries(inputFile, outputFile):
    with open(inputFile, "r") as ins, open(outputFile, "a") as out:
        array = []
        for line in ins:
            out.write("http://www.google.com/search?lr=lang_en&filter=0&as_epq="+line.strip().replace(" ", "+")+"\n")

if __name__ == '__main__':
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <RAW file> <RULE file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 3:
        print("Usage: <input file> <output file>")
    else:
        getGoogleQueries(sys.argv[1], sys.argv[2])
