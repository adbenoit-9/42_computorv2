from dataclasses import replace
import math
from multiprocessing.sharedctypes import Value
from unittest import result
from function import Function
from ft_matrix import Matrix
from ft_complex import Complex
import re

class Parser:
    '''Parse a mathematic expression.'''
    ERROR = -1,
    BEGIN = 0,
    MUL = 1,
    DIV = 2,
    MOD = 3,
    ADD = 4,
    SUB = 5,
    END = 10

    def __init__(self, data) -> None:
        self.expr = None
        self.format_expr = None
        self.state = None
        self.type = None
        self.data = data
        self.param = None
        self.re_operator = r"[^\w\^\.\(\)\[\],;]+"

    def start(self, expr, expr_type, param=None):
        type_list = ['function', 'f', 'funct', 'variable', 'var', 'v']
        if isinstance(expr, str) is False or \
                isinstance(expr_type, str) is False or \
                expr_type not in type_list:
            raise ValueError('Parser: invalid argument')
        self.state = self.BEGIN
        self.type = expr_type
        self.param = param
        self.expr = expr
        self.format_expr = self.format(expr)
        if expr_type in type_list[:3]:
            return Function(self.format_expr, self.data, param)
        else:
            result = self.controller(self.format_expr)
            return self.calculate(result)

    def replace_funct(self, expr):
        math_funct = {
            'cos': math.cos,
            'sin': math.sin,
            'tan': math.tan,
            'exp': math.exp,
            'abs': abs,
            'sqrt': math.sqrt,
        }
        matches = re.finditer(r"(?P<name>[\w_]+)[\(](?P<param>[\w\.\[\],;]+|[\w\.\[\],;]*[+-]?[\w\.\[\],;]*[\*]?[i])[\)]", expr)
        for match in matches:
            funct = match.group()
            name = match.group('name')
            param = self.str_to_value(match.group('param'))
            if isinstance(param, str) and self.type == 'funct':
                continue
            elif isinstance(param, str):
                raise ValueError("variable '{}' is undefined.".format(param))
            if name in math_funct.keys():
                value = math_funct[name](param)
            elif name in self.data.keys():
                value = self.data[name].image(param)
            elif name not in math_funct:
                raise ValueError("function '{}' is undefined.".format(name))
            expr = expr.replace(funct, str(value))
        return expr

    def replace_var(self, expr):
        matches = re.finditer(r"[\w_]+", expr)
        new_expr = expr
        for elem in matches:
            var = elem.group()
            name = var
            if name in self.data.keys():
                value = self.data[name]
                if isinstance(value, Function) is False:
                    new_expr = new_expr.replace(var, str(value))
        return new_expr

    def calculate_pow(self, expr):
        regex = r"(?P<x1>[\d\.]+)[\^](?P<x2>[\d\.]+)"
        tmp = 0
        calc = re.search(regex, expr)
        new_expr = expr
        while calc is not None:
            x1 = self.str_to_value(calc.group('x1'))
            x2 = self.str_to_value(calc.group('x2'))
            start, end = calc.span()
            if start != 0 and new_expr[start - 1] == '^':
                x = self.do_operation(x1, x2, '*')
            else:
                x = self.do_operation(x1, x2, '^')
            new_expr = '{}{}{}'.format(new_expr[:start], x, new_expr[end:])
            calc = re.search(regex, new_expr)
        return new_expr

    def format(self, expr):
        expr = self.replace_var(expr)
        expr = self.replace_funct(expr)
        expr = self.calculate_pow(expr)
        regex = r"[\w\^\.\(\)\[\],;\-\+]+([^\w\^\.\(\)\[\],;\-\+]+[\w\^\.\(\)\[\],;\-\+]+)*"
        r2 = r"(?P<x1>[\w\^\.\(\)\[\],;\-\+]+)(?P<op>[^\w\^\.\(\)\[\],;\-\+]+)(?P<x2>[\w\^\.\(\)\[\],;\-\+]+)"
        matches = re.finditer(regex, expr)
        for elem in matches:
            operation = elem.group()
            result = operation
            calc = re.search(r2, result)
            unknown = None
            while calc is not None:
                try:
                    x1 = self.str_to_value(calc.group('x1'))
                    x2 = self.str_to_value(calc.group('x2'))
                    op = calc.group('op')
                    x = self.do_operation(x1, x2,op)
                    result = '{}{}'.format(x, result[calc.span()[1]:])
                except TypeError:
                    unknown = op
                    unknown += x1 if isinstance(x1, str) else x2
                    result = (str(x2) if isinstance(x1, str) else str(x1)) + result[calc.span()[1]:]
                calc = re.search(r2, result)
                if result == calc.group() and isinstance(self.str_to_value(calc.group()), Complex):
                    break
            if unknown is not None:
                result += unknown
            expr = expr.replace(operation, result)
        expr = self.replace_funct(expr)
        expr = self.rm_useless_brackets(expr)
        return self.put_space(expr)

    def controller(self, expr):
        if isinstance(self.str_to_value(expr), Complex):
            return self.format(expr.replace(' ', ''))
        regex = r"[^\w\_]\([^\(\)]+\)"
        matches = list(re.finditer(regex, expr))
        n = len(matches)
        for match in matches:
            result = self.calculate(match.group()[1:-1])
            expr = expr.replace(match.group(), '({})'.format(result))
            expr = self.format(expr.replace(' ', ''))
        if n:
            return self.controller(expr)
        return self.format(expr.replace(' ', ''))

        
    def calculate(self, expr):
        tokens = expr.split()
        result = 0
        value = 0
        op = None
        for i, token in enumerate(tokens):
            if token in '-+':
                op = token
                continue
            value = self.str_to_value(token)
            if op is not None:
                try:
                    result = self.do_operation(result, value, op)
                except TypeError as err:
                    raise ValueError(err)
            else:
                result = value
        return result

    # UTILS

    def rm_useless_brackets(self, expr):
        regex = r"\([\w\.\^\[\],;]+\)"
        matches = re.finditer(regex, expr)
        for elem in matches:
            expr = expr.replace(elem.group(), elem.group()[1:-1])
        return expr

    def put_space(self, expr):
        matches = re.finditer(self.re_operator, expr)
        op = []
        for elem in matches:
            if elem.group() not in op:
                expr = expr.replace(elem.group(), " {} ".format(elem.group()))
            op.append(elem.group())
        return expr

    def str_to_matrix(self, mat):
        if isinstance(mat, str) is False:
            raise ValueError("str_to_matrix: type '{}' not supported"
                             .format(type(mat).__name__))
        if len(mat) < 2:
            return None
        if mat[0] != '[' or mat[-1] != ']':
            return None
        rows = mat[1:-1].split(';')
        lst = [[] for _ in range(len(rows))]
        for i, row in enumerate(rows):
            elem_lst = row[1:-1].split(',')
            for elem in elem_lst:
                lst[i].append(self.str_to_value(elem))
        return Matrix(lst)

    def str_to_complex(self, comp):
        if isinstance(comp, str) is False:
            raise ValueError("str_to_complex: type '{}' not supported"
                             .format(type(comp).__name__))
        re_im = r"([\d\.+-]+)?([\d\.\+\-]+[\*])?i{1}"
        match = re.fullmatch(re_im, comp)
        if match is None:
            return None
        re_nb = r"[+-]?[\d\.]+"
        matches = list(re.finditer(re_nb, comp))
        n = len(matches)
        if n == 0:
            return Complex(im=1)
        elif n == 1:
            if comp[matches[0].span()[1]] == '*':
                return Complex(im=float(matches[0].group()))
            return Complex(real=float(matches[0].group()), im=1)
        return Complex(real=float(matches[0].group()), im=float(matches[1].group()))

    def str_to_value(self, x):
        if isinstance(x, str) is False:
            raise ValueError("str_to_value: type '{}' not supported"
                             .format(type(x).__name__))
        if x in self.data.keys() and (self.param is None or x != self.param):
            return self.data[x]
        comp = self.str_to_complex(x)
        if comp is not None:
            return comp
        mat = self.str_to_matrix(x)
        if mat is not None:
            return mat
        try:
            x = float(x)
            if x.is_integer():
                return int(x)
            return x
        except Exception:
            return x

    def do_operation(self, x1, x2, op):
        if isinstance(x1, str) or isinstance(x2, str):
            raise TypeError("operation between '{}' and '{}' not supported"
                            .format(type(x1).__name__, type(x2).__name__))
        print(x1, op, x2)
        if op == '+':
            result = x1 + x2
        elif op == '-':
            result = x1 - x2
        elif op == '*':
            result = x1 * x2
        elif op == '/':
            result = x1 / x2
        elif op == '%':
            result = abs(x1) % abs(x2)
            result =  -result if x1 < 0 else result
        elif op == '^':
            result = x1 ** x2
        elif op == '**':
            if isinstance(x1, Matrix) is False and isinstance(x2, Matrix):
                raise ValueError("operator '**' not supported between '{}' and '{}'."
                                .format(type(x1).__name__, type(x2).__name__))
            result = x1.dot(x2)
        else:
            raise ValueError("operator '{}' not supported.".format(op))
        return result
