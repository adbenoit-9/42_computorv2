from dataclasses import replace
import math
from unittest import result
from function import Function
from ft_matrix import Matrix
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

    def replace_var(self, expr):
        matches = re.finditer(r"[\w_\(\)]+", expr)
        new_expr = expr
        for elem in matches:
            var = elem.group()
            match = re.fullmatch(r"(?P<name>[\w_]+)[\(](?P<param>[\w_]+)[\)]", var)
            if match is not None:
                name = match.group('name')
                param = match.group('param')
            else:
                name = var
            if name in self.data.keys():
                if match is None:
                    value = str(self.data[name])
                else:
                    value = str(self.data[name].image(param))
                new_expr = new_expr.replace(var, value)
            elif match is not None:
                raise ValueError("Function '{}' is undefined.".format(name))
        return new_expr

    def calculate_pow(self, expr):
        regex = r"(?P<x1>[\d\.]+)[\^](?P<x2>[\d\.]+)"
        tmp = 0
        calc = re.search(regex, expr)
        new_expr = expr
        while calc is not None:
            x1 = self.get_value(calc.group('x1'))
            x2 = self.get_value(calc.group('x2'))
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
        expr = self.calculate_pow(expr)
        regex = r"[\w\.\^]+([^\w\^\.\(\)\[\],;\-\+]+[\w\.\^]+)*"
        r2 = r"(?P<x1>[\w\.\^]+)(?P<op>[^\w\^\.\(\)\[\],;\-\+]+)(?P<x2>[\w\.\^]+)"
        matches = re.finditer(regex, expr)
        for elem in matches:
            operation = elem.group()
            result = operation
            calc = re.search(r2, result)
            unknown = None
            while calc is not None:
                try:
                    x1 = self.get_value(calc.group('x1'))
                    x2 = self.get_value(calc.group('x2'))
                    op = calc.group('op')
                    x = self.do_operation(x1, x2,op)
                    result = '{}{}'.format(x, result[calc.span()[1]:])
                except TypeError:
                    unknown = op
                    unknown += x1 if isinstance(x1, str) else x2
                    result = (str(x2) if isinstance(x1, str) else str(x1)) + result[calc.span()[1]:]
                calc = re.search(r2, result)
            if unknown is not None:
                result += unknown
            expr = expr.replace(operation, result)
        self.rm_useless_brackets(expr)
        return self.put_space(expr)

    def controller(self, expr):
        regex = r"\([^\(\)]+\)"
        matches = list(re.finditer(regex, expr))
        n = len(matches)
        for match in matches:
            result = self.calculate(match.group()[1:-1])
            expr = expr.replace(match.group(), str(result))
            expr = self.format(expr.replace(' ', ''))
            print(expr)
        if n:
            return self.controller(expr)
        return expr

        
    def calculate(self, expr):
        tokens = expr.split()
        result = 0
        value = 0
        op = None
        for i, token in enumerate(tokens):
            if token in '-+':
                op = token
                continue
            value = self.get_value(token)
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

    def get_value(self, x):
        if x in self.data.keys() and (self.param is None or x != self.param):
            return self.data[x]
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
            if isinstance(x1, Matrix) is False or isinstance(x2, Matrix):
                raise ValueError("operator '**' not supported between '{}' and '{}'."
                                .format(type(x1).__name__, type(x2).__name__))
            result = x1 * x2
        else:
            raise ValueError("operator '{}' not supported.".format(op))
        return result
