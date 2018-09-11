from __future__ import division
import sys
import tools

def PrepareData(lines):
    res = []
    i = 0
    while i<len(lines):
        if len(lines[i].strip()) == 0:
            i = i + 1
            continue
        line = lines[i]
        i = i + 1
        num = int(lines[i])
        d = []
        for j in range(num):
            d.append(lines[i+j+1])
        entry = (line,d)
        res.append(entry)
        i = i + num + 1
    return res

def Evaluate(output, test, gold):
    print("Evaluating...")

    # prepare gold and test data

    test_file = open(test, 'r')
    test_lines = test_file.readlines()
    test_file.close()

    test_data = PrepareData(test_lines)

    gold_file = open(gold, 'r')
    gold_lines = gold_file.readlines()
    gold_file.close()

    gold_data = PrepareData(gold_lines)

    # compare gold and test data for evaluation

    eval_lines = PrepareEvalFile(test_data, gold_data)

    with open(output + '.eval','w') as output_file:
        output_file.write(''.join(eval_lines))

def PrepareEvalFile(test_data, gold_data):
    res = []
    total_score = 0
    total_test = 0
    total_gold = 0
    false_pos_count = 0
    false_neg_count = 0
    error = 0

    res.append('item')
    res.append('\t\t\t\t\t')
    res.append('score (amount of matches in tests relatively to gold)')
    res.append('\n')
    res.append('--------------------------------------------------------------------------')
    res.append('\n')

    i = 0
    while i < len(test_data):
        test_item = test_data[i]
        gold_item = gold_data[i]

        total_test = total_test + len(test_item[1])
        total_gold = total_gold + len(gold_item[1])

        sentence = test_item[0].strip()
        res.append(sentence)
        res.append('\t\t\t')

        if len(gold_item[1]) > 0:
            score = len(test_item[1])/len(gold_item[1])
        elif len(test_item[1]) > 0:
            score = len(test_item[1])
        else:
            score = 1

        res.append(str(score))
        res.append('\n')

        total_score = total_score + score
        error = error + abs(score - 1)

        for match in test_item[1]:
            if (match not in gold_item[1]):
                false_pos_count = false_pos_count + 1

        for match in gold_item[1]:
            if (match not in test_item[1]):
                print(match.strip() + " did not matched for "+gold_item[0].strip())
                false_neg_count = false_neg_count + 1

        i = i+1

    avg = total_score/len(test_data)

    false_neg_error = false_neg_count/total_gold
    false_pos_error = false_pos_count/total_test
    accuracy = 100 * (1 - (false_neg_error + false_pos_error)/2)

    res.append('\n')
    res.append('=========================================')
    res.append('\n')
    res.append('Avarage score:')
    res.append('\t')
    res.append(str(avg))
    res.append('\n')
    res.append('Number of false positives:')
    res.append('\t')
    res.append(str(false_pos_count))
    res.append('\n')
    res.append('Number of false negatives:')
    res.append('\t')
    res.append(str(false_neg_count))
    res.append('\n')
    res.append('Accuracy score:')
    res.append('\t')
    res.append(str(accuracy))
    res.append('\n')

    return res

if __name__ == '__main__':
    # Get command line arguments and allow for IDLE manual
    # argument input.
    if 'idlelib' in sys.modules:
        if sys.modules['idlelib']:
            print("Usage: <output name> <PARSED file> <GOLD file>")
            sys.argv.extend(input("Args: ").split())

    if len(sys.argv) != 4:
        print("Usage: <output name> <PARSED file> <GOLD file>")
    else:
        Evaluate(sys.argv[1], sys.argv[2], sys.argv[3])
