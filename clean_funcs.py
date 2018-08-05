import re
import urllib, json
from urllib.request import urlopen
from urllib.parse import urlencode

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
def CanPunctuate(orig_sentence, match, length_threshold):
    length_diff = abs(len(match.split(' ')) - len(orig_sentence.split(' ')))
    # print ('length_diff: ' + str(length_diff))
    if length_diff >= length_threshold:
        return False
    valid = (IsSyntacticallyValid(match) and IsSemanticallyValid(match))
    invalidIntended = IsIncorrectnessIntended(match)
    #print ('valid: '+str(valid))
    return (valid or invalidIntended)

# Returns True iff a given sentence is syntactically valid.
def IsSyntacticallyValid(sentence):
    #print sentence.strip()
    parsing = GetGrammticalParsingOfSentence(sentence)
    n = GetNumOfParsingAnalyses(parsing)
    #print n
    return (n > 0)

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
    res.append(match)
    return res

# Makes a call to LOGON api to retrieve a list of gramatical
# parsing analysis of a given sentence.
def GetGrammticalParsingOfSentence(sentence):
    parserUrl = 'http://erg.delph-in.net/logon'

    #print sentence.strip()

    # Pyhon2 fallback:

    # data = []
    # data.append('input=')
    # data.append(sentence.strip())
    # data.append('&task=Analyze&roots=sentences&genericsp=yes&exhaustivep=best&output=tree&output=dm&output=eds&nresults=0')

    # opener = urllib2.build_opener()
    # opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded')]
    # response = opener.open(parserUrl, ''.join(data))
    # return response.read()

    params = {"input": sentence.strip(), "task": "Analyze",
    "roots": "sentences", "genericsp": "yes", "exhaustivep": "best",
    "output": "tree", "output": "dm", "output": "eds", "nresults": "0"}

    query_string = urllib.parse.urlencode(params)
    data = query_string.encode()

    req = urllib.request.Request(parserUrl,
    headers = {'Content-Type': 'application/x-www-form-urlencoded'},
    data=data)

    res = ''
    q = 'Y'
    while q == 'y' or q == 'Y':
        try:
            res = urllib.request.urlopen(req).read().decode()
        except (ConnectionAbortedError, \
                ConnectionResetError,   \
                ConnectionRefusedError) as error:
            print("Paused due to connection fail. Try again (Y/N/Q)?")
            q = input()
            if q == 'q' or q == 'Q':
                exit()
        else:
            q = 'N'
        
    return res

# Parses the given response of the form "0 of 2 analyses" to extract the result
# of parsing analyses and returns the number of total analyses.
def GetNumOfParsingAnalyses(response):
    fullAnalysisInfo = re.search('<div id=summary>\[(.*)analys', response)
    if fullAnalysisInfo is None:
        return 0
    numOfAnalysis = re.search('([0-9]+) of ([0-9]+)', fullAnalysisInfo.group(1)).group(2)
    return int(numOfAnalysis)

# Makes a call to DataMuse API to retrieve a list of related words
# for a given word.
def GetRelatedWordsOfAWord(word):
    url = 'https://api.datamuse.com/words?ml='
    response = requests.get(url + word)
    return response.json()
