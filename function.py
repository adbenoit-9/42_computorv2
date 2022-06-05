from calculator import calculator
from ft_complex import Complex
from polynomial import Polynomial
from decompose import decompose
import re


class Function:
    def __init__(self, parser, expr, x='x'):
        if isinstance(expr, str) is False or isinstance(x, str) is False:
            raise ValueError('Function: type error')
        if x.isalpha() is False:
            raise ValueError("parameter '{}' is invalid".format(x))
        regex = r"[^\d\+\-\*\%\/\^;,\.\[\]\(\)i" + x + "]+"
        match = re.search(regex, expr)
        if match is not None and \
                match.group() not in ['cos', 'sin', 'tan', 'abs', 'sqrt']:
            raise ValueError("variable '{}' is undefined".format(match.group()))
        self.x = x
        self.expr = expr
        self.decomposed = decompose(self.expr)
        self.decomposed = parser.start(self.decomposed)

    def image(self, x):
        if isinstance(x, str) or isinstance(x, Complex):
            param = "({})".format(x)
        else:
            param = str(x)
        return self.expr.replace(self.x, param)

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
        print('{} = {}'.format(expr, y))
        expr = expr.replace(x, 'X')
        eq = Polynomial('{} = {}'.format(expr, y), x)
        eq.resolve()

    def __str__(self):
        return self.expr
