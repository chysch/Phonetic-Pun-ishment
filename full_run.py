import sys
import train
import analyze
import synthesize
import clean
import evaluate

# Run core functions from project modules
def Run(output, test, gold, rule, dicts):
    print("Running...")
    train.Train(output, rule, dicts)
    analyze.Analyze(output, test, output + '.fore')
    synthesize.Synthesize(output, output + '.phon', output + '.back')
    clean.Clean(output, output + '.raw')
    evaluate.Evaluate(output, output + '.parsed', gold)

# If this module is the main running module make sure
# the arguments are valid.
if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <TEST file> <GOLD file> <RULE file> <DICT files...>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) < 6:
        print("Usage: <output name> <TEST file> <GOLD file> <RULE file> <DICT files...>")
    else:
        Run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], list(sys.argv[5:]))
