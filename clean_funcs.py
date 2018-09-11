import sys
import re
import urllib, json
sys.path.insert(0, 'tools')
from file_utils import getListOfPronounsAndPrepositions
from urllib.request import urlopen
from urllib.parse import urlencode
from random import randint
from time import sleep


# to use After The Deadline API:

# import ATD

# to use Google search:

from googlesearch import search

# to use nltk parsing:

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


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
def CanPunctuate(orig_sentence, match, length_threshold, listOfCommonWords, pronouns):
    length_diff = abs(len(match.split(' ')) - len(orig_sentence.split(' ')))
    # print ('length_diff: ' + str(length_diff))
    if length_diff >= length_threshold:
        return False

    return (IsSyntacticallyValid(match) and IsSemanticallyValid(listOfCommonWords, match, pronouns))

# Returns True iff a given sentence is syntactically valid.
def IsSyntacticallyValid(sentence):
    #print sentence.strip()

    # parsing = GetGrammticalParsingOfSentence(sentence)
    # n = GetNumOfParsingAnalyses(parsing)

    #print n

    # return (n > 0)
    return True

# Returns True iff a given sentence is semantically valid.
def IsSemanticallyValid(listOfCommonWords, sentence, pronouns):
    # NLTK parsing:

    # tokens = nltk.word_tokenize(sentence)
    # tagged = nltk.pos_tag(tokens)
    # entities = nltk.chunk.ne_chunk(tagged)
    # print(sentence + ": \n" + str(entities))

    # Google search:

    # sleep(randint(10,100))
    #
    # params = {'filter': '0', 'lr': 'lang_en'}
    # results = search("\"" + sentence.strip() + "\"", stop=3, only_standard=True, extra_params=params, pause=2)
    # num_results = len(list(results))
    # if (num_results > 0):
    #     print (sentence.strip() + ": " +str(num_results)+ " results \n ")
    #     return True
    # return False


    # ATD parsing:

    # ATD.setDefaultKey("Phonetic-Pun-ishment")
    # errors = ATD.checkDocument("Looking too the water. Fixing your writing typoss.")
    # for error in errors:
    #     print (str(error.type) + " error for: "+error.precontext+" **"+error.string+"**")

    # return GetSearchResults(sentence) > 0

    return IsSentenceInCommonUse(listOfCommonWords, sentence, pronouns)

def getAllWordsBetweenIndices(sentence_words, start, end):
    words = sentence_words[start:end+1]
    return words

def getDifferIndices(original_words, sentence_words):
    start = 0
    while (start < len(original_words) and start < len(sentence_words) and original_words[start] == sentence_words[start]):
        start = start + 1
    end = 0
    while (end < len(original_words) and end < len(sentence_words) and original_words[len(original_words) - end-1] == sentence_words[len(sentence_words) - end-1]):
        end = end + 1
    return [i for i in range(start, end+1)]

# Returns True iff a given sentence is invalid with an intention
# of humorous effect, and a word-play was in place.
def IsIncorrectnessIntended(sentence, original, ignore_words):
    # sentence_words = sentence.split(' ');
    # original_words = original.split(' ');
    #
    # differ_indices = getDifferIndices(original_words, sentence_words)
    #
    # if len(differ_indices) > 0:
    #     differ_words = getAllWordsBetweenIndices(sentence_words, differ_indices[0],  differ_indices[len(differ_indices)-1])
    #
    #     for word in differ_words:
    #         if (word.strip() not in ignore_words):
    #             relatedWords = GetRelatedWordsOfAWord(word)
    #             for orig_word in original_words:
    #                 if (orig_word.lower() != word.lower() \
    #                 and orig_word.lower().find(word.lower()) == -1 \
    #                 and word.lower().find(orig_word.lower()) == -1 \
    #                 and orig_word.lower() in relatedWords):
    #                     print (orig_word + " is a related word to  " + word + ". Pun intended.")
    #                     return True
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
    "roots": "sentences", "genericsp": "yes", "exhaustivep": "all",
    "nresults": "0"}

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
    # response = requests.get(url + word)
    # return response.json()

    listOfWords = []

    req = urllib.request.Request(url + word)
    try:
        res = urllib.request.urlopen(req).read().decode()
    except urllib.error.HTTPError as err:
        print("error while getting related words of: " + word+ ": "+ str(err.code))

    jsonResponse = json.loads(res)
    for item in jsonResponse:
        if (item.get("score") is not None and int(item.get("score")) > 50000):
            listOfWords.append(item.get("word"))

    return listOfWords

def GetSearchResults(sentence):
    query = sentence.strip().lower()
    query = query.replace(' ', '+')
    query = "\"" + query + "\""
    url = 'http://search-api.herokuapp.com/search?q='
    # response = requests.get(url + word)
    # return response.json()
    req = urllib.request.Request(url + query)
    res = urllib.request.urlopen(req).read().decode()

    total_results = -1

    jsonResponse = json.loads(res)
    if (jsonResponse["total_results"] is not None):
        total_results = int(jsonResponse["total_results"])
    print (sentence.strip() + ": " +str(total_results)+ " results \n ")

    return total_results

def IsWordInCommonUse(listOfCommonWords, word):
    # Binary search throught alphabetically sorted list of words
    start = 0
    end = len(listOfCommonWords) - 1
    while start <= end:
        middle = (start + end)// 2
        midpoint = listOfCommonWords[middle]
        if midpoint > word:
            end = middle - 1
        elif midpoint < word:
            start = middle + 1
        elif midpoint == word:
            return True
        else:
            return False
    return False

def IsSentenceInCommonUse(listOfCommonWords, sentence, pronouns):
    sentence_words = sentence.split(' ');
    for word in sentence_words:
        if (not IsWordInCommonUse(listOfCommonWords, word.lower().strip()) and word.lower().strip() not in pronouns):
            print ("Word: " + word + " is not in common use\n")
            return False
    return True
