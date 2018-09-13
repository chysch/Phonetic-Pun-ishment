import sys
from clean_funcs import *
from rules import *
import time

# Runs the main filtering module which filters from the
# raw match data only the matches which we want in the
# final parsed file.
def Clean(output, raw, rules):
    print("Filtering...")

    # Organize input
    rule_file = open(rules, 'r')
    rule_lines = rule_file.readlines()
    rule_file.close()
    sent_rules = PrepareRules(rule_lines)[2]
    if ('Threshold' in sent_rules):
        length_threshold = int(sent_rules['Threshold'])
    else:
        length_threshold = -1
    if ('OnlineMode' in sent_rules):
        online_mode = True if sent_rules['OnlineMode'].lower() == 'on' else False
    else:
        online_mode = False

    raw_file = open(raw, 'r')
    raw_lines = raw_file.readlines()
    raw_file.close()

    raw_data = PrepareRawData(raw_lines)

    listOfCommonWords = [line.rstrip('\n') for line in open('dicts/common_words.txt')]
    pronous = getListOfPronounsAndPrepositions()

    # Create data
    parsed_lines = []
    for pair in raw_data:
        orig_sentence = pair[0]
        list_of_matches = pair[1]

        start_time = time.time()

        parsed_lines.append(orig_sentence)
        clean_matches = []
        for match in list_of_matches:
            # print ('can pun? : ' + match)
            if CanPunctuate(orig_sentence, match, length_threshold, listOfCommonWords, pronous, online_mode):
                # print ('-> yes ')
                clean_matches.append(match)
            elif IsIncorrectnessIntended(match, orig_sentence, pronous, online_mode):
                clean_matches.append(match + " *** Pun Intended ***")

            # else:
                # print ('-> no ')
        clean_matches = list(set(clean_matches))
        parsed_lines.append(str(len(clean_matches)) + '\n')
        parsed_lines = parsed_lines + clean_matches
        parsed_lines.append('\n')

        elapsed_time = "%.2f" % (time.time() - start_time)
        print ('Finished Cleaning Sentence: ' + orig_sentence.strip()
        + '\nValid Matches Out Of Total = ' + str(len(clean_matches)) + ' / ' + str(len(list_of_matches))
        + '\nTime passed = ' + str(elapsed_time) + ' Sec\n')


    # Output
    parsed_file = open(output + '.parsed', 'w')
    parsed_file.writelines(parsed_lines)
    parsed_file.close()

# If this module is the main running module make sure
# the arguments are valid.
if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <RAW file> <RULE file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 4:
        print("Usage: <output name> <RAW file> <RULE file>")
    else:
        Clean(sys.argv[1], sys.argv[2], sys.argv[3])
