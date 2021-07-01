#!/usr/bin/env python
from logical_expression import *

a_a = {}
def main(argv):
    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [inputfile]' % argv[0])
        sys.exit(0)
    try:
        inputfile = open(argv[1], 'rb')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)
    print('\nLoading wumpus rules...')
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in inputfile:
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        if subexpression.connective[0] == 'not':
            a_a[subexpression.subexpressions[0].symbol[0]] = False
        if subexpression.connective[0] == '':
            a_a[subexpression.symbol[0]] = True

        knowledge_base.subexpressions.append(subexpression)
    inputfile.close()


    try:
        inputfile = open(argv[2], 'rb')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)
    print('\n\nLoading additional knowledge...')

    try:
        for line in inputfile:
            if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
                continue
            counter = [0]
            subexpression = read_expression(line.rstrip('\r\n'), counter)
            if subexpression.connective[0] == 'not':
                a_a[subexpression.subexpressions[0].symbol[0]] = False

            if subexpression.connective[0] == '':
                a_a[subexpression.symbol[0]] = True

            knowledge_base.subexpressions.append(subexpression)
        inputfile.close()

    except:
        print("Error")
    if not check_expression(knowledge_base):
        sys.exit('invalid knowledge base')
    print_expression(knowledge_base, '\n')

    try:
        inputfile = open(argv[3], 'rb')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print('\n\nLoading statement...')
    statement = inputfile.readline().rstrip('\r\n')
    inputfile.close()
    true_false(knowledge_base, statement, a_a)
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
