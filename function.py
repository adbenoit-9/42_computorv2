from calculator import calculator
from ft_complex import Complex
from polynomial import Polynomial
from decompose import decompose
from utils import put_space
import re


class Function:
    def __init__(self, parser, expr, x='x'):
        if isinstance(expr, str) is False or isinstance(x, str) is False:
            raise ValueError('Function: type error')
        if x.isalpha() is False or x in ['cos', 'sin', 'tan', 'abs', 'sqrt', 'i', 'exp']:
            raise ValueError("parameter '{}' is invalid".format(x))
        regex = r"[^\d\+\-\*\%\/\^;,\.\[\]\(\) ]+"
        match = re.search(regex, expr)
        if match is not None and \
                match.group() not in ['cos', 'sin', 'tan', 'abs', 'sqrt', 'i', 'exp', x]:
            raise ValueError("variable '{}' undefined".format(match.group()))
        self.x = x
        self.expr = expr
        self.decomposed = decompose(self.expr)
        self.decomposed = parser.start(self.decomposed)

    def image(self, x):
        if isinstance(x, str) or isinstance(x, Complex):
            param = "({})".format(x)
        else:
            param = str(x)
        regex = r"[a-z]*" + self.x + r"[a-z]*\(?"
        matches = re.finditer(regex, self.expr)
        expr = self.expr
        i = 0
        for match in matches:
            if match.group() == self.x:
                expr = expr[:match.span()[0] + i] + param + expr[match.span()[1] + i:]
                i += len(param) - len(self.x)
        print(expr)
        return expr

    def resolve(self, x, y, parser):
        '''
        Resolves f(x) = y
        '''
        if isinstance(parser.str_to_value(x), str) is False:
            x = parser.str_to_value(calculator(x, parser))
            if x == y:
                print('Each real number is a solution.')
            else:
                print("No solution.")
            return
        y = parser.start(y)
        y = decompose(y)
        y = parser.start(y)
        expr = self.decomposed
        print('{} = {}'.format(put_space(expr), y))
        expr = expr.replace(x, 'X')
        eq = Polynomial('{} = {}'.format(expr, y), x)
        eq.resolve()

    def __str__(self):
        return put_space(self.expr)
