import sys

def Evaluate(output, raw):
    print("Evaluating...")
    #TODO: Implement...


if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <PARSED file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 4:
        print("Usage: <output name> <PARSED file>")
        exit()
    
    Evaluate(sys.argv[1], sys.argv[2])
