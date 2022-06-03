welcome!
    this is a simple program which prints the proof of any propositional tautology using sequent calculus. 
    the program also prints the formula's truth table. a couple of notes on syntax:
    
    -the program is case sensitive, be careful!
    -list of allowed connectives:
        ['and', 'or', 'then', 'not']
    -formulas and connectives should be separated with commas. variables do not need parentheses around them. examples:
        p, then, (q, then, (not, p)) is a valid formula, whereas 
        p, then, (q, then, not, p) & p, then, (q, then, not p) are not.  