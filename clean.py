import sys
from clean_funcs import *

# Runs the main filtering module which filters from the
# raw match data only the matches which we want in the
# final parsed file.
def Clean(output, raw):
    print("Filtering...")

    # Organize input
    raw_file = open(raw, 'r')
    raw_lines = raw_file.readlines()
    raw_file.close()

    raw_data = PrepareRawData(raw_lines)

    # Create data
    parsed_lines = []
    for pair in raw_data:
        parsed_lines.append(pair[0])
        matches = []
        for match in pair[1]:
            if CanPunctuate(match):
                matches = matches + GetPunctuations(match)
        matches = list(set(matches))
        parsed_lines.append(str(len(matches)) + '\n')
        parsed_lines = parsed_lines + matches
        parsed_lines.append('\n')

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
            print("Usage: <output name> <RAW file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 4:
        print("Usage: <output name> <RAW file>")
    else:
        Clean(sys.argv[1], sys.argv[2])
