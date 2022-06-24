from utils import isrealnumber, isnumber
from ft_complex import Complex

class Matrix:
    def __init__(self, *args):
        self.values = []
        if isinstance(args[0], list):
            if len(args) != 1:
                raise ValueError('invalid Matrix')
            m = len(args[0])
            if m == 0:
                self.shape = (0, 0)
            elif isinstance(args[0][0], list) is False:
                raise ValueError('invalid Matrix')
            n = len(args[0][0])
            self.shape = (m, n)
            for row in args[0]:
                if isinstance(row, list) is False or len(row) != n:
                    raise ValueError('invalid Matrix')
                for i in row:
                    if isnumber(i) is False:
                        raise ValueError('invalid Matrix')
            self.values = args[0].copy()
        elif len(args) == 2 and isinstance(args[0], tuple)\
                and isinstance(args[0][0], int)\
                and isinstance(args[0][1], int)\
                and isrealnumber(args[1]):
            self.shape = args[0]
            for i in range(self.shape[0]):
                row = [args[1]] * self.shape[1]
                self.values.append(row)
        else:
            raise ValueError('invalid argument(s)')

    def copy(self):
        if self.shape == (0, 0):
            return []
        cpy = []
        for elem in self.values:
            if isinstance(elem, list):
                cpy.append(elem.copy())
        return Matrix(cpy)

    def __add__(self, v):
        if isinstance(v, Matrix) is False:
            raise TypeError("addition not supported.")
        if self.shape != v.shape:
            raise ValueError("addition between matrices of differents dimensions")
        res = self.copy()
        for i, row in enumerate(v.values):
            for j, val in enumerate(row):
                res.values[i][j] += val
        return res

    def __radd__(self, v):
        return self.__add__(v)

    def __sub__(self, v):
        if isinstance(v, Matrix) is False:
            raise TypeError("substration not supported.")
        if self.shape != v.shape:
            raise ValueError("subtraction between matrices of differents dimensions")
        res = self.copy()
        for i, row in enumerate(v.values):
            for j, val in enumerate(row):
                res.values[i][j] -= val
        return res

    def __rsub__(self, v):
        if isinstance(v, Matrix) is False:
            raise TypeError("substration not supported.")
        return v.__sub__(self)

    def __mul__(self, n):
        if isinstance(n, Matrix):
            if self.shape != n.shape:
                raise ValueError("""
term-to-term multiplication between matrices of differents dimensions""")
            res = self.copy()
            for i, row in enumerate(self.values):
                for j, val in enumerate(row):
                    res.values[i][j] *= n.values[i][j]
            return res
        if isnumber(n) is False:
            raise TypeError("matrix can be multiplied only by scalar")
        res = self.copy()
        for i, row in enumerate(res.values):
            for j, val in enumerate(row):
                res.values[i][j] *= n
        return res

    def __rmul__(self, n):
        return self.__mul__(n)

    def __truediv__(self, n):
        if isrealnumber(n) is False:
            raise TypeError("matrix can be divided only by scalar")
        if n == 0:
            raise ValueError("Division by 0")
        res = self.copy()
        for i, row in enumerate(res.values):
            for j, val in enumerate(row):
                res.values[i][j] /= n
        return res

    def __rtruediv__(self, n):
        raise TypeError("scalar cannot be divided by a Matrix")

    def __repr__(self):
        ret = ""
        for i, row in enumerate(self.values):
            ret += '['
            for j, val in enumerate(row):
                if isinstance(val, float):
                    ret += ' {} '.format(round(val, 4))
                elif isinstance(val, Complex):
                    ret += ' {} '.format(repr(val))
                else:
                    ret += ' {} '.format(val)
                if j != self.shape[1] - 1:
                    ret += ','
            if i != self.shape[0] - 1:
                ret += ']\n'
            else:
                ret += ']'
        return ret

    def __str__(self):
        ret = "["
        for i, row in enumerate(self.values):
            ret += '['
            for j, val in enumerate(row):
                if isinstance(val, float):
                    ret += '{}'.format(round(val, 4))
                elif isinstance(val, Complex):
                    ret += repr(val)
                else:
                    ret += '{}'.format(val)
                if j != self.shape[1] - 1:
                    ret += ','
            if i != self.shape[0] - 1:
                ret += '];'
            else:
                ret += ']'
        ret += ']'
        return ret

    def identity(self, n):
        mat = []
        for i in range(n):
            row = [0] * n
            row[i] = 1
            mat.append(row)
        return Matrix(mat)

    def is_square(self):
        if self.shape[0] == self.shape[1]:
            return True
        else:
            return False

    def __pow__(self, n):
        if isinstance(n, int) is False:
            raise TypeError("invalid power type '{}'".format(type(n).__name__))
        if n < 0:
            raise ValueError("negative power not supported")
        if self.is_square() is False:
            raise ValueError("power supported only on square matrix")
        if n == 0:
            return self.identity(self.shape[0])
        ret = self.copy()
        for i in range(n - 1):
            ret = ret.dot(self)
        return ret

    def dot(self, other):
        if isinstance(other, Matrix) is False:
            raise TypeError("Matrix product with '{}' not supported"
                            .format(type(other).__name__))
        if self.shape[1] != other.shape[0]:
            raise ValueError("product not supported between matrices of dimensions {} and {}."
                             .format(self.shape, other.shape))
        prod = []
        for i in range(self.shape[0]):
            prod.append([0] * other.shape[1])
        for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                for k in range(self.shape[1]):
                    prod[i][j] += self.values[i][k] * other.values[k][j]
        return Matrix(prod)

    def T(self):
        if self.shape == (0, 0):
            return []
        res = [[] for _ in range(self.shape[1])]
        for i, row in enumerate(self.values):
            for j, val in enumerate(row):
                res[j].append(val)
        return Matrix(res)
