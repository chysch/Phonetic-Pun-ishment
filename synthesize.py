import sys
from synthesize_funcs import *
from rules import *

# Runs the main synthesis module which finds phonetic
# matches for the test data.
def Synthesize(output, phon, back, rules):
    print("Synthesizing...")

    # Organize input
    rule_file = open(rules, 'r')
    rule_lines = rule_file.readlines()
    rule_file.close()

    rule_lines = PrepareRules(rule_lines)[2]

    phon_file = open(phon, 'r')
    phon_lines = phon_file.readlines()
    phon_file.close()

    back_file = open(back, 'r')
    back_lines = back_file.readlines()
    back_file.close()

    back_data = PrepareBackData(back_lines)
    phon_data = PreparePhonData(phon_lines)

    raw_file = open(output + '.raw', 'w')
    raw_file.close()

    count = 0
    for pair in phon_data:
        # Create data
        raw_lines = []
        raw_lines.append(pair[0])
        matches = []
        for d in pair[1]:
            matches = matches + \
                      GetMatches(d, back_data, rule_lines)
        map(lambda x: pair[1][0]+x+pair[1][2], matches)
        matches = list(set(matches))
        raw_lines.append(str(len(matches)) + '\n')
        raw_lines = raw_lines + matches
        raw_lines.append('\n')
        count = count + 1
        print("Completed synthesis for #" + str(count),\
              pair[0].rstrip('\n'),
              "(" + str(len(matches)) + ")")

        # Output
        raw_file = open(output + '.raw', 'a')
        raw_file.writelines(raw_lines)
        raw_file.close()

# If this module is the main running module make sure
# the arguments are valid.
if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <PHON file> <BACK file> <RULE file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 5:
        print("Usage: <output name> <PHON file> <BACK file> <RULE file>")
    else:   
        Synthesize(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
