import sys

def Synthesize(output, phon, back):
    print("Synthesizing...")
    #TODO: Implement...


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
