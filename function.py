from ft_complex import Complex
from polynomial import Polynomial
from decompose import decompose


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

    def resolve(self, x, y):
        '''
        Resolves f(x) = y
        '''
        expr = decompose(self.expr)
        print('{} = {}'.format(expr, y))
        eq = Polynomial('{} = {}'.format(expr.replace(x, 'X'), x), y)
        eq.resolve()

    def __str__(self):
        return self.expr
