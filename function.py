from asyncio import exceptions
from polynomial import Polynomial
from utils import isnumber


class Function:
    def __init__(self, expr, data, unknown='x'):
        if isinstance(expr, str) is False:
            raise TypeError('Function: Type {} not supported'.format(type(expr).__name__))
        try:
            zero_polynomial = Polynomial(expr.replace(unknown, 'X') + '= 0', unknown)
        except ValueError:
            raise ValueError('Function: Invalid expression syntax')
        self.expr = expr
        self.coefs = zero_polynomial.coefs
        self.degree = zero_polynomial.degree
        self.unknown = unknown

    def image(self, x):
        try:
            x = int(x)
        except Exception:
            raise ValueError('Function: Invalid number')
        im = [0] * len(self.coefs)
        for i, coef in enumerate(self.coefs):
            im[i] = coef * (x ** i)
        return sum(im)

    def resolve(self, y):
        '''
        Resolves f(x) = y
        '''
        print('{} = {}', self.expr, y)
        eq = Polynomial('{} = {}'.format(self.expr.replace(self.unknown, 'X'), y), self.unknown)
        eq.resolve()
    
    def __str__(self) -> str:
        return self.expr
