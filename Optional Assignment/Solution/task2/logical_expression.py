#!/usr/bin/env python

import sys
from copy import copy
import copy


class logical_expression:
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []

def update(symbol, value, model):
    model[symbol] = value
    return model


def true_false(knowledgebase, stm, model):
    ss = []
    negation = '(not ' + stm + ')'

    stm = read_expression(stm)
    if not check_expression(stm):
        sys.exit('statement is invalid')

    print('\nChecking statement: ')
    print_expression(stm, '')


    ss = get_symbols(ss, knowledgebase, stm)
    ss = list(set(ss))

    ss = copy.deepcopy(ss)
    for i in model.keys():
        ss.remove(i)

    negative_statement = read_expression(negation, [0])
    statement1 = check_TT_entail(knowledgebase, stm, ss, model)
    statement2 = check_TT_entail(knowledgebase, negative_statement, ss, model)
    result = get_result_statement(statement1, statement2)
    print(result)
    wr_re(result)



def read_subexpressions(input_string, counter, subexpressions):

    length = len(input_string)
    while True:
        if counter[0] >= length:
            print('\nUnexpected end of input.\n')
            return 0

        if input_string[counter[0]] == ' ':
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def check_TT_entail(knowledge_base, stm, ss, model):
    if not ss:
        result = ev(knowledge_base, model)
        if result:
            result = ev(stm, model)
            return result
        else:
            return True
    else:
        symbol, remaining = ss[0], ss[1:]
        return check_TT_entail(knowledge_base, stm, remaining, update(symbol, True, model)) and check_TT_entail(
            knowledge_base, stm, remaining, update(symbol, False, model))


def read_word(input_string, counter, target):
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def read_expression(input_string, counter=[0]):
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:
            read_word(input_string, counter, result.symbol)
            break
    return result


def check_expression(expression):
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                  (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' % (
            expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
            expression.connective[0].lower() != 'or' and \
            expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not check_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1


def get_symbols(ss, knowledbase=None, stm=None):
    if knowledbase is not None:
        if knowledbase.symbol[0]:
            ss.append(knowledbase.symbol[0])
        for i in knowledbase.subexpressions:
            get_symbols(ss, i)
    if stm is not None:
        if stm.symbol[0]:
            ss.append(stm.symbol[0])
        for i in stm.subexpressions:
            get_symbols(ss, i)

    return ss


def wr_re(result):
    output_file = open('result.txt', 'w')
    output_file.write(result)
    output_file.close()





def get_result_statement(statement1, statement2):
    if statement1 and not statement2:
        return 'Definitely True.'
    elif not statement1 and statement2:
        return "Definitely False."
    elif not statement1 and not statement2:
        return "Possibly True, Possibly False."
    else:
        return "Both True and False."


def ev(expression, model):
    if expression.connective[0] == 'not':
        return not ev(expression.subexpressions[0], model)
    elif expression.connective[0] == 'xor':
        for i, sub in enumerate(expression.subexpressions):
            if i == 0:
                val = ev(sub, model)
                continue
            val = (val and not ev(sub, model)) or (not val and ev(sub, model))
        return val
    elif expression.connective[0] == 'and':
        for i, sub in enumerate(expression.subexpressions):
            if i == 0:
                val = ev(sub, model)
                continue
            val = val and ev(sub, model)
        return val

    elif expression.connective[0] == 'or':
        for i, sub in enumerate(expression.subexpressions):
            if i == 0:
                val = ev(sub, model)
                continue
            val = val or ev(sub, model)
        return val
    elif expression.connective[0] == 'if':
        return (not ev(expression.subexpressions[0], model)) or ev(expression.subexpressions[1], model)
    elif expression.connective[0] == 'iff':
        return (ev(expression.subexpressions[0], model) and ev(expression.subexpressions[1], model))

    return model[expression.symbol[0]]

def print_expression(expression, separator):
    if expression == 0 or expression == None or expression == '':
        print('\nINVALID\n')

    elif expression.symbol[0]:
        sys.stdout.write('%s' % expression.symbol[0])

    else:
        sys.stdout.write('(%s' % expression.connective[0])
        for subexpression in expression.subexpressions:
            sys.stdout.write(' ')
            print_expression(subexpression, '')
            sys.stdout.write('%s' % separator)
        sys.stdout.write(')')




