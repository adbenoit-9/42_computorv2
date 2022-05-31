from parse_polynomial import parse_polynomial
import math


def pgcd(x, y):
    x = float(x)
    y = float(y)
    if x.is_integer() and y.is_integer():
        n = min(abs(int(x)), abs(int(y)))
        for i in range(n, 1, -1):
            if x % i == 0 and y % i == 0:
                if x < 0 and y < 0:
                    return True, -i
                return True, i
    return False, 1


class Polynomial:
    def __init__(self, polynomial) -> None:
        if isinstance(polynomial, str) is False:
            raise TypeError("Only str is accepted")
        try:
            self.values = parse_polynomial(polynomial)
            if self.values is None:
                raise ValueError('Invalid Polynomial')
            self.degree = len(self.values) - 1
            while self.values[self.degree] == 0. and self.degree > 0:
                self.degree -= 1
        except Exception:
            raise ValueError('Invalid Polynomial')

    def reduce_form(self):
        return self.__str__()

    def null_delta_step(self):
        form1 = "x = {b} / (2 * {a})"
        form2 = "x = {num} / {denom}"
        form3 = "x = {result}"
        b = -self.values[1]
        print(form1.format(a=self.values[2], b=b))
        denom = 2 * self.values[2]
        print(form2.format(num=b, denom=denom))
        ret, k = pgcd(denom, b)
        if ret is True:
            b = int(b / k)
            denom = int(denom / k)
            print(form2.format(num=b, denom=denom))
        result = b / denom
        if result.is_integer():
            result = int(result)
        print(form3.format(result=result))

    def positive_delta_step(self, delta):
        form1 = "x{k} = ({b} {sign} sqrt({delta})) / (2 * {a})"
        form2 = "x{k} = ({b} {sign} sqrt({delta})) / {denom}"
        form3 = "x{k} = ({b} {sign} {sqrt_delta}) / {denom}"
        form4 = "x{k} = {num} / {denom}"
        form5 = "x{k} = {result}"
        for i in range(2):
            data = {
                'k': i + 1,
                'b': -self.values[1],
                'sign': '-' if i == 0 else '+',
                'delta': delta,
                'sqrt_delta': math.sqrt(delta),
                'a': self.values[2]
            }
            print(form1.format(**data))
            denom = 2 * data['a']
            if isinstance(data['sqrt_delta'], float):
                print(form2.format(**data, denom=denom))
            else:
                print(form3.format(**data, denom=denom))
            if i == 0:
                num = data['b'] - data['sqrt_delta']
            else:
                num = data['b'] + data['sqrt_delta']
            if isinstance(num, int) or num.is_integer():
                num = int(num)
                print(form4.format(k=data['k'], num=num, denom=denom))
            ret, k = pgcd(denom, num)
            if ret is True:
                num = int(num / k)
                denom = int(denom / k)
                print(form4.format(k=data['k'], num=num, denom=denom))
            result = num / denom
            if result.is_integer():
                result = int(result)
            print(form5.format(k=data['k'], result=result))
            if i == 0:
                print('')

    def negative_delta_step(self, delta):
        form1 = "x{k} = ({b} {sign} i * sqrt({delta})) / (2 * {a})"
        form2 = "x{k} = ({b} {sign} i * sqrt({delta})) / {denom}"
        form3 = "x{k} = {b} / {d1} {sign} i * sqrt({delta}) / {d2}"
        form4 = "x{k} = {b} / {d1} {sign} i * {sqrt_delta} / {d2}"
        for i in range(2):
            data = {
                'k': i + 1,
                'b': -self.values[1],
                'sign': '-' if i == 0 else '+',
                'delta': -delta,
                'sqrt_delta': math.sqrt(-delta),
                'a': self.values[2],
                'denom': 2 * self.values[2]
            }
            print(form1.format(**data))
            print(form2.format(**data))
            ret, k = pgcd(data['b'], data['denom'])
            d1 = data['denom']
            d2 = data['denom']
            if ret is True:
                data['b'] /= k
                data['b'] = int(data['b'])
                d1 /= k
                d1 = int(d1)
            ret2, k2 = pgcd(data['sqrt_delta'], data['denom'])
            if ret2 is True:
                data['sqrt_delta'] /= k2
                data['sqrt_delta'] = int(data['sqrt_delta'])
                d2 /= k2
                d2 = int(d2)
                print(form4.format(**data, d1=d1, d2=d2))
            else:
                print(form3.format(**data, d1=d1, d2=d2))
            if i == 0:
                print('')

    def show_step(self, delta):
        if isinstance(delta, float) and delta.is_integer():
            delta = int(delta)
        if delta > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            self.positive_delta_step(delta)
        elif delta < 0:
            print('Discriminant is strictly negative, the two solutions are:')
            self.negative_delta_step(delta)
        else:
            print("Discriminant equal to zero, the solution is:")
            self.null_delta_step()

    def resolve(self):
        if self.degree > 2:
            print("The polynomial degree is strictly greater than 2, I can't solve.")
            return False
        elif self.degree == 0:
            if self.values[0] != 0.:
                print("No solution.")
            else:
                print('Each real number is a solution.')
            return True
        elif self.degree == 1:
            print("The solution is:")
            b = -self.values[0]
            denom = self.values[1]
            x = b / denom
            ret, k = pgcd(denom, b)
            print("x = {} / {}".format(-self.values[0], self.values[1]))
            if ret is True:
                b = int(b / k)
                denom = int(denom / k)
                print("x = {} / {}".format(x))
            print("x = {}".format(x))
            return True
        delta = self.values[1] * self.values[1] - 4 * \
            self.values[2] * self.values[0]
        print("Δ = {}^2 - 4 * {} * {} = {}\n".format(self.values[1],
                                                     self.values[2],
                                                     self.values[0],
                                                     delta))
        self.show_step(delta)
        return True

    def show_info(self):
        print('Reduced form: {}'.format(self.reduce_form()))
        print('Polynomial degree: {}'.format(self.degree))

    def __str__(self):
        polynomial = ""
        for i in range(self.degree + 1):
            op = '-' if self.values[i] < 0 else '+'
            if i != 0 or op == '-':
                polynomial += "{} ".format(op)
            polynomial += "{} * X^{} ".format(abs(self.values[i]), i)
        polynomial += "= 0"
        return polynomial
