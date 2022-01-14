class Node():
    def __init__(self, premises, conclusions):
        self.sequent = []
        self.sequent.append(premises)
        self.sequent.append(conclusions)

        self.left_child = None
        self.right_child = None

    def display_sequent(self):
        sequent = ' '
        for premise in self.sequent[0]:
            for i in range(0, len(premise)):
                sequent += str(premise[i]) + ' '

            sequent += ';'

        if sequent[-1] == ';':
            sequent = sequent[:-1]

        sequent += '|- '

        for conclusion in self.sequent[1]:
            for i in range(0, len(conclusion)):
                sequent += str(conclusion[i]) + ' '

            sequent += ';'

        if sequent[-1] == ';':
            sequent = sequent[:-1]

        return sequent.replace('[', '(').replace(']', ')').replace('\'', '').replace(',', ' ').replace(';', ',')

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        # No child.
        if self.right_child is None and self.left_child is None:
            line = '%s' % self.display_sequent()
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right_child is None:
            lines, n, p, x = self.left_child._display_aux()
            s = '%s' % self.display_sequent()
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left_child is None:
            lines, n, p, x = self.right_child._display_aux()
            s = '%s' % self.display_sequent()
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left_child._display_aux()
        right, m, q, y = self.right_child._display_aux()
        s = '%s' % self.display_sequent()
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def prove(node):

    premises = node.sequent[0]
    conclusions = node.sequent[1]

    if is_axiom(node) or (len(premises) == 0 and len(conclusions) == 0):
        return

    left = []
    right = []

    if len(premises) > 0:
        left = premises[0]

    if len(conclusions) > 0:
        right = conclusions[-1]

    left_child_premises = []
    left_child_conclusions = []
    right_child_premises = []
    right_child_conclusions = []

    if len(left) == 2:
        gamma = premises[1:]
        delta = conclusions

        connective = left[0]
        A = left[1]

        if connective == 'not':

            for formula in gamma:
                left_child_premises.append(formula)

            left_child_conclusions.append(A)

            for formula in delta:
                left_child_conclusions.append(formula)

    elif len(left) == 3:

        gamma = premises[1:]
        delta = conclusions
        A = left[0]
        B = left[2]
        connective = left[1]

        if connective == 'and':

            left_child_premises.append(A)
            left_child_premises.append(B)
            for formula in gamma:
                left_child_premises.append(formula)

            for formula in delta:
                left_child_conclusions.append(formula)

        elif connective == 'or':

            left_child_premises.append(A)
            for formula in gamma:
                left_child_premises.append(formula)

            right_child_premises.append(B)
            for formula in gamma:
                right_child_premises.append(formula)

            for formula in delta:
                left_child_conclusions.append(formula)
                right_child_conclusions.append(formula)

        elif connective == 'then':

            for formula in gamma:
                left_child_premises.append(formula)

            left_child_conclusions.append(A)

            right_child_premises.append(B)
            for formula in gamma:
                right_child_premises.append(formula)

            for formula in delta:
                left_child_conclusions.append(formula)
                right_child_conclusions.append(formula)

    elif len(right) == 2:
        gamma = premises
        delta = conclusions[:-1]

        connective = right[0]
        A = right[1]

        if connective == 'not':

            left_child_premises.append(A)
            for formula in gamma:
                left_child_premises.append(formula)

            for formula in delta:
                left_child_conclusions.append(formula)

    elif len(right) == 3:

        gamma = premises
        delta = conclusions[:-1]
        A = right[0]
        B = right[2]
        connective = right[1]

        if connective == 'and':
            for formula in gamma:
                left_child_premises.append(formula)
                right_child_premises.append(formula)

            for formula in delta:
                left_child_conclusions.append(formula)
                right_child_conclusions.append(formula)

            left_child_conclusions.append(A)
            right_child_conclusions.append(B)

        elif connective == 'or':
            for formula in gamma:
                left_child_premises.append(formula)
            for formula in delta:
                left_child_conclusions.append(formula)

            left_child_conclusions.append(A)
            left_child_conclusions.append(B)

        elif connective == 'then':
            left_child_premises.append(A)

            for formula in gamma:
                left_child_premises.append(formula)
            for formula in delta:
                left_child_conclusions.append(formula)

            left_child_conclusions.append(B)



    if len(left_child_premises) > 0 or len(left_child_conclusions) > 0:
        node.left_child = Node(left_child_premises, left_child_conclusions)
        prove(node.left_child)

    if len(right_child_premises) > 0 and len(right_child_conclusions) > 0:
        node.right_child = Node(right_child_premises, right_child_conclusions)
        prove(node.right_child)


def is_axiom(node):
    premises = node.sequent[0]
    conclusions = node.sequent[1]

    for left in premises:
        for right in conclusions:
            if len(left) == 1 and left == right:
                return True

    return False
