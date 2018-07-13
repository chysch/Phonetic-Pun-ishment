import sys
from train_funcs import *

# Runs the main training module
def Train(output, rules, dicts):
    print("Training...")

    # Arrange input
    rule_file = open(rules, 'r')
    rule_lines = rule_file.readlines()
    rule_file.close()

    rule_lines = PrepareRules(rule_lines)

    # Create data
    output_list = []
    for d in dicts:
        dict_file = open(d, 'r')
        dict_lines = dict_file.readlines()
        dict_file.close()

        dict_lines = PrepareList(dict_lines)
        
        output_list = output_list + ConvertList(\
            rule_lines, dict_lines)

    (fore_lines, back_lines) = GetLists(output_list)

    # Output
    fore_file = open(output + '.fore', 'w')
    fore_file.writelines(fore_lines)
    fore_file.close()

    back_file = open(output + '.back', 'w')
    back_file.writelines(back_lines)
    back_file.close()

# If this module is the main running module make sure
# the arguments are valid.
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
