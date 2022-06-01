from function import Function
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
        self.state = None
        self.type = None
        self.data = data
        self.param = None

    def start(self, expr, expr_type, param=None):
        type_list = ['function', 'f', 'funct', 'variable', 'var', 'v']
        if isinstance(expr, str) is False or \
                isinstance(expr_type, str) is False or \
                expr_type not in type_list:
            raise ValueError('Parser: invalid argument')
        self.state = self.BEGIN
        self.type = expr_type
        self.param = param
        self.expr = self.replace(expr)
        if expr_type in type_list[:3]:
            return Function(self.expr, self.data, param)
        else:
            return self.calculate()

    def format_val(self, value, i):
        if isinstance(value, str):
            return "{} ".format(value)
        if value < 0:
            return "- {} ".format(value)
        elif i != 0:
            return "+ {} ".format(value)
        return "{} ".format(value)

    def var_replace(self, expr):
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

    def pow_replace(self, expr):
        regex = r"(?P<x1>[\d\.]+)[\^](?P<x2>[\d\.]+)"
        tmp = 0
        calc = re.search(regex, expr)
        unknown = None
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

    def replace(self, expr):
        new_expr = self.var_replace(expr)
        expr = self.pow_replace(expr)
        regex = r"[\w\.\^]+([\*\/%]{1,2}[\w\.\^]+)*"
        r2 = r"(?P<x1>[\w\.\^]+)(?P<op>[\*\/%]{1,2})(?P<x2>[\w\.\^]+)"
        matches = re.finditer(regex, expr)
        new_expr = ""
        tmp = 0
        for elem in matches:
            token = elem.group()
            start, end = elem.span()
            calc = re.search(r2, token)
            unknown = None
            while calc is not None:
                try:
                    x1 = self.get_value(calc.group('x1'))
                    x2 = self.get_value(calc.group('x2'))
                    op = calc.group('op')
                    x = self.do_operation(x1, x2,op)
                    token = '{}{}'.format(x, token[calc.span()[1]:])
                except:
                    unknown = op + ' '
                    unknown += x1 if isinstance(x1, str) else x2
                    token = (str(x2) if isinstance(x1, str) else str(x1)) + token[calc.span()[1]:]
                calc = re.search(r2, token)
            new_expr += expr[tmp:start]
            if len(expr[tmp:start]):
                new_expr += ' '
            if len(token):
                new_expr += token + ' '
            if unknown is not None:
                new_expr += unknown + ' '
            tmp = end
        return new_expr

    def calculate(self):
        expr = self.expr.replace(' ', '')
        tokens = self.split(expr, '+-')
        result = 0
        for i, token in enumerate(tokens):
            value = self.get_value(token)
            if isinstance(value, str):
                raise ValueError("(CGI) Variable '{}' is undefined".format(value))
            result += self.get_value(token)
        return result

    # UTILS

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

    def split(self, string, sep, rm_sep=0):
        if isinstance(string, str) is False or \
                isinstance(sep, str) is False or \
                isinstance(rm_sep, int) is False:
            raise ValueError('Parser: split failed')
        tokens = []
        tmp = 0
        for i, c in enumerate(string):
            if c in sep and i != 0:
                tokens.append(string[tmp:i])
                tmp = i + rm_sep
        if tmp < len(string):
            tokens.append(string[tmp:])
        return tokens

    def do_operation(self, x1, x2, op):
        if isinstance(x1, str) or isinstance(x2, str):
            raise ValueError('invalid operation')
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
            result = x1 * x2
        else:
            raise ValueError('Parser: invalid operation ')
        return result
