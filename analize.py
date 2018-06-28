import sys

def Analize(output, test, fore):
    print("Analizing...")
    #TODO: Implement...


if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <TEST file> <FORE file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 4:
        print("Usage: <output name> <TEST file> <FORE file>")
        exit()
    
    Analize(sys.argv[1], sys.argv[2], sys.argv[3])
