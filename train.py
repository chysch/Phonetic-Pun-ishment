import sys

def Train(output, rules, dicts):
    print("Training...")
    #TODO: Implement...


if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <RULE file> <DICT files...>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) < 4:
        print("Usage: <output name> <RULE file> <DICT files...>")
    else:
        Train(sys.argv[1], sys.argv[2], list(sys.argv[3:]))
