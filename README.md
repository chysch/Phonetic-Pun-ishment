# Phonetic-Pun-ishment
**_Calling our puns gay doesn't really do them justice because it limits them to homo-graphic one, so we decided to call them punishing instead._**

A system for detecting homophonic puns.
## Table of Contents
1. [Requirements](#requirements)
2. [How to use](#how-to-use)
    1. [Installing Python](#installing-python)
    2. [Installing NLTK](#installing-nltk)
    3. [Running the Project](#running-the-project)
3. [File Formats](#file-formats)
    1. [Input](#input)
    2. [Intermediate](#intermediate)
    3. [Output](#output)
## Requirements
* Python 3.X
* Internet connection
* NLTK
* NLTK libraries:
     * punkt
     * averaged_perceptron_tagger
     * wordnet
     * words

[Back to table of contents](#table-of-contents)
## How to use
### Installing Python
Go to the website https://www.python.org/ and download and install the latest version of Python 3.X.

[Back to table of contents](#table-of-contents)
### Installing NLTK
In the command line in the Python directory write the following command:
```
python -n pip install nltk
```
In the Python interpreter write for each library necessary a download command, for example:
```
>>> nltk.download('punkt')
```

[Back to table of contents](#table-of-contents)
### Running the Project
**_If you want a shortcut script which does the whole pipeline see [this](#putting-them-all-together)._**
#### Train
This stage takes a phonetic dictionary file and turns it into two phonetic files formatted for the next stages.

Output: .FORE file, .BACK file

Usage syntax:
```
train <output name> <RULE file> <DICT files...>
```
Explanation:

- output name: The name of the output file/s without extensions.
- RULE file: The name of a file with ".rule" extension with the hyper-parameter values to use.
- DICT files: The names of one or more phonetic dictionary files in plain text.

[Back to table of contents](#table-of-contents)
#### Analyze
This stage takes a .FORE file and the TEST file and creates a phonetic breakdown of the TEST file sentences.

Output: .PHON file

Usage syntax:
```
analyze <output name> <TEST file> <FORE file> <RULE file>
```
Explanation:

- output name: The name of the output file/s without extensions.
- TEST file: The name of the TEST file with the sentences to analyze.
- FORE file: The name of a file the has the phonetic structure of the dictionary words as created by the Train stage.
- RULE file: The name of a file with ".rule" extension with the hyper-parameter values to use.

[Back to table of contents](#table-of-contents)
#### Synthesize
This stage takes a .BACK file and a .PHON file and creates a list of phonetically matching sentences for the phonetic breakdowns in the .PHON file.

Output: .RAW file

Usage syntax:
```
synthesize <output name> <PHON file> <BACK file> <RULE file>
```
Explanation:

- output name: The name of the output file/s without extensions.
- PHON file: The name of a file the has the phonetic structure of the TEST sentences as created by the Analyze stage.
- BACK file: The name of a file the has the dictionary words fitting phonetic structures as created by the Train stage.
- RULE file: The name of a file with ".rule" extension with the hyper-parameter values to use.

[Back to table of contents](#table-of-contents)
#### Clean
This stage takes a .RAW file and filters from it all the illogical possibilities leaving (hopefully) only good candidates for multiple meanings.

Output: .PARSED file

Usage syntax:
```
clean <output name> <RAW file> <RULE file>
```
Explanation:

- output name: The name of the output file/s without extensions.
- RAW file: The name of a file the has the phonetic matches for the TEST sentences as created by the Synthesize stage.
- RULE file: The name of a file with ".rule" extension with the hyper-parameter values to use.

[Back to table of contents](#table-of-contents)
#### Evaluate
This stage takes a fully parsed file and compares it with a provided GOLD file.

Output: .EVAL file

Usage syntax:
```
evaluate <output name> <PARSED file> <GOLD file>
```
Explanation:

- output name: The name of the output file/s without extensions.
- PARSED file: The name of a fully parsed file as created by the Clean stage.
- GOLD file: The name of a the results expected in the PARSED file.

[Back to table of contents](#table-of-contents)
#### Putting them all together
We created a script for skipping all the intermediate stages to make the job easier.

Output: All outputs from all stages.

Usage syntax:
```
full_run <output name> <TEST file> <GOLD file> <RULE file> <DICT files...>
```
Explanation:

- output name: The name of the output file/s without extensions.
- TEST file: The name of the TEST file with the sentences to analyze.
- GOLD file: The name of a the results expected in the PARSED file.
- RULE file: The name of a file with ".rule" extension with the hyper-parameter values to use.
- DICT files: The names of one or more phonetic dictionary files in plain text.

[Back to table of contents](#table-of-contents)
## File Formats
### Input
#### Dictionary files (.dict or .txt or other plain text)
##### Format
Format type: A line for every entry

Each entry:
```
<Word>\t<Phoneme> <Phoneme> <Phoneme> etc.
```
Comments:
* The words are composed of A-Z, a-z, 0-9 and symbols.
* A word which appears more than once has the number # in parenthesis after the word such: Word (#)
* The phonemes can be any combination of one or more uppercase A-Z. We use the ARPAbet symbol set (see [wikipedia entry](http://en.wikipedia.org/wiki/Arpabet)).
* The dictionary we used is The Carnegie Mellon University Pronouncing Dictionary taken from the source code [here](http://www.speech.cs.cmu.edu/cgi-bin/cmudict).
##### Example lines
```
ADVANTAGEOUS    AE D V AH N T EY JH AH S
ADVANTAGES  AE D V AE N T IH JH IH Z
ADVANTAGES(2)	AH D V AE N T IH JH IH Z
ADVANTAGES(3)	AE D V AE N IH JH IH Z
ADVANTAGES(4)	AH D V AE N IH JH IH Z
ADVANTEST	AE D V AE N T AH S T
ADVANTEST(2)	AH D V AE N T AH S T
ADVECTION	AE D V EH K SH AH N
ADVENT	AE D V EH N T
```
#### Rule files (.rule or .txt or other plain text)
##### Format
Format type: A line for every rule.

Each rule:
```
<Domain>#<Rule>
```
Domains:
1. Phon - This rule applies to all phonemes used and affects the Train stage. Structure:
```
<Domain>#Replace,<Location>:<Phoneme>( <Phoneme>)*,<Phoneme>( <Phoneme>)*
```
Comments:
* Valid values for Location: start, any, end
* Phoneme( Phoneme)* means one or more phonemes seperated by spaces.
2. Word - This rule applies to all words in the dictionaries and affects the Train stage. Structure:
```
<Domain>#<Rule>
```
Comments:
* The only rule currently available is WordNetFilter which uses NLTK to filter out "invalid" words from the dictionary.
3. Sent - This rule applies to sentences processed and applies to the Analyze, Synthesize and Clean stages. Structure:
```
<Domain>#<Key>:<Value>
```
* Keys: Threshold, Sticky, StickyAddSkip, Trunc
* Threshold value is an integer. It indicates the maximal number of consequent words tested for multiple meaning.
* Sticky value is None (default), Add, Rem or Both.
* StickyAddSkip is a list of phonemes seperated by spaces. Only relevant if Sticky is Add or Both.
* Trunc value is an integer. It indicates the maximal number of matches to find for a sentence.
##### Example lines
```
Phon#Replace,any:NG,N
Phon#Replace,end:ER,AH
Phon#Replace,any:IY AH,IH R
Word#WordNetFilter
Sent#Threshold:5
Sent#Sticky:Both
Sent#StickyAddSkip:AW AI CH ER EY NG OW OY
Sent#Trunc:500000
```
#### Test files (.test or .txt or other plain text)
##### Format
Format type: A line for every entry

Each entry:
```
<Sentence>
```
Comments:
* All the letters must be uppercase.
* The sentence must be without punctuation.
* The sentence should be a complete sentence. If only a sentence fragment is submitted the results will not be sufficiently good.
##### Example lines
```
HAVE A GOOD MORNING
DOLPHINS DON'T SPEAK WELSH ONLY WALES
```
#### Gold files (.gold or .txt or other plain text)
See [.parsed](#parsed).

[Back to table of contents](#table-of-contents)
### Intermediate
#### .fore
##### Format
Format type: A line for every entry

Each entry:
```
<Word>\t<Phoneme> <Phoneme> <Phoneme> etc.
```
Comments:
* The words are composed of A-Z, a-z, 0-9 and symbols.
* The phonemes can be any combination of one or more uppercase A-Z. We use the ARPAbet symbol set (see [wikipedia entry](http://en.wikipedia.org/wiki/Arpabet)).
##### Example lines
```
ADVANTAGEOUS    AE D V AH N T EY JH AH S
ADVANTAGES  AE D V AE N T IH JH IH Z
ADVANTAGES	AH D V AE N T IH JH IH Z
ADVANTAGES	AE D V AE N IH JH IH Z
ADVANTAGES	AH D V AE N IH JH IH Z
ADVANTEST	AE D V AE N T AH S T
ADVANTEST	AH D V AE N T AH S T
ADVECTION	AE D V EH K SH AH N
ADVENT	AE D V EH N T
```
#### .back
##### Format
Format type: A line for every entry

Each entry:
```
<Phoneme> <Phoneme> <Phoneme> etc.\t<Word>
```
Comments:
* The words are composed of A-Z, a-z, 0-9 and symbols.
* The phonemes can be any combination of one or more uppercase A-Z. We use the ARPAbet symbol set (see [wikipedia entry](http://en.wikipedia.org/wiki/Arpabet)).
##### Example lines
```
IY R OW D Z	ERODES
G L EY SH ER	GLACIER
IY F IY SH AH N S IY	EFFICIENCY
D IY S P OW Z IY NG	DISPOSING
F AO R M AH N	FOREMEN
R AA K AH W EY	ROCKAWAY
```
#### .phon
##### Format
Format type: A set of lines for each entry succeeded by a empty line.

Each entry:
```
<Sentence>
<Number of Matches>
<Words> [<Phonemes>] <Words>
<Words> [<Phonemes>] <Words>
<Words> [<Phonemes>] <Words>
.
.
.

```
Comments:
* The sentence is the original sentence from the test file.
* The words and brackets are only if a threshold is defined in the rule file. The words are the words from the original sentence and the phonemes are the phonetic breakdowns of the words being analyzed.
##### Example lines
```
GOOD MORNING
2
G UH D M AO R N IY NG
G IY D M AO R N IY NG

HE IS A CREATURE OF PHEW WORDS
8
HE [IY Z EY K R IY CH ER] OF PHEW WORDS
HE [IY Z ER K R IY CH ER] OF PHEW WORDS
HE IS [ER K R IY CH ER AH V] PHEW WORDS
HE IS A [K R IY CH ER AH V F Y UW] WORDS
[HH IY IY Z ER] CREATURE OF PHEW WORDS
HE IS [EY K R IY CH ER AH V] PHEW WORDS
[HH IY IY Z EY] CREATURE OF PHEW WORDS
HE IS A CREATURE [AH V F Y UW W ER D Z]

```
#### .raw
See [.parsed](#parsed).

[Back to table of contents](#table-of-contents)
### Output
#### .parsed
##### Format
Format type: A set of lines for each entry succeeded by a empty line.

Each entry:
```
<Sentence>
<Number of Matches>
<Words>
<Words>
<Words>
.
.
.

```
Comments:
* The sentence is the original sentence from the test file.
* The words are the words composing the phonetic match.
##### Example lines
```
GOOD MORNING
6
GOOD MORN ING
GOOD MORN NG
GOOD MORNING
GOOD MOURN ING
GOOD MOURN NG
GOOD MOURNING

```

#### .eval
##### Format
##### Example lines

[Back to table of contents](#table-of-contents)
