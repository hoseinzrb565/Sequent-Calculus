import re
import ast

variables = []
connectives = ['not', 'and', 'or', 'then']


def get_formula_as_list(formula_str):

    while formula_str[0] == '(' and formula_str[-1] == ')':
        formula_str = formula_str[1:-1]

    formula_str = re.compile(r"(\b(?!and|or|then|iff|not|\(\w+\)\b)\w+)").sub(r"(\1)", formula_str)
    formula_str = '(' + formula_str + ')'
    formula_str = re.compile(r'(\w+)').sub(r"'\1'", formula_str)
    formula_str = formula_str.replace('(', '[').replace(')', ']')

    formula_lst = ast.literal_eval(formula_str)

    if isinstance(formula_lst, tuple):
        formula_lst = ast.literal_eval('[' + formula_str + ']')

    get_list_of_variables(formula_lst)

    return formula_lst


def get_list_of_variables(formula_lst):

    if not isinstance(formula_lst, list):
        return

    if len(formula_lst) == 1 :
        if isinstance(formula_lst[0], list) and not formula_lst[0][0] in variables:
            variables.append(formula_lst[0][0])
        elif not isinstance(formula_lst[0], list) and not formula_lst[0] in variables:
            variables.append(formula_lst[0])

    elif len(formula_lst) > 1:

        get_list_of_variables(formula_lst[0])
        get_list_of_variables(formula_lst[1])

        if len(formula_lst) == 3:
            get_list_of_variables(formula_lst[2])


def get_indexed_formula(formula_lst):
    indexed_formula = formula_lst

    for variable in variables:
        indexed_formula = str(indexed_formula). \
            replace("\'" + variable + "\'", str(variables.index(variable)))

    return ast.literal_eval(indexed_formula)


def valuation(formula_lst, truth_bits):
    indexed_formula = get_indexed_formula(formula_lst)

    if isinstance(indexed_formula, int):
        return truth_bits[indexed_formula]

    elif len(indexed_formula) == 1:
        return str(int(valuation(indexed_formula[0], truth_bits)))

    elif len(indexed_formula) == 2:
            if indexed_formula[0] == 'not':
                return str((int(valuation(indexed_formula[1], truth_bits)) + 1) % 2)

    elif len(indexed_formula) == 3:
        a = valuation(indexed_formula[0], truth_bits)
        connective = indexed_formula[1]
        b = valuation(indexed_formula[2], truth_bits)

        if connective == 'and':
            if a == '1' and b == '1':
                return '1'
            return '0'

        elif connective == 'or':
            if a == '0' and b == '0':
                return '0'
            return '1'

        elif connective == 'then':
            if a == '1' and b == '0':
                return '0'
            return '1'

        elif connective == 'iff':
            if a == b:
                return '1'
            return '0'

        elif connective == 'NOR':
            if a == '0' and b == '0':
                return '1'
            return '0'

        elif connective == 'NAND':
            if a == '1' and b == '1':
                return '0'
            return '1'

        elif connective == 'XOR':
            if a == b:
                return '0'
            return '1'

    else:
        print("error: invalid input.")


def get_trues(formula_lst):
    trues = []

    for i in range(0, pow(2, len(variables))):
        truth_bit = format(i, '#0' + str((len(variables) + 2)) + 'b')[2:]
        if valuation(formula_lst, truth_bit) == '1':
            trues.append(truth_bit)

    return trues


def is_tautology(formula_lst):
    trues = get_trues(formula_lst)
    if len(trues) == pow(2, len(variables)):
        return True
    return False


def print_help():
    print('''
    welcome!
    this is a simple program which prints the proof of any propositional tautology using sequent calculus. 
    the program also prints the formula's truth table. a couple of notes on syntax:
    
    -the program is case sensitive, be careful!
    -list of allowed connectives:
        ['and', 'or', 'then', 'not']
    -formulas and connectives should be separated with commas. variables do not need parentheses around them. examples:
        p, then, (q, then, (not, p)) is a valid formula, whereas 
        p, then, (q, then, not, p) & p, then, (q, then, not p) are not.           
         ''')
