import math


def isrealnumber(n):
    if isinstance(n, float) or isinstance(n, int):
        return True
    return False


class Complex:
    def __init__(self, real=0, im=0):
        if isrealnumber(real) is False or isrealnumber(im) is False:
            raise TypeError('Invalid argument.')
        self.real = real
        self.im = im

    def module(self):
        return math.sqrt(self.real ** 2 + self.im ** 2)

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
        return self.__sub__(other)

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
        if isrealnumber(n) is False:
            raise ValueError('Invalid type')
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
        if isinstance(self.im, float) and self.im.is_integer():
            self.im = int(self.im)
        if isinstance(self.real, float) and self.real.is_integer():
            self.real = int(self.real)
        if self.im >= 0:
            return "{real} + {im}i".format(real=self.real, im=self.im)
        else:
            return "{real} - {im}i".format(real=self.real, im=abs(self.im))
