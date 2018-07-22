import re
import urllib2, urllib, json

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

# Returns True iff a given list of words can be punctuated
# correctly and logically and False otherwise.
def CanPunctuate(match):
    return (IsSyntacticallyValid(match) and IsSemanticallyValid(match)) or IsIncorrectnessIntended(match)

# Returns True iff a given sentence is syntactically valid.
def IsSyntacticallyValid(sentence):
    #print sentence.strip()
    parsing = GetGrammticalParsingOfSentence(sentence)
    return GetNumOfParsingAnalyses(parsing) > 0

# Returns True iff a given sentence is semantically valid.
def IsSemanticallyValid(sentence):
    # TODO - Anna
    return True

# Returns True iff a given sentence is invalid with an intention
# of humorous effect, and a word-play was in place.
def IsIncorrectnessIntended(sentence):
    # TODO - Anna
    # relatedWords = GetRelatedWordsOfAWord(word)
    return False

# Returns a list of correctly punctuated sentences for a
# given unpunctuated sentence.
def GetPunctuations(match):
    res = []
    return res

# Makes a call to LOGON api to retrieve a list of gramatical
# parsing analysis of a given sentence.
def GetGrammticalParsingOfSentence(sentence):
    parserUrl = 'http://erg.delph-in.net/logon'

    #print sentence.strip()

    data = []
    data.append('input=')
    data.append(sentence.strip())
    data.append('&task=Analyze&roots=sentences&genericsp=yes&exhaustivep=best&output=tree&output=dm&output=eds&nresults=0')

    opener = urllib2.build_opener()
    opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
    response = opener.open(parserUrl, ''.join(data))

    return response.read()

# Parses the given response of the form "0 of 2 analyses" to extract the result
# of parsing analyses and returns the number of total analyses.
def GetNumOfParsingAnalyses(response):
    fullAnalysisInfo = re.search('<div id=summary>\[(.*)analys', response)
    if fullAnalysisInfo is None:
        return 0
    numOfAnalysis = re.search('([0-9]+) of ([0-9]+)', fullAnalysisInfo.group(1)).group(2)
    return numOfAnalysis

# Makes a call to DataMuse API to retrieve a list of related words
# for a given word.
def GetRelatedWordsOfAWord(word):
    url = 'https://api.datamuse.com/words?ml='
    response = requests.get(url + word)
    return response.json()
