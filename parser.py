from dataclasses import replace
import math
from function import Function
from ft_matrix import Matrix
from ft_complex import Complex, isrealnumber
from utils import rm_useless_brackets, put_space
import re
from calculator import calculator, do_operation


class Parser:
    '''Parse a mathematic expression.'''

    def __init__(self, data={}, cmd="") -> None:
        if isinstance(cmd, str) is False:
            raise ValueError("Parser: command type '{}' not supported"
                             .format(type(cmd).__name__))
        if data is None:
            data = {}
        self.data = data
        regex = r"[^\w\_\+\-\*\/\(\)\[\];,\.\%\^=\?]"
        match = re.search(regex, cmd)
        if match is not None:
            raise ValueError('illegal character: {}'.format(match.group()))
        i = cmd.count('(') - cmd.count(')')
        j = cmd.count('[') - cmd.count(']')
        if i != 0 or j != 0:
            raise ValueError('syntax error')
        self.cmd = cmd.lower().split('=')
        if len(self.cmd) != 2:
            raise ValueError('syntax error')
        for i in range(len(self.cmd)):
            self.cmd[i] = self.cmd[i].strip()
            if '?' in self.cmd[i]:
                if i == 0 or '?' in self.cmd[i][:-1]:
                    raise ValueError('syntax error')

    def start(self, expr):
        if isinstance(expr, str) is False:
            raise ValueError('Parser: invalid argument')
        expr = expr.replace(' ', '')
        expr = self.put_mul(expr)
        expr = self.replace_var(expr)
        expr = self.replace_funct(expr)
        expr = self.replace_funct(expr)
        expr = self.put_pow(expr)
        expr = self.calculate_pow(expr)
        expr = rm_useless_brackets(expr)
        expr = self.reduce(expr)
        regex = r"[\d\^\.\[\],;]+[^\w\^\.\(\)\[\],;\-\+]+[-]{,1}[\d\^\.\[\],;]+"
        while re.search(regex, expr) is not None:
            expr = self.reduce(expr)
        return expr

    def end(self, result):
        if isinstance(result, str) is False:
            if isinstance(result, Matrix):
                return result.__repr__()
            return result
        tmp = self.str_to_matrix(result)
        if tmp is not None:
            return tmp.__repr__()
        tmp = self.str_to_complex(result)
        if tmp is not None:
            return tmp.__repr__()
        return put_space(result)

    def replace_funct(self, expr):
        math_funct = {
            'cos': math.cos,
            'sin': math.sin,
            'tan': math.tan,
            'exp': math.exp,
            'abs': abs,
            'sqrt': math.sqrt,
        }
        matches = re.finditer(r"(?P<name>[\w_]+)[\(](?P<param>[^\(\)]*)[\)]", expr)
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
            if isinstance(param, str):
                param = calculator(param, self)
            if name in math_funct.keys() and isrealnumber(param):
                value = math_funct[name](param)
                expr = expr.replace(funct, str(value))
            elif name in self.data.keys():
                value = "({})".format(self.data[name].image(param))
                expr = expr.replace(funct, str(value))
            elif name not in math_funct:
                raise ValueError("function '{}' is undefined.".format(name))
        return expr

    def put_mul(self, expr):
        expr = expr.replace(')(', ')*(')
        regex = r"(?P<x1>[\d\[\]\;\,\.]+)(?P<x2>[A-Za-z]+)"
        match = re.search(regex, expr)
        if match is None:
            return expr
        expr = expr.replace(match.group(), "{}*{}"
                            .format(match.group('x1'), match.group('x2')))
        return self.put_mul(expr)

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
        regex = r"(?P<x1>[+-]{,1}[\d\.]+|i)[\^](?P<x2>[-+]{,1}[\d\.]+)"
        calc = re.search(regex, expr)
        new_expr = expr
        while calc is not None:
            x1 = self.str_to_value(calc.group('x1'))
            x2 = self.str_to_value(calc.group('x2'))
            start, end = calc.span()
            if start != 0 and new_expr[start - 1] == '^':
                x = do_operation(x1, x2, '*')
            else:
                x = do_operation(x1, x2, '^')
            if (isrealnumber(x) is False or x > 0) and (start == 0 or new_expr[start - 1] not in '*/%^'):
                new_expr = '{}+{}{}'.format(new_expr[:start], x, new_expr[end:])
            else:
                new_expr = '{}{}{}'.format(new_expr[:start], x, new_expr[end:])
            calc = re.search(regex, new_expr)
        return new_expr

    def put_pow(self, expr):
        regex = r"[\w\^\.]+([*][\w\^\.]+)+"
        matches = re.finditer(regex, expr)
        for match in matches:
            begin = 0
            if match.span()[0] > 0 and expr[match.span()[0] - 1] in "/^%":
                begin = match.group().find('*') + 1
            tokens = match.group()[begin:].split('*')
            new_expr = ""
            used = []
            for token in tokens:
                if token not in used:
                    i = tokens.count(token)
                    used.append(token)
                    if len(new_expr) != 0:
                        new_expr += '*'
                    if i > 1:
                        new_expr += "{}^{}".format(token, i)
                    else:
                        new_expr += token
            expr = expr.replace(match.group()[begin:], new_expr)
        return expr
                
    def reduce(self, expr):
        regex = r"(?P<x1>[-]{,1}[\w\^\.\[\],;]+)(?P<op>[^\w\^\.\(\)\[\],;\-\+]+)(?P<x2>[-]{,1}[\w\^\.\[\],;]+)"
        matches = list(re.finditer(regex, expr))
        if len(matches) == 0:
            return expr
        for match in matches:
                operation = match.group()
                result = operation
                x1 = match.group('x1')
                x2 = match.group('x2')
                if x1 != "i":
                    x1 = self.str_to_value(x1)
                if x2 != "i":
                    x2 = self.str_to_value(x2)
                op = match.group('op')
                result = do_operation(x1, x2, op)
                expr = expr.replace(operation, str(result))
                if isinstance(result, str):
                    size = len(x1) if isinstance(x1, str) else len(x2)
                    rest = expr[match.span()[1]:]
                    if len(rest):
                        size = len(x1) if isinstance(x1, str) else len(x2)
                        rest = expr[match.span()[1] - size:]
                        return expr.replace(rest, self.reduce(rest))
                    return expr
                expr = rm_useless_brackets(expr)
        return expr.replace('+-', '-')

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
        if x in self.data.keys() and isinstance(self.data[x], Function) is False:
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
