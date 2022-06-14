from ft_math import ft_abs, ft_sqrt
from function import Function
from ft_complex import Complex, isrealnumber
from conversion import str_to_complex, str_to_matrix, str_to_value
from utils import isnumber, rm_useless_brackets, put_space, extract_function
import re
import math
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
        tokens = cmd.lower().split()
        if len(tokens) == 2 and tokens[0] == "show" and tokens[1] == "data":
            self.cmd = [tokens[0] + ' ' + tokens[1]]
            return
        cmd = cmd.replace(' ', '')
        regex = r"\|.+\|"
        match = re.search(regex, cmd)
        while match is not None:
            cmd = cmd.replace(match.group(),
                              "abs({})".format(match.group()[1:-1]))
            match = re.search(regex, cmd)
        regex = r"[^\w\_\+\-\*\/\(\)\[\];,\.\%\^=\?]"
        match = re.search(regex, cmd)
        if match is not None:
            raise ValueError('illegal character: {}'.format(match.group()))
        i = cmd.count('(') - cmd.count(')')
        j = cmd.count('[') - cmd.count(']')
        if i != 0 or j != 0:
            raise ValueError('syntax error')
        self.cmd = cmd.lower().split('=')
        if len(self.cmd) != 2 or len(self.cmd[1]) == 0 or len(self.cmd[0]) == 0:
            raise ValueError('syntax error')
        for i in range(len(self.cmd)):
            self.cmd[i] = self.cmd[i].strip()
            if self.cmd[i][-1] in "*/+-%^":
                raise ValueError('syntax error')
            if '?' in self.cmd[i]:
                if i == 0 or '?' in self.cmd[i][:-1]:
                    raise ValueError('syntax error')

    def start(self, expr):
        if isinstance(expr, str) is False:
            raise ValueError('Parser: invalid argument')
        expr = expr.replace(' ', '')
        expr = self.replace_var(expr)
        expr = self.put_mul(expr)
        expr = self.replace_funct(expr)
        expr = self.put_pow(expr)
        expr = self.calculate_pow(expr).replace('-+', '-')
        expr = rm_useless_brackets(expr)
        expr = self.reduce(expr)
        return expr

    def end(self, result):
        result = str(result)
        if result[-1] in "*/+-%^":
            raise ValueError('syntax error')
        tmp = str_to_matrix(result, self.data)
        if tmp is not None:
            return tmp.__repr__()
        tmp = str_to_complex(result)
        if tmp is not None:
            return tmp.__repr__()
        result = result.replace(' ', '')
        name, param = extract_function(result, "abs")
        while param is not None:
            result = result.replace("abs({})".format(param),
                                    "|{}|".format(param))
            name, param = extract_function(result, "abs")
        return put_space(result)

    def replace_funct(self, expr):
        math_funct = {
            'cos': math.cos,
            'sin': math.sin,
            'tan': math.tan,
            'exp': math.exp,
            'abs': ft_abs,
            'sqrt': ft_sqrt,
        }
        name, param = extract_function(expr)
        if param is None:
            return expr
        funct = "{}({})".format(name, param)
        i = expr.find(funct)
        j = i + len(funct)
        if len(param) == 0:
            raise ValueError('function parameter not found.')
        param = str_to_value(param, self.data)
        if isinstance(param, str):
            param = calculator(param, self)
            param = str_to_value(param, self.data)
        if name in math_funct.keys() and isrealnumber(param):
            value = math_funct[name](param)
            expr = expr[:i] + str(value) + expr[j:]
        elif name == "abs" and isinstance(param, Complex):
            value = param.conjugate()
            expr = expr.replace(funct, str(value))
        elif name in self.data.keys():
            if (i == 0 or expr[i - 1] not in "%*/)") and \
                    (j == len(expr) or expr[j] not in "%*/)"):
                value = "{}".format(self.data[name].image(param))
            else:
                value = "({})".format(self.data[name].image(param))
            expr = expr[:i] + str(value) + expr[j:]
        elif name not in math_funct:
            raise ValueError("function '{}' undefined.".format(name))
        return self.replace_funct(expr)

    def put_mul(self, expr):
        expr = expr.replace(')(', ')*(')
        regex = r"(?P<x1>[\d\[\];,\.]+)(?P<x2>([A-Za-z]+|\(|\[))"
        match = re.search(regex, expr)
        if match is None:
            regex = r"(?P<x1>[A-Za-z]+|\)|\])(?P<x2>[\d\[\];,\.]+)"
            match = re.search(regex, expr)
            if match is None:
                return expr
        if match.group('x1')[-1] != '.':
            expr = expr.replace(match.group(), "{}*{}"
                                .format(match.group('x1'), match.group('x2')))
        elif match.group('x2') == 't':
            mat = str_to_matrix(match.group('x1')[:-1], self.data)
            if mat is None:
                raise ValueError("tranpose supported only by matrix")
            expr = expr.replace(match.group(), str(mat.T()))
        else:
            raise ValueError("syntax error")
        return self.put_mul(expr)

    def replace_var(self, expr):
        matches = re.finditer(r"[a-z]+", expr)
        new_expr = expr
        for elem in matches:
            var = elem.group()
            name = var
            if name in self.data.keys():
                value = self.data[name]
                if isinstance(value, Function) is False:
                    new_expr = new_expr[:elem.span()[0]] + "({})".format(str(value))\
                               + new_expr[elem.span()[1]:]
        return new_expr

    def calculate_pow(self, expr):
        regex = r"(?P<x1>[\d\.\[\];,]+|i)[\^](?P<x2>[-+]?[\d\.]+)"
        operation = re.search(regex, expr)
        new_expr = expr
        while operation is not None:
            x1 = str_to_value(operation.group('x1'), self.data)
            x2 = str_to_value(operation.group('x2'), self.data)
            start, end = operation.span()
            if start != 0 and new_expr[start - 1] == '^':
                x = do_operation(x1, x2, '*')
            else:
                x = do_operation(x1, x2, '^')
            if (isrealnumber(x) is False or x > 0) and \
                    (start == 0 or new_expr[start - 1] not in '*/%^'):
                new_expr = '{}+{}{}'.format(new_expr[:start], x,
                                            new_expr[end:])
            else:
                new_expr = '{}{}{}'.format(new_expr[:start], x, new_expr[end:])
            operation = re.search(regex, new_expr)
        return new_expr

    def put_pow(self, expr):
        regex = r"[\w\^\.]+([*][\w\^\.]+)+"
        matches = list(re.finditer(regex, expr))
        i = 0
        n = len(matches)
        while i < n:
            begin = 0
            if matches[i].span()[0] > 0 and \
                    expr[matches[i].span()[0] - 1] in "/^%":
                begin = matches[i].group().find('*') + 1
            tokens = matches[i].group()[begin:].split('*')
            new_expr = ""
            used = []
            for token in tokens:
                if token not in used:
                    count = tokens.count(token)
                    used.append(token)
                    if len(new_expr) != 0:
                        new_expr += '*'
                    if count > 1:
                        new_expr += "{}^{}".format(token, count)
                    else:
                        new_expr += token
            if new_expr != matches[i].group()[begin:]:
                expr = expr[:matches[i].span()[0] + begin] + \
                       new_expr + expr[matches[i].span()[1]:]
                matches = list(re.finditer(regex, expr))
                n = len(matches)
                i = -1
            i += 1
        return expr

    def do_division(self, expr):
        regex = [r"(?P<x1>[\d\.]+|i)\/(?P<x2>[-]?[\d\.]+|i)",
                 r"(?P<x1>[\d\.]+|i)\/\((?P<x2>[\w\.\+\-\*\%]+)\)",
                 r"\((?P<x1>[\w\.\+\-\*\%]+)\)\/\((?P<x2>[\w\.\+\-\*\%]+)\)"]
        for i in range(3):
            match = re.search(regex[i], expr)
            if match is not None:
                break
        if match is None:
            return expr
        x1 = rm_useless_brackets(match.group('x1'))
        x2 = rm_useless_brackets(match.group('x2'))
        x1 = str_to_value(x1, self.data)
        x2 = str_to_value(x2, self.data)
        if isnumber(x1) is False:
            x1 = str_to_value(match.group('x1'), self.data)
        if isnumber(x2) is False:
            x2 = str_to_value(match.group('x2'), self.data)
        result = do_operation(x1, x2, '/')
        if isinstance(result, str) or (match.span()[0] != 0 and
                                       expr[match.span()[0] - 1] == '/'):
            tmp = self.do_division(expr[match.span()[1]:])
            return expr[:match.span()[1]] + tmp
        return expr[:match.span()[0]] + str(result) + expr[match.span()[1]:]

    def do_multiplication(self, expr):
        regex = r"[\w\.]+([\*]\-?[\w\.]+)+"
        matches = re.finditer(regex, expr)
        for match in matches:
            if match.span()[0] != 0 and expr[match.span()[0] - 1] == '%':
                return expr
            tokens = match.group().split('*')
            result = str_to_value(tokens[0], self.data)
            for i in range(1, len(tokens)):
                x = str_to_value(tokens[i], self.data)
                result = do_operation(result, x, '*')
                if isinstance(result, str) and i != len(tokens) - 1:
                    x2 = str_to_value(tokens[i + 1], self.data)
                    if isinstance(x2, str):
                        raise ValueError('multiple unknowns not supported')
            tmp = expr
            expr = expr.replace(match.group(), str(result))
            if tmp != expr:
                break
        return expr

    def do_matrix_operation(self, expr):
        rg = [r"\[[\w\.\[\],;\-\+]+\](?P<op>[\*\/]{1,2})\[[\w\.\[\],;\-\+]+\]",
              r"\[[\w\.\[\],;\-\+]+\](?P<op>[\*\/]{1,2})\-?[\w\.]+",
              r"[\w\.]+(?P<op>[\*\/]{1,2})\[[\w\.\[\],;\-\+]+\]",
              r"\([\di\.\-\+\*]+\)(?P<op>[\*\/]{1,2})\[[\w\.\[\],;\-\+]+\]",
              r"\[[\w\.\[\],;\-\+]+\](?P<op>[\*\/]{1,2})\([\di\.\-\+\*]+\)"]
        for i in range(len(rg)):
            match = re.search(rg[i], expr)
            if match is not None:
                break
        if match is None:
            return expr
        op = match.group('op')
        tokens = match.group().split(op)
        if i == 3:
            tokens[0] = tokens[0][1:-1]
        elif i == 4:
            tokens[1] = tokens[1][1:-1]
        result = str_to_value(tokens[0], self.data)
        for i in range(1, len(tokens)):
            x = str_to_value(tokens[i], self.data)
            result = do_operation(result, x, op)
        expr = expr.replace(match.group(), str(result))
        return expr

    def do_modulo(self, expr):
        regex = r"[\w\.\[\],;]+([%][\w\.\[\],;]+)+"
        match = re.search(regex, expr)
        if match is None:
            return expr
        tokens = match.group().split('%')
        x1 = str_to_value(tokens[0], self.data)
        x2 = str_to_value(tokens[1], self.data)
        result = do_operation(x1, x2, '%')
        return expr.replace(match.group(), str(result))

    def reduce(self, expr):
        new_expr = self.do_division(expr).replace('--', '+')
        new_expr = self.do_multiplication(new_expr).replace('--', '+')
        new_expr = self.do_matrix_operation(new_expr).replace('--', '+')
        new_expr = self.do_modulo(new_expr).replace('--', '+')
        if new_expr[0] == "+":
            new_expr = new_expr[1:]
        if new_expr == expr:
            return new_expr
        return self.reduce(new_expr)
