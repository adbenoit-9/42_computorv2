from ft_complex import Complex
from polynomial import Polynomial
from utils import put_space, rm_useless_brackets
import re
import sys


class Function:
    def __init__(self, expr, x='x'):
        forbidden = ['cos', 'sin', 'tan', 'abs', 'sqrt', 'i', 'exp']
        if isinstance(expr, str) is False or isinstance(x, str) is False:
            raise ValueError('Function: type error')
        if x.isalpha() is False or x in forbidden:
            raise ValueError("parameter '{}' is invalid".format(x))
        regex = r"[^\d\+\-\*\%\/\^;,\.\[\]\(\) ]+"
        match = re.search(regex, expr)
        if match is not None and \
                match.group() not in forbidden and match.group() != x:
            raise ValueError("variable '{}' undefined".format(match.group()))
        self.x = x
        self.expr = expr

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
                expr = expr[:match.span()[0] + i] + param + \
                       expr[match.span()[1] + i:]
                i += len(param) - len(self.x)
        expr = rm_useless_brackets(expr)
        return expr

    def resolve(self, x, y):
        '''
        Resolves f(x) = y
        '''
        if x is None or y is None:
            raise ValueError('invalid parameters')
        expr = self.image(x)
        print('{} = {}'.format(put_space(expr), y))
        expr = self.image('X')
        y = str(y).replace(x, 'X')
        eq = Polynomial('{} = {}'.format(expr, y), x)
        eq.resolve()

    def __str__(self):
        return self.expr
