from calculator import calculator
from ft_complex import Complex
from polynomial import Polynomial
from decompose import decompose
import re


class Function:
    def __init__(self, expr, x='x'):
        if isinstance(expr, str) is False:
            raise ValueError('Function: Type {} not supported'.format(type(expr).__name__))
        self.expr = expr
        self.x = x

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
        expr = decompose(self.expr)
        expr = parser.start(expr)
        regex = self.x + r"( \* " + self.x + ")+"
        match = re.search(regex, expr)
        while match is not None:
            i = match.group().count(self.x)
            expr = expr.replace(match.group(), "{}^{}".format(self.x, i))
            match = re.search(regex, expr)
        expr = expr.replace(self.x, x)
        print('{} = {}'.format(expr, y))
        expr = expr.replace(x, 'X')
        eq = Polynomial('{} = {}'.format(expr, y), x)
        eq.resolve()

    def __str__(self):
        return self.expr
