import sys
from analyze_funcs import *

# Runs the analysis module which translates the test data
# into its phonetic structure.
def Analyze(output, test, fore):
    print("Analyzing...")

    # Organize input
    test_file = open(test, 'r')
    test_lines = test_file.readlines()
    test_file.close()

    fore_file = open(fore, 'r')
    fore_lines = fore_file.readlines()
    fore_file.close()

    fore_data = PrepareForeData(fore_lines)

    # Create data
    phon_lines = []
    for line in test_lines:
        phon_lines = phon_lines + \
                     AnalyzeLine(fore_data, line)

    # Output
    phon_file = open(output + '.phon', 'w')
    phon_file.writelines(phon_lines)
    phon_file.close()

# If this module is the main running module make sure
# the arguments are valid.
if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <TEST file> <FORE file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 4:
        print("Usage: <output name> <TEST file> <FORE file>")
    else:
        Analyze(sys.argv[1], sys.argv[2], sys.argv[3])
