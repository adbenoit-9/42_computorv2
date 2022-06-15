from ft_math import ft_abs, ft_sqrt
from function import Function
from ft_matrix import Matrix
from ft_complex import Complex, isrealnumber
from conversion import str_to_matrix, str_to_value
from utils import check_brackets, isnumber, rm_useless_brackets, \
                  put_space, extract_function
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
        if re.search(r"\(\)", cmd) or re.search(r"[\/\%]{2}", cmd) or \
                re.search(r"(\*[\/%])|([\/%]\*)|\*{3}", cmd):
            raise ValueError('syntax error')
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
        if match:
            raise ValueError('illegal character: {}'.format(match.group()))
        regex = r"[\*\/\%\^\+\-=\.\(\)\[;,]\."
        if re.search(regex, cmd):
            raise ValueError('syntax error')
        regex1 = r"\[\[.*\](;\[.*\])+\]"
        regex2 = r"\[.*(,.*)+\]"
        if (cmd.find(';') != -1 and re.search(regex1, cmd) is None) or \
                (cmd.find(',') != -1 and re.search(regex2, cmd) is None):
            raise ValueError('syntax error')
        i = cmd.count('(') - cmd.count(')')
        j = cmd.count('[') - cmd.count(']')
        if check_brackets(cmd) is False:
            raise ValueError('syntax error')
        self.cmd = cmd.lower().split('=')
        if len(self.cmd) != 2 or len(self.cmd[1]) == 0 or \
                len(self.cmd[0]) == 0:
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
        expr = expr.replace('+-', '-')
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
        expr = expr.replace('-(', '-1*(')
        regex = [r"(?P<x1>[\d\.]+)(?P<x2>([a-su-z]|[a-z]{2,}))",
                 r"(?P<x1>[a-z])(?P<x2>[\d\.]+)",
                 r"(?P<x1>[\d\.]+)(?P<x2>\()",
                 r"(?P<x1>\))(?P<x2>[\d\.]+)"]
        match = None
        for i in range(len(regex)):
            match = re.search(regex[i], expr)
            if match:
                break
        if match is None:
            return expr
        expr = expr.replace(match.group(), "{}*{}"
                            .format(match.group('x1'), match.group('x2')))
        return self.put_mul(expr)

    def replace_var(self, expr):
        matches = re.finditer(r"[a-z]+", expr)
        new_expr = expr
        i = 0
        for elem in matches:
            var = elem.group()
            name = var
            if name in self.data.keys():
                value = self.data[name]
                if isinstance(value, Function) is False:
                    new_expr = new_expr[:elem.span()[0] + i] + \
                               "({})".format(str(value)) + \
                               new_expr[elem.span()[1] + i:]
                    i += len(str(value)) + 2 - len(elem.group())
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
                    (start == 0 or new_expr[start - 1] not in '*/%^-+'):
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
        if isrealnumber(result):
            return expr[:match.span()[0]] + '{:f}'.format(result) + \
                   expr[match.span()[1]:]
        return expr[:match.span()[0]] + str(result) + expr[match.span()[1]:]

    def do_multiplication(self, expr):
        regex = r"[\w\.]+([\*]{1,2}\-?[\w\.]+)+"
        matches = re.finditer(regex, expr)
        for match in matches:
            if re.search(r'\*{2}', match.group()):
                raise ValueError("operator '**' supported only between matrices")
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
                        if x2 in '.;,':
                            raise ValueError('syntax error')
                        raise ValueError('multiple unknowns not supported')
            tmp = expr
            if isrealnumber(result):
                expr = expr.replace(match.group(), '{:f}'.format(result))
            else:
                expr = expr.replace(match.group(), str(result))
            if tmp != expr:
                break
        return expr

    def do_matrix_operation(self, expr):
        rg = [r"\[[\w\.\[\],;\-\+]+\](?P<op>[\*\/]{1,2})\[[\w\.\[\],;\-\+]+\]",
              r"\[[\w\.\[\],;\-\+]+\](?P<op>[\*\/]{1,2})\-?[\w\.]+",
              r"[\w\.]+(?P<op>[\*\/]{1,2})\[[\w\.\[\],;\-\+]+\]",
              r"\[[\w\.\[\],;\-\+]+\](?P<op>\.t)",
              r"\(\[[\w\.\[\],;\-\+]+\]\)(?P<op>\.t)",
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
        if i == 4 or i == 5:
            tokens[0] = tokens[0][1:-1]
        elif i == 6:
            tokens[1] = tokens[1][1:-1]
        result = str_to_value(tokens[0], self.data)
        if op == '.t':
            if isinstance(result, Matrix):
                result = result.T()
            else:
                raise ValueError('transpose supported only by matrices')
        else:
            for i in range(1, len(tokens)):
                x = str_to_value(tokens[i], self.data)
                result = do_operation(result, x, op)
        expr = expr.replace(match.group(), str(result))
        return expr

    def do_modulo(self, expr):
        regex = r"[\w\.\[\],;]+(%[+-]?[\w\.\[\],;]+)+"
        match = re.search(regex, expr)
        if match is None:
            return expr
        tokens = match.group().split('%')
        x1 = str_to_value(tokens[0], self.data)
        x2 = str_to_value(tokens[1], self.data)
        result = do_operation(x1, x2, '%')
        if isrealnumber(result):
            return expr.replace(match.group(), '{:f}'.format(result))
        return expr.replace(match.group(), str(result))

    def reduce(self, expr):
        new_expr = self.do_division(expr).replace('--', '+')
        new_expr = self.do_multiplication(new_expr).replace('--', '+')
        new_expr = self.do_matrix_operation(new_expr)
        new_expr = self.do_modulo(new_expr)
        if re.search(r"(([\d\.]+i?)|[^a-z]i)\.t", new_expr) or \
                new_expr.startswith('i.t'):
            raise ValueError('transpose supported only by matrices')
        if new_expr[0] == "+":
            new_expr = new_expr[1:]
        if new_expr == expr:
            return new_expr
        return self.reduce(new_expr)
