from ft_real import Real


def isrealnumber(n):
    if isinstance(n, Real):
        return True
    elif isinstance(n, float) or isinstance(n, int):
        return True
    return False


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
        return n.module()
    if isrealnumber(n) is False:
        raise TypeError("must be number, not '{}'"
                        .format(type(n).__name__))
    if n > 0:
        return n
    return n * -1


class Complex:
    def __init__(self, real=0, im=0):
        if isrealnumber(real) is False or isrealnumber(im) is False:
            raise TypeError('Invalid argument.', type(real), type(im))
        self.real = Real(real)
        self.im = Real(im)

    def module(self):
        return ft_sqrt(self.real ** 2 + self.im ** 2)

    def conjugate(self):
        return Complex(self.real, -self.im)

    def copy(self):
        return Complex(self.real, self.im)

    def __iadd__(self, other):
        if isrealnumber(other):
            self.real += other
            return self
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        self.real += other.real
        self.im += other.im
        return self

    def __isub__(self, other):
        if isrealnumber(other):
            self.real -= other
            return self
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        self.real -= other.real
        self.im -= other.im
        return self

    def __imul__(self, other):
        if isrealnumber(other):
            other = Complex(other, 0)
        if isinstance(other, Complex):
            new_real = (self.real * other.real) - (self.im * other.im)
            self.im = (self.real * other.im) + (self.im * other.real)
            self.real = new_real
        elif isrealnumber(other):
            self.real *= other
            self.im *= other
        else:
            raise TypeError('Invalid type')
        return self

    def __itruediv__(self, other):
        if isrealnumber(other):
            other = Complex(other, 0)
        if isinstance(other, Complex):
            d = other.real * other.real + other.im * other.im
            if d == 0:
                raise ValueError('Division by 0')
            new_real = (self.real * other.real + self.im * other.im) / d
            self.im = (self.im * other.real - self.real * other.im) / d
            self.real = new_real
        elif isrealnumber(other):
            self.real /= other
            self.im /= other
        else:
            raise TypeError('Invalid type')
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isrealnumber(other):
            return (Complex(real=self.real + other, im=self.im))
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        return (Complex(real=self.real + other.real, im=self.im + other.im))

    def __rsub__(self, other):
        if isrealnumber(other):
            return (Complex(real=other - self.real, im=-self.im))
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        return (Complex(real=other.real - self.real, im=other.im - self.im))

    def __sub__(self, other):
        if isrealnumber(other):
            return (Complex(real=self.real - other, im=self.im))
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        return (Complex(real=self.real - other.real, im=self.im - other.im))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isrealnumber(other):
            other = Complex(other, 0)
        if isinstance(other, Complex):
            real = (self.real * other.real) - (self.im * other.im)
            im = (self.real * other.im) + (self.im * other.real)
        elif isrealnumber(other):
            real = self.real * other
            im = self.im * other
        else:
            raise TypeError('Invalid type')
        return Complex(real=real, im=im)

    def __rtruediv__(self, other):
        if isrealnumber(other):
            other = Complex(other, 0)
        if isinstance(other, Complex):
            return other.__truediv__(self)
        if isrealnumber(other):
            return Complex(real=other).__truediv__(self)
        raise TypeError('Invalid type')

    def __truediv__(self, other):
        if isrealnumber(other):
            other = Complex(other, 0)
        if isinstance(other, Complex):
            d = other.real * other.real + other.im * other.im
            if d == 0:
                raise ValueError('Division by 0')
            real = (self.real * other.real + self.im * other.im) / d
            im = (self.im * other.real - self.real * other.im) / d
        elif isrealnumber(other):
            real = self.real / other
            im = self.im / other
        else:
            raise TypeError('Invalid type')
        return Complex(real=real, im=im)

    def __pow__(self, n):
        if isrealnumber(n) is False or n.is_integer() is False:
            raise ValueError("invalid power type '{}'"
                             .format(type(n).__name__))
        n = int(n.value)
        if n < 0:
            raise ValueError("negative power not supported")
        res = self.copy()
        for i in range(n - 1):
            res *= self
        return res

    def __eq__(self, other):
        if isrealnumber(other):
            other = Complex(other, 0)
        if isinstance(other, Complex) is True:
            return (self.real == other.real) and (self.im == other.im)
        if isrealnumber(other):
            if self.im == 0 and self.real == other:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        s = ""
        if self.real != 0:
            s += str(self.real)
        if self.im > 0 and self.real != 0:
            s += '+'
        if self.im < 0:
            s += '-'
        if ft_abs(self.im) != 1 and self.im != 0:
            s += "{}*".format(ft_abs(self.im))
        if self.im:
            s += 'i'
        if self.real == 0 and self.im == 0:
            return '0'
        return s

    def __repr__(self):
        s = ""
        if self.real != 0:
            s += str(self.real)
        if self.im > 0 and self.real != 0:
            s += '+'
        if self.im < 0:
            s += '-'
        if ft_abs(self.im) != 1 and self.im != 0:
            s += "{}".format(ft_abs(self.im))
        if self.im:
            s += 'i'
        if self.real == 0 and self.im == 0:
            return '0'
        return s
