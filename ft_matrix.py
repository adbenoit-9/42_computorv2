from utils import isrealnumber, isnumber


class Matrix:
    def __init__(self, *args):
        self.values = []
        if isinstance(args[0], list):
            if len(args) != 1:
                raise ValueError('Invalid Matrix')
            n = len(args[0])
            if n == 0:
                self.shape = (0, 0)
            elif isinstance(args[0][0], list) is False:
                raise ValueError('Invalid Matrix')
            m = len(args[0][0])
            self.shape = (m, n)
            for row in args[0]:
                if isinstance(row, list) is False or len(row) != m:
                    raise ValueError('Invalid Matrix')
                for i in row:
                    if isnumber(i) is False:
                        raise ValueError('Invalid Matrix')
            self.values = args[0].copy()
        elif len(args) == 2 and isinstance(args[0], tuple)\
                and isinstance(args[0][0], int)\
                and isinstance(args[0][1], int)\
                and isrealnumber(args[1]):
            self.shape = args[0]
            column = []
            for i in range(self.shape[1]):
                column.append(args[1])
            for i in range(self.shape[0]):
                self.values.append(column)
        else:
            raise ValueError('Invalid argument(s)')

    def copy(self):
        if self.shape == (0, 0):
            return []
        cpy = []
        for elem in self.values:
            if isinstance(elem, list):
                cpy.append(elem.copy())
        return Matrix(cpy)

    def __add__(self, v):
        if isinstance(v, Matrix) is False or self.shape != v.shape:
            raise ValueError("Matrixs must have the same dimensions.")
        res = self.copy()
        for i, row in enumerate(v.values):
            for j, val in enumerate(row):
                res.values[i][j] += val
        return res

    def __radd__(self, v):
        return self.__add__(v)

    def __sub__(self, v):
        if isinstance(v, Matrix) is False or self.shape != v.shape:
            raise ValueError("Matrixs must have the same dimensions.")
        res = self.copy()
        for i, row in enumerate(v.values):
            for j, val in enumerate(row):
                res.values[i][j] -= val
        return res

    def __rsub__(self, v):
        return self.__sub__(v)

    def __mul__(self, n):
        if isinstance(n, Matrix):
            return self.dot(n)
        if isrealnumber(n) is False:
            raise ValueError("A Matrix can be multiplied only by scalar.")
        res = self.copy()
        for i, row in enumerate(res.values):
            for j, val in enumerate(row):
                res.values[i][j] *= n
        return res

    def __rmul__(self, n):
        return self.__mul__(n)

    def __truediv__(self, n):
        if isrealnumber(n) is False:
            raise ValueError("A Matrix can be divided only by scalar.")
        if n == 0:
            raise ValueError("Division by 0")
        res = self.copy()
        for i, row in enumerate(res.values):
            for j, val in enumerate(row):
                res.values[i][j] /= n
        return res

    def __rtruediv__(self, n):
        raise ValueError("A scalar cannot be divided by a Matrix.")

    def __repr__(self):
        return 'Matrix({})'.format(self.values)

    def __str__(self):
        ret = ""
        for i, row in enumerate(self.values):
            ret += '['
            for j, val in enumerate(row):
                ret += ' {} '.format(val)
                if j != self.shape[0] - 1:
                    ret += ','
            if i != self.shape[1] - 1:
                ret += ']\n'
            else:
                ret += ']'
        return ret

    # def dot(self, other):
    #     if isinstance(v, Matrix) is False:
    #         raise ValueError("Matrixs must have the same dimensions.")
    #     vect = [0] * 
    #     for i, row in enumerate(self.values):
    #         for j, val in enumerate(row):
    #     return res

    def T(self):
        if self.shape == (0, 0):
            return []
        res = [[] for _ in range(self.shape[0])]
        for i, row in enumerate(self.values):
            for j, val in enumerate(row):
                res[j].append(val)
        return Matrix(res)
