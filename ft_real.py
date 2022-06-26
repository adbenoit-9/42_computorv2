class Real:
    def __init__(self, n):
        if isinstance(n, int) is False or \
                isinstance(n, float) is False:
            raise TypeError('must be int or float')
        self.val = float(n)

    def __str__(self):
        if self.val.is_integer():
            return "{}".format(int(self.val))
        return "{:f}".format(self.val)

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.val + other)
        elif isinstance(other, Real):
            return Real(self.val + other.val)
        else:
            return other + self.val

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.val - other)
        elif isinstance(other, Real):
            return Real(self.val - other.val)
        else:
            return -other + self.val

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.val * other)
        elif isinstance(other, Real):
            return Real(self.val * other.val)
        else:
            return other * self.val

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.val / other)
        elif isinstance(other, Real):
            return Real(self.val / other.val)
        else:
            return self.val / other

    def __rdiv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(other / self.val)
        elif isinstance(other, Real):
            return Real(other.val / self.val)
        else:
            return other / self.val

