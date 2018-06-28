import sys
import train
import analize
import synthesize
import clean
import evaluate

def Run(output, test, rule, dicts):
    print("Running...")
    train.Train(output, rule, dicts)
    analize.Analize(output, test, output + '.fore')
    synthesize.Synthesize(output, output + '.phon', output + '.back')
    clean.Clean(output, output + '.raw')
    evaluate.Evaluate(output, output + '.parsed')


if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <TEST file> <RULE file> <DICT files...>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) < 5:
        print("Usage: <output name> <TEST file> <RULE file> <DICT files...>")
        exit()
    
    Run(sys.argv[1], sys.argv[2], sys.argv[3], list(sys.argv[4:]))
