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
    def __init__(self, polynomial, unknown='x') -> None:
        if isinstance(polynomial, str) is False:
            raise ValueError("Only str is accepted")
        try:
            self.coefs = parse_polynomial(polynomial)
            if self.coefs is None:
                raise ValueError('Invalid Polynomial')
            self.degree = len(self.coefs) - 1
            while self.coefs[self.degree] == 0. and self.degree > 0:
                self.degree -= 1
            self.unknown = unknown
        except ValueError:
            raise ValueError('Invalid Polynomial')

    def reduce_form(self):
        return self.__str__()

    def null_delta_step(self):
        form2 = "{unkown} = {num} / {denom}"
        form3 = "{unkown} = {result}"
        b = -self.coefs[1]
        denom = 2 * self.coefs[2]
        print(form2.format(unknown=self.unknown, num=b, denom=denom))
        ret, k = pgcd(denom, b)
        if ret is True:
            b = int(b / k)
            denom = int(denom / k)
            if denom != 1:
                print(form2.format(unknown=self.unknown, num=b, denom=denom))
        result = b / denom
        if result.is_integer():
            result = int(result)
        print(form3.format(result=result))

    def positive_delta_step(self, delta):
        form4 = "{unkown}{k} = {num} / {denom}"
        form5 = "{unkown}{k} = {result}"
        for i in range(2):
            data = {
                'k': i + 1,
                'b': -self.coefs[1],
                'sign': '-' if i == 0 else '+',
                'delta': delta,
                'sqrt_delta': math.sqrt(delta),
                'a': self.coefs[2],
                'unknown': self.unknown
            }
            denom = 2 * data['a']
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
                if denom != 1:
                    print(form4.format(k=data['k'], num=num, denom=denom))
            result = num / denom
            if result.is_integer():
                result = int(result)
            print(form5.format(k=data['k'], result=result))
            if i == 0:
                print('')

    def negative_delta_step(self, delta):
        form3 = "{unkown}{k} = {b} / {d1} {sign} i * sqrt({delta}) / {d2}"
        form4 = "{unkown}{k} = {b} / {d1} {sign} i * {sqrt_delta} / {d2}"
        for i in range(2):
            data = {
                'k': i + 1,
                'b': -self.coefs[1],
                'sign': '-' if i == 0 else '+',
                'delta': -delta,
                'sqrt_delta': math.sqrt(-delta),
                'a': self.coefs[2],
                'denom': 2 * self.coefs[2],
                'unknown': self.unknown
            }
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
            if self.coefs[0] != 0.:
                print("No solution.")
            else:
                print('Each real number is a solution.')
            return True
        elif self.degree == 1:
            print("The solution is:")
            b = -self.coefs[0]
            denom = self.coefs[1]
            x = b / denom
            ret, k = pgcd(denom, b)
            if ret is True:
                b = int(b / k)
                denom = int(denom / k)
                if denom != 1:
                    print("{} = {} / {}".format(self.unknown, x))
            print("{} = {}".format(self.unknown, x))
            return True
        delta = self.coefs[1] * self.coefs[1] - 4 * \
            self.coefs[2] * self.coefs[0]
        print("Δ = {}^2 - 4 * {} * {} = {}\n".format(self.coefs[1],
                                                     self.coefs[2],
                                                     self.coefs[0],
                                                     delta))
        self.show_step(delta)
        return True

    def show_info(self):
        print('Reduced form: {}'.format(self.reduce_form()))
        print('Polynomial degree: {}'.format(self.degree))

    def __str__(self):
        polynomial = ""
        for i in range(self.degree + 1):
            op = '-' if self.coefs[i] < 0 else '+'
            if i != 0 or op == '-':
                polynomial += "{} ".format(op)
            polynomial += "{} * X^{} ".format(abs(self.coefs[i]), i)
        polynomial += "= 0"
        return polynomial
