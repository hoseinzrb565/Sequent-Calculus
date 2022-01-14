import utilities
import truth_table
import sequent_calculus

formula_str = input('enter a propositional formula. enter help for syntax. enter exit to quit the program.\n')

while formula_str.casefold() != 'exit'.casefold():
    if formula_str.casefold() == 'help'.casefold():
        utilities.print_help()

    else:

        try:

            formula_lst = utilities.get_formula_as_list(formula_str)
            print(f'\ntruth table:\n{truth_table.truth_table(formula_str)}')

            premises = []
            conclusions = []
            conclusions.append(formula_lst)

            if utilities.is_tautology(formula_lst):
                print('this formula is a tautology. its proof in sequent calculus:\n')
                node = sequent_calculus.Node([], conclusions)
                sequent_calculus.prove(node)
                node.display()

            else:
                print('this formula is not a tautology and cannot be proved with sequent calculus.')

        except:
            print('invalid input.')

    utilities.variables = []
    formula_str = input('\nenter a propositional formula. enter help for syntax. enter exit to quit the program.\n')