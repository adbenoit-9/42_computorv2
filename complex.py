from utils import isnumber
import math

class Complex:
    def __init__(self, real=0, im=0):
        if isnumber(real) is False or isnumber(im) is False:
            raise TypeError('Invalid argument.')
        self.real = real
        self.im = im

    def module(self):
        return math.sqrt(self.real ** 2 + self.im ** 2)

    def copy(self):
        return Complex(self.real, self.im)

    def __iadd__(self, other):
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        self.real += other.real
        self.im += other.im
        return self

    def __isub__(self, other):
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        self.real -= other.real
        self.im -= other.im
        return self

    def __imul__(self, other):
        if isinstance(other, Complex):
            new_real = (self.real * other.real) - (self.im * other.im)
            self.im = (self.real * other.im) + (self.im * other.real)
            self.real = new_real
        elif isnumber(other):
            self.real *= other
            self.im *= other
        else:
            raise TypeError('Invalid type')
        return self

    def __itruediv__(self, other):
        if isinstance(other, Complex):
            d = other.real * other.real + other.im * other.im
            if d == 0:
                raise ValueError('Division by 0')
            new_real = (self.real * other.real + self.im * other.im) / d
            self.im = (self.im * other.real - self.real * other.im) / d
            self.real = new_real
        elif isnumber(other):
            self.real /= other
            self.im /= other
        else:
            raise TypeError('Invalid type')
        return self

    def __add__(self, other):
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        return (Complex(real=self.real + other.real, im=self.im + other.im))

    def __sub__(self, other):
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        return (Complex(real=self.real - other.real, im=self.im - other.im))

    def __mul__(self, other):
        if isinstance(other, Complex):
            real = (self.real * other.real) - (self.im * other.im)
            im = (self.real * other.im) + (self.im * other.real)
        elif isnumber(other):
            real = self.real * other
            im = self.im * other
        else:
            raise TypeError('Invalid type')
        return Complex(real=real, im=im)

    def __truediv__(self, other):
        if isinstance(other, Complex):
            d = other.real * other.real + other.im * other.im
            if d == 0:
                raise ValueError('Division by 0')
            real = (self.real * other.real + self.im * other.im) / d
            im = (self.im * other.real - self.real * other.im) / d
        elif isnumber(other):
            real = self.real / other
            im = self.im / other
        else:
            raise TypeError('Invalid type')
        return Complex(real=real, im=im)

    def __eq__(self, other):
        if isinstance(other, Complex) is False:
            raise TypeError('only Complex')
        return (self.real == other.real) and (self.im == other.im)
        

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.im < 0:
            return "{real} + {im}i".format(real=self.real, im=self.im)
        else:
            return "{real} - {im}i".format(real=self.real, im=abs(self.im))
