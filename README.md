# Phonetic-Pun-ishment
A system for finding homophonic puns.
## Table of Contents
1. [Requirements](#Requirements)
2. [How to use](#How-to-use)
    1. [Installing Python](#Installing-Python)
    2. [Installing NLTK](#Installing-NLTK)
    3. [Running the Project](#Running-the-Project)
3. [File Formats](#File-Formats)
## Requirements
* Python 3.X
* Internet connection
* NLTK
* NLTK libraries:
     * punkt
     * averaged_perceptron_tagger
     * wordnet
     * words
## How to use
### Installing Python
Go to the website https://www.python.org/ and download and install the latest version of Python 3.X.
### Installing NLTK
In the command line in the Python directory write the following command:
```
python -n pip install nltk
```
In the Python interpreter write for each library necessary a download command, for example:
```
>>> nltk.download('punkt')
```
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
#### Putting them all together
We created a script for skipping all the middle stages to make the job easier.

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

## File Formats
