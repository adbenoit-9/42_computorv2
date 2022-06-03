from asyncio import exceptions
from ft_complex import Complex
from ft_matrix import Matrix
from polynomial import Polynomial
from utils import isnumber


class Function:
    def __init__(self, expr, decomposed, unknown='x'):
        if isinstance(expr, str) is False:
            raise TypeError('Function: Type {} not supported'.format(type(expr).__name__))
        try:
            zero_polynomial = Polynomial(decomposed.replace(unknown, 'X') + '= 0', unknown)
        except ValueError:
            raise ValueError('Function: Invalid expression syntax')
        print(expr)
        self.coefs = zero_polynomial.coefs
        self.degree = zero_polynomial.degree
        self.unknown = unknown
        self.expr = expr

    def image(self, x):
        if isinstance(x, str):
            return self.expr.replace(self.unknown, x)
        if isinstance(x, Complex):
            tab = [Complex()] * len(self.coefs)
        elif isinstance(x, Matrix):
            tab = [Matrix(x.shape, 0)] * len(self.coefs)
        else:
            tab = [0] * len(self.coefs)
        for i, coef in enumerate(self.coefs):
            tab[i] = coef * (x ** i)
        im = tab[0]
        for i in range(1, len(tab)):
            im += tab[i]
        return im

    def resolve(self, y, unknown='x'):
        '''
        Resolves f(x) = y
        '''
        self.unknown = unknown
        expr = repr(self)
        print('{} = {}'.format(expr, y))
        eq = Polynomial('{} = {}'.format(expr.replace(self.unknown, 'X'), y), self.unknown)
        eq.resolve()
    
    def __repr__(self) -> str:
        expr = ""
        for i, coef in enumerate(self.coefs):
            if coef < 0:
                expr += ' - '
            elif i != 0:
                expr += ' + '
            expr += '{} * {}^{}'.format(coef, self.unknown, i)
        return expr

    def __str__(self):
        return self.expr
