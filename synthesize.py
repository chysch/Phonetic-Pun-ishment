import sys
from synthesize_funcs import *

# Runs the main synthesis module which finds phonetic
# matches for the test data.
def Synthesize(output, phon, back):
    print("Synthesizing...")

    # Organize input
    phon_file = open(phon, 'r')
    phon_lines = phon_file.readlines()
    phon_file.close()

    back_file = open(back, 'r')
    back_lines = back_file.readlines()
    back_file.close()

    back_data = PrepareBackData(back_lines)
    phon_data = PreparePhonData(phon_lines)

    # Create data
    raw_lines = []
    for pair in phon_data:
        raw_lines.append(pair[0])
        matches = []
        for d in pair[1]:
            matches = matches + GetMatches(d, back_data)
        matches = list(set(matches))
        raw_lines.append(str(len(matches)) + '\n')
        raw_lines = raw_lines + matches
        raw_lines.append('\n')

    # Output
    raw_file = open(output + '.raw', 'w')
    raw_file.writelines(raw_lines)
    raw_file.close()

# If this module is the main running module make sure
# the arguments are valid.
if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <PHON file> <BACK file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 4:
        print("Usage: <output name> <PHON file> <BACK file>")
    else:   
        Synthesize(sys.argv[1], sys.argv[2], sys.argv[3])
