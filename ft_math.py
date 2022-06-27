from ft_real import Real
from ft_complex import Complex
from utils import isrealnumber, isnumber


def ft_sqrt(n):
    if isrealnumber(n) is False:
        raise TypeError("must be real number, not '{}'"
                        .format(type(n).__name__))
    iscomplex = False
    if n < 0:
        iscomplex = True
        n *= -1
    sqrt = n / 2.
    while sqrt * sqrt < n:
        sqrt += 1.
    if sqrt * sqrt == n:
        if iscomplex:
            return Complex(0, sqrt)
        return sqrt
    sqrt -= 1.
    tmp = 0.
    while tmp != sqrt:
        tmp = sqrt
        sqrt = (n / tmp + tmp) / 2
    if iscomplex:
        return Complex(0, sqrt)
    return sqrt


def ft_abs(n):
    if isinstance(n, Complex):
        return n.conjugate()
    if isrealnumber(n) is False:
        raise TypeError("must be number, not '{}'"
                        .format(type(n).__name__))
    if n > 0:
        return n
    return n * -1


def pgcd(x, y):
    x = Real(x)
    y = Real(y)
    if x.is_integer() and y.is_integer():
        n = min(int(str(ft_abs(x))), int(str(ft_abs(y))))
        for i in range(n, 1, -1):
            if x % i == 0 and y % i == 0:
                if x < 0 and y < 0:
                    return True, -i
                return True, i
    return False, 1
