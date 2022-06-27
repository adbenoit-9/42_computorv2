class Real:
    def __init__(self, n):
        if isinstance(n, float) or isinstance(n, int) or isinstance(n, str):
            self.value = float(n)
        elif isinstance(n, Real):
            self.value = n.value
        else:
            print(type(n))
            raise TypeError('must be int or float')

    def is_integer(self):
        return self.value.is_integer()

    def __str__(self):
        return "{:f}".format(self.value).rstrip('0').rstrip('.')

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.value + other)
        elif isinstance(other, Real):
            return Real(self.value + other.value)
        else:
            return other + self.value

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.value - other)
        elif isinstance(other, Real):
            return Real(self.value - other.value)
        else:
            return self.value - other

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.value * other)
        elif isinstance(other, Real):
            return Real(self.value * other.value)
        else:
            return other * self.value

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(self.value / other)
        elif isinstance(other, Real):
            return Real(self.value / other.value)
        else:
            return self.value / other

    def __rtruediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Real(other / self.value)
        elif isinstance(other, Real):
            return Real(other.val / self.value)
        else:
            return other / self.value

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __pow__(self, other):
        if isinstance(other, Real):
            return Real(self.value ** other.value)
        elif isinstance(other, float) or isinstance(other, int):
            return Real(self.value ** other)
        else:
            return self.value ** other

    def __rpow__(self, other):
        if isinstance(other, Real):
            return Real(other.value ** self.value)
        elif isinstance(other, float) or isinstance(other, int):
            return Real(other ** self.value)
        else:
            return other ** self.value

    def __ipow__(self, other):
        return self.__pow__(self, other)

    def __eq__(self, other):
        if isinstance(other, Real):
            return self.value == other.value
        return other == self.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Real):
            return self.value < other.value
        return self.value < other

    def __gt__(self, other):
        if isinstance(other, Real):
            return self.value > other.value
        return self.value > other

    def __le__(self, other):
        if isinstance(other, Real):
            return self.value <= other.value
        return self.value <= other

    def __ge__(self, other):
        if isinstance(other, Real):
            return self.value >= other.value
        return self.value >= other

    def __mod__(self, other):
        if isinstance(other, Real):
            return Real(self.value % other.value)
        elif isinstance(other, float) or isinstance(other, int):
            return Real(self.value % other)
        return self.value % other

    def __rmod__(self, other):
        if isinstance(other, Real):
            return Real(other.value % self.value)
        elif isinstance(other, float) or isinstance(other, int):
            return Real(other % self.value)
        return other % self.value

    def __imod__(self, other):
        if isinstance(other, Real):
            self.value %= other.value
        else:
            self.value %= other
        return self

    def __neg__(self):
        return Real(-self.value)

    def __pos__(self):
        return Real(self.value)
