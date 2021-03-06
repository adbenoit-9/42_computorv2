import re
import math
from ft_math import ft_abs, ft_sqrt
from ft_function import Function
from ft_matrix import Matrix
from ft_real import Real
from ft_complex import isrealnumber
from conversion import str_to_complex, str_to_matrix, str_to_value
from utils import check_brackets, get_variables, isnumber, \
                  rm_brackets, put_space, extract_function, ismatrix
from calculator import calculator, do_operation


class Parser:
    '''Parse a mathematic expression.'''

    ##################################################
    #  Part1: parse the syntax of the command line  #
    ##################################################

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
        if self.check_space(tokens) is False:
            raise ValueError('syntax error')
        cmd = cmd.replace(' ', '')
        re_abs = r"\|.+\|"
        match = re.search(re_abs, cmd)
        while match is not None:
            cmd = cmd.replace(match.group(),
                              "abs({})".format(match.group()[1:-1]))
            match = re.search(re_abs, cmd)
        if self.command_syntax(cmd) is False:
            raise ValueError('syntax error')
        self.cmd = cmd.lower().split('=')
        if len(self.cmd) != 2 or len(self.cmd[1]) == 0 or \
                len(self.cmd[0]) == 0:
            raise ValueError('syntax error')
        for i in range(len(self.cmd)):
            if self.cmd[i][-1] in "*/+-%^":
                raise ValueError('syntax error')
            if '?' in self.cmd[i]:
                if i == 0 or '?' in self.cmd[i][:-1]:
                    raise ValueError('syntax error')

    def command_syntax(self, cmd):
        if re.search(r"\(\)", cmd) or re.search(r"[\^\/\%]{2}", cmd) or \
                re.search(r"(\*[\/%])|([\/%]\*)|\*{3}", cmd) or \
                re.search(r"(\([\*\/%\^])|([\^\*\/%\+\-]\))", cmd):
            return False
        re_illegal_char = r"[^\w\_\+\-\*\/\(\)\[\];,\.\%\^=\?]"
        match = re.search(re_illegal_char, cmd)
        if match:
            raise ValueError('illegal character: {}'.format(match.group()))
        re_point = r"[\*\/\%\^\+\-=\.\(\[;,]\."
        if re.search(re_point, cmd):
            return False
        if self.matrix_syntax(cmd) is False:
            return False
        if check_brackets(cmd) is False:
            return False
        return self.brackets_syntax(cmd)

    def matrix_syntax(self, cmd):
        re_semicolon = r"\[\[.*\](;\[.*\])+\]"
        re_coma = r"\[\[[^\[\]]*(,[^\[\]]*)+\]"
        if (cmd.find(';') != -1 and re.search(re_semicolon, cmd) is None) or \
                (cmd.find(',') != -1 and re.search(re_coma, cmd) is None):
            return False
        re_matrix = r"\[(((\[[^\[\]]*\])?(;\[[^\[\]]*\])*)|([\w\+\-\*\/\%\(\)]+))\]"
        matches = re.finditer(re_matrix, cmd)
        for match in matches:
            if ismatrix(match.group()) is False:
                return False
        return True

    def brackets_syntax(self, expr):
        matches = list(re.finditer(r"(\([^\(\)\[\]]*\))|(\[[^\(\)\[\]]*\])",
                       expr))
        if re.search(r"[\(\)\[\]]", expr) and len(matches) == 0:
            return False
        for match in matches:
            if re.search(r"[\(\)\[\]]", match.group()):
                if self.brackets_syntax(expr.replace(match.group(),
                                        match.group()[1:-1])) is False:
                    return False
        return True

    def check_space(self, tokens):
        space = True
        for token in tokens:
            if space is False and token[0] not in "[]()-+/*=%^,;?":
                return False
            elif token[-1] in "[]()-+/*=%^,;":
                space = True
            else:
                space = False
        return True

    #################################################
    #    Part2: parse and compute the expression    #
    #################################################

    def start(self, expr):
        '''Reduce the expression until it becomes a sum.'''
        if isinstance(expr, str) is False:
            raise ValueError('Parser: invalid argument')
        expr = expr.replace(' ', '')
        expr = self.standardize_mul(expr)
        expr = self.put_variables(expr)
        expr = self.put_functions(expr)
        expr = self.factor_power(expr)
        expr = self.compute_power(expr)
        expr = rm_brackets(expr)
        expr = self.reduce(expr)
        return expr

    def put_functions(self, expr):
        '''Replaces functions with their value'''
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
        if name in math_funct.keys() and isinstance(param, str) is False:
            try:
                if name not in ['sqrt', 'abs'] and isinstance(param, Real):
                    value = math_funct[name](param.value)
                else:
                    value = math_funct[name](param)
                if name not in ['sqrt', 'abs']:
                    value = Real(value)
                expr = expr[:i] + str(value) + expr[j:]
            except TypeError as err:
                raise ValueError(err)
        elif name in self.data.keys():
            if (i == 0 or expr[i - 1] not in "%*/)") and \
                    (j == len(expr) or expr[j] not in "%*/)"):
                value = "{}".format(self.data[name].image(param))
            else:
                value = "({})".format(self.data[name].image(param))
            expr = expr[:i] + str(value) + expr[j:]
        elif name not in math_funct:
            raise ValueError("function '{}' undefined.".format(name))
        return self.put_functions(expr)

    def put_variables(self, expr):
        '''Replaces variables with their value'''
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

    def standardize_mul(self, expr):
        '''Add operator * where the product is implicit'''
        expr = expr.replace(')(', ')*(')
        expr = expr.replace('-(', '-1*(')
        regex = [r"(?P<x1>\d+\.?\d*)(?P<x2>([a-su-z]|[a-z]{2,}|\[))",
                 r"(?P<x1>[a-z]|\])(?P<x2>\d+\.?\d*)",
                 r"(?P<x1>(\d+\.?\d*)|\])(?P<x2>\()",
                 r"(?P<x1>\))(?P<x2>(\d+\.?\d*)|[a-z]+|\[)"]
        match = None
        for i in range(len(regex)):
            match = re.search(regex[i], expr)
            if match:
                break
        if match is None:
            return expr
        expr = expr.replace(match.group(), "{}*{}"
                            .format(match.group('x1'), match.group('x2')))
        return self.standardize_mul(expr)

    def factor_power(self, expr):
        '''Factors expression: multiplication to power'''
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

    def compute_power(self, expr):
        '''Calculates the powers of the expression'''
        re_pow = r"(?P<x1>[\d\.\[\];,]+|i|(\([\d\.]*[\+\-]?[\d\.]*\*?i\)))[\^](?P<x2>[-+]?[\d\.]+)"
        operation = re.search(re_pow, expr)
        new_expr = expr
        while operation is not None:
            if operation.group('x1')[0] == '(':
                x1 = str_to_value(operation.group('x1')[1:-1], self.data)
            else:
                x1 = str_to_value(operation.group('x1'), self.data)
            x2 = str_to_value(operation.group('x2'), self.data)
            start, end = operation.span()
            x = do_operation(x1, x2, '^')
            if (isrealnumber(x) is False or x > 0) and \
                    (start == 0 or new_expr[start - 1] not in '*/%-^+('):
                new_expr = '{}+{}{}'.format(new_expr[:start], x,
                                            new_expr[end:])
            else:
                new_expr = '{}{}{}'.format(new_expr[:start], x, new_expr[end:])
            operation = re.search(re_pow, new_expr)
        return new_expr.replace('-+', '-').replace('+-', '-')

    def compute_division(self, expr):
        '''Calculates one division of the expression'''
        re_div = [r"(?P<x1>[\d\.]+|i|[a-z]+|(\([\d\.]*[\+\-]?[\d\.]*\*?i\)))\/(?P<x2>[-]?[\d\.]+|i|(\([\d\.]*[\+\-]?[\d\.]*\*?i\)))",
                  r"(?P<x1>[\d\.]+|i|[a-z]+)\/\((?P<x2>[\w\.\+\-\*\%]+)\)",
                  r"\((?P<x1>[\w\.\+\-\*\%]+)\)\/\((?P<x2>[\w\.\+\-\*\%]+)\)"]
        for i in range(3):
            match = re.search(re_div[i], expr)
            if match is not None:
                break
        if match is None:
            return expr
        x1 = rm_brackets(match.group('x1'))
        x2 = rm_brackets(match.group('x2'))
        x1 = str_to_value(x1, self.data)
        x2 = str_to_value(x2, self.data)
        if isnumber(x1) is False:
            x1 = str_to_value(match.group('x1'), self.data)
        if isnumber(x2) is False:
            x2 = str_to_value(match.group('x2'), self.data)
        result = do_operation(x1, x2, '/')
        if isinstance(result, str) or (match.span()[0] != 0 and
                                       expr[match.span()[0] - 1] in '/^'):
            if isinstance(result, str) and match.span()[0] != 0 and \
                    expr[match.span()[0] - 1] == '*':
                return expr[:match.span()[0] - 1] + '/' + str(x2) + '*' + \
                       str(x1) + expr[match.span()[1]:]
            tmp = self.compute_division(expr[match.span()[1]:])
            return expr[:match.span()[1]] + tmp
        if isrealnumber(result):
            return expr[:match.span()[0]] + str(result) + \
                   expr[match.span()[1]:]
        return expr[:match.span()[0]] + str(result) + expr[match.span()[1]:]

    def compute_multiplication(self, expr):
        '''Calculates one multiplication of the expression'''
        re_mul = r"[\w\.]+([\*]{1,2}\-?[\w\.]+)+"
        matches = re.finditer(re_mul, expr)
        for match in matches:
            if re.search(r'\*{2}', match.group()):
                raise ValueError("operator '**' supported only between matrices")
            if match.span()[0] != 0 and expr[match.span()[0] - 1] in '%/':
                return expr.replace('--', '+')
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
                        raise ValueError('multiple variables not supported')
            tmp = expr
            expr = expr.replace(match.group(), str(result))
            if tmp != expr:
                break
        return expr.replace('--', '+')

    def compute_modulo(self, expr):
        '''Calculates one modulo of the expression'''
        re_mod = r"[\w\.\[\],;]+(%[+-]?[\w\.\[\],;]+)+"
        match = re.search(re_mod, expr)
        if match is None:
            if re.search(r"\([\d\.\+\-\/\*]*i[\d\.\+\-\/\*]*\)%", expr) or \
                    re.search(r"%\([\d\.\+\-\/\*]*i[\d\.\+\-\/\*]*\)", expr):
                raise ValueError("operator '%' not supported on 'Complex'")
            return expr
        tokens = match.group().split('%')
        x1 = str_to_value(tokens[0], self.data)
        x2 = str_to_value(tokens[1], self.data)
        result = do_operation(x1, x2, '%')
        if isrealnumber(result):
            return expr.replace(match.group(), str(result))
        return expr.replace(match.group(), str(result))

    def join_tokens(self, tokens, op, start, end):
        '''join tokens with the operator op from start to end'''
        new_tokens = []
        joined = ""
        for i in range(start):
            new_tokens.append(tokens[i])
        for i in range(start, end):
            if i != start:
                joined += op
            joined += tokens[i]
        if len(joined):
            new_tokens.append(joined)
        for i in range(end, len(tokens)):
            new_tokens.append(tokens[i])
        return new_tokens

    def do_matrix_operation(self, expr):
        '''Calculates one matrix operation of the expression'''
        re_row = r"\[[\d\.i\+\-\*\/\%]+(,[\d\.i\+\-\*\/\%]+)*\]"
        re_mat = r"\[" + re_row + r"(;" + re_row + r")*\]"
        if re.search(r"\([\d\.\+\-\/\*]*i[\d\.\+\-\/\*]*\)\*{2}", expr) or \
                re.search(r"\*{2}\([\d\.\+\-\/\*]*i[\d\.\+\-\/\*]*\)", expr):
            raise ValueError("operator '**' not supported on 'Complex'")
        re_op = [re_mat + r"(?P<op>[\*\/]{1,2})" + re_mat,
                 re_mat + r"(?P<op>[\*\/]{1,2})\-?[\w\.]+",
                 r"[\w\.]+(?P<op>[\*\/]{1,2})" + re_mat,
                 re_mat + r"(?P<op>\.[a-z]+)",
                 r"\([\di\.\-\+\*]+\)(?P<op>[\*\/]{1,2})" + re_mat,
                 re_mat + r"(?P<op>[\*\/]{1,2})\([\di\.\-\+\*]+\)"]
        for i in range(len(re_op)):
            match = re.search(re_op[i], expr)
            if match is not None:
                break
        if match is None:
            return expr
        op = match.group('op')
        tokens = match.group().split(op)
        for j in range(1, len(tokens)):
            if tokens[j].startswith('(') or tokens[j].startswith('[['):
                break
        tokens = self.join_tokens(tokens, '*', j, len(tokens))
        tokens = self.join_tokens(tokens, '*', 0, j)
        if i == 4:
            tokens[0] = tokens[0][1:-1]
        elif i == 5:
            tokens[1] = tokens[1][1:-1]
        result = str_to_value(tokens[0], self.data)
        if op == '.t':
            if isinstance(result, Matrix):
                result = result.T()
            else:
                raise ValueError('transpose supported only by matrices', result, op)
        elif op.startswith('.'):
            raise ValueError('syntax error')
        else:
            for i in range(1, len(tokens)):
                x = str_to_value(tokens[i], self.data)
                result = do_operation(result, x, op)
        expr = expr.replace(match.group(), str(result))
        return expr

    def reduce(self, expr):
        '''Do all operations except the sum'''
        new_expr = self.factor_power(expr)
        new_expr = self.compute_division(new_expr).replace('--', '+')
        new_expr = self.compute_multiplication(new_expr)
        new_expr = self.do_matrix_operation(new_expr)
        new_expr = self.compute_modulo(new_expr)
        if re.search(r"((\(?[\d\.]+i?\)?)|[^a-z]i)\.t", new_expr) or \
                new_expr.startswith('i.t'):
            raise ValueError('transpose supported only by matrices')
        if len(new_expr) and new_expr[0] == "+":
            new_expr = new_expr[1:]
        if new_expr == expr:
            return new_expr
        return self.reduce(new_expr)

    #################################################
    #       Part3: parse and format the result      #
    #################################################

    def end(self, result):
        '''Parse and format the result'''
        result = str(result)
        if result[-1] in "*/+-%^":
            raise ValueError('syntax error')
        matches = re.finditer(r"[a-z]+", result)
        if len(get_variables(result)) > 1:
            raise ValueError('multiple variables not supported')
        tmp = str_to_matrix(result, self.data)
        if tmp is not None:
            return repr(tmp)
        tmp = str_to_complex(result)
        if tmp is not None:
            result = repr(tmp)
        result = result.replace(' ', '')
        matches = re.finditer(r"(?P<x>[\d\.]+)\*i", result)
        i = 0
        for match in matches:
            result = result[:match.span()[0] - i] + match.group('x') + \
                     'i' + result[match.span()[1] - i:]
            i += 1
        name, param = extract_function(result, "abs")
        while param is not None:
            result = result.replace("abs({})".format(param),
                                    "|{}|".format(param))
            name, param = extract_function(result, "abs")
        return put_space(result)
