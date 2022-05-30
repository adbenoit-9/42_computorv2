from polynomial import Polynomial
from utils import isnumber


class Function:
    def __ini__(self, expr):
        if isinstance(expr, Polynomial) is False:
            raise TypeError('Type {} not support'.format(type(expr).__name__))
        self.expr = expr

    def image(self, x):
        if isnumber(x) is False:
            raise ValueError('Invalid value')
        im = 0
        for i, val in enumerate(self.expr.values):
            im += val * x ** i
        return im
