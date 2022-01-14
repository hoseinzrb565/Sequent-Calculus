import utilities

def truth_table(formula_str):

    formula_lst = utilities.get_formula_as_list(formula_str)
    truth_table = ''

    for variable in utilities.variables:
        truth_table += '|  ' + variable + '  '

    truth_table += f'|  {formula_str}  |\n'

    for variable in utilities.variables:
        truth_table += '-' * (len(variable) + 5)

    truth_table += '-' * (len(formula_str) + 6) + '\n'

    for i in range(0, pow(2, len(utilities.variables))):

        truth_bit = format(i, '#0' + str((len(utilities.variables) + 2)) + 'b')[2:]

        for j in range(0, len(truth_bit)):
                truth_table += '|  ' + ' ' * (len(utilities.variables[j]) // 2  - 1) +\
                       truth_bit[j] + \
                       ' ' * ((len(utilities.variables[j]) // 2)) + '  '

        truth_table += '|  ' + ' ' * (len(formula_str) // 2  - 1) +\
                       utilities.valuation(formula_lst, truth_bit) + \
                       ' ' * ((len(formula_str) // 2)) + '  |\n'

    for variable in utilities.variables:
        truth_table += '-' * (len(variable) + 5)

    truth_table += '-' * (len(formula_str) + 6) + '\n'

    return truth_table