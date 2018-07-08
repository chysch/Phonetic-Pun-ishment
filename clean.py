import sys
from clean_funcs import *

def Clean(output, raw):
    print("Filtering...")

    raw_file = open(raw, 'r')
    raw_lines = raw_file.readlines()
    raw_file.close()

    raw_data = PrepareRawData(raw_lines)

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

    parsed_file = open(output + '.parsed', 'w')
    parsed_file.writelines(parsed_lines)
    parsed_file.close()


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
