from dataclasses import replace
from functools import reduce
import math
from multiprocessing.sharedctypes import Value
from tracemalloc import start
from unittest import result
from function import Function
from ft_matrix import Matrix
from ft_complex import Complex
import re

class Parser:
    '''Parse a mathematic expression.'''

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
        self.type = expr_type
        self.param = param
        self.expr = expr
        self.format_expr = self.format(expr)
        decomposed = self.decompose(self.format_expr)
        print(decomposed)
        if expr_type in type_list[:3]:
            expr = self.put_space(self.format_expr)
            return Function(expr, decomposed, param)
        else:
            return self.calculate(decomposed)


    def decompose(self, expr):
        begin = expr.rfind('(')
        if begin == -1:
            return self.format(expr)
        match = expr[begin:]
        end = match.find(')')
        if end == -1:
            raise ValueError("')' is missing")
        end += begin + 1
        if begin > 0 and expr[begin - 1] in '*/':
            op = expr[begin - 1]
            for i in range(begin - 1, 0, -1):
                if expr[i] in "*/%()":
                    match = expr[i - 1:end]
                    break
        elif end < len(expr) and expr[end] in '*/':
            op = expr[end]
            for i in range(end + 1, len(expr)):
                if expr[i] in "*/%()":
                    match = expr[begin:i]
                    break
        else:
            return self.decompose(expr.replace(expr[begin:end],
                                  expr[begin + 1:end - 1]))
        i = match.find(op)
        tokens = [match[:i], match[i + 1:]]
        new_expr = ""
        for i in range(len(tokens)):
            if re.fullmatch(r"\(.+\)", tokens[i]) is None:
                tokens[i] = [tokens[i]]
            else:
                tokens[i] = tokens[i][1:-1].split('+')
        for i in range(1, len(tokens)):
            for j in range(len(tokens[i - 1])):
                for k in range(len(tokens[i])):
                    if len(new_expr) != 0:
                        new_expr += '+'
                    new_expr += tokens[i - 1][j] + op + tokens[i][k]
        expr = expr.replace(match, new_expr)
        return self.decompose(expr)

    def replace_funct(self, expr):
        math_funct = {
            'cos': math.cos,
            'sin': math.sin,
            'tan': math.tan,
            'exp': math.exp,
            'abs': abs,
            'sqrt': math.sqrt,
        }
        matches = re.finditer(r"(?P<name>[\w_]+)[\(](?P<param>.*)[\)]", expr)
        for match in matches:
            funct = match.group()
            name = match.group('name')
            param = match.group('param')
            if isinstance(self.str_to_value(name), str) is False and \
                    isinstance(self.str_to_value(name), Function) is False:
                expr = expr[:match.span()[0] + len(name)] + '*' + expr[match.span()[0] + len(name):]
                continue
            if len(param) == 0:
                raise ValueError('function parameter not found.')
            param = self.str_to_value(param)
            op = r"[(\*\/%+-]"
            if isinstance(param, str) and re.search(op, param) is not None:
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

    def reduce(self, expr):
        regex = r"(?P<x1>[-]{,1}[\w\^\.\[\],;]+)(?P<op>[^\w\^\.\(\)\[\],;\-\+]+)(?P<x2>[-]{,1}[\w\^\.\[\],;]+)"
        match = re.search(regex, expr)
        if match is None:
            return expr
        operation = match.group()
        result = operation
        x1 = self.str_to_value(match.group('x1'))
        x2 = self.str_to_value(match.group('x2'))
        op = match.group('op')
        result = self.do_operation(x1, x2,op)
        expr = expr.replace(operation, str(result))
        if isinstance(result, str):
            size = len(x1) if isinstance(x1, str) else len(x2)
            rest = expr[match.span()[1]:]
            if len(rest):
                size = len(x1) if isinstance(x1, str) else len(x2)
                rest = expr[match.span()[1] - size:]
                return expr.replace(rest, self.reduce(rest))
            return expr
        expr = self.rm_useless_brackets(expr)
        return self.reduce(expr)

    def format(self, expr):
        if isinstance(expr, str) is False:
            raise ValueError("Parse: format: bad argument, '{}' not supprted".format(type(expr).__name__))
        expr = expr.replace(' ', '')
        expr = self.replace_var(expr)
        expr = self.replace_funct(expr)
        expr = self.calculate_pow(expr)
        expr = self.rm_useless_brackets(expr)
        expr = self.reduce(expr)
        expr = self.replace_funct(expr)
        return expr
        
    def calculate(self, expr):
        tokens = self.split(expr)
        result = 0
        value = 0
        op = None
        for i, token in enumerate(tokens):
            if token in '-+':
                op = token
                continue
            if token in '*/%':
                return expr
            value = self.str_to_value(token)
            if op is not None:
                result = self.do_operation(result, value, op)
            else:
                result = value
        if op is None:
            return expr
        return result

    # UTILS

    def rm_useless_brackets(self, expr):
        regex = r"\([^\+\-\*\/%\(\)]*\)"
        matches = list(re.finditer(regex, expr))
        change = 1
        while len(matches) and change:
            change = 0
            for elem in matches:
                span = elem.span()
                if span[0] != 0 and expr[span[0] - 1] not in "*%/-+(":
                    continue
                change = 1
                expr = expr.replace(elem.group(), elem.group()[1:-1])
            matches = list(re.finditer(regex, expr))
        return expr

    def put_space(self, expr):
        matches = re.finditer(self.re_operator, expr)
        op = []
        for elem in matches:
            if elem.group() not in op:
                expr = expr.replace(elem.group(), " {} ".format(elem.group()))
            op.append(elem.group())
        return expr

    def split(self, expr):
        matches = re.finditer(self.re_operator, expr)
        tokens = []
        tmp = 0
        for elem in matches:
            begin, end = elem.span()
            tokens.append(expr[tmp:begin])
            tokens.append(elem.group())
            tmp = end
        tokens.append(expr[tmp:])
        for i in range(len(tokens)):
            tokens[i] = tokens[i].strip()
        return tokens

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
            if comp[matches[0].span()[1]] == '*' or comp[matches[0].span()[1]] == 'i':
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
        if isinstance(x2, str):
            return "{}{}{}".format(x1, op, x2)
        elif isinstance(x1, str):
            return "{}{}{}".format(x2, op, x1)
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
