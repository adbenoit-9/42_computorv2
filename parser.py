from function import Function


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
        self.tokens = None
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
        self.tokens = self.translate(expr)
        if expr_type in type_list[:3]:
            return Function(self.tokens, self.data, param)
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

    def translate(self, expr):
        new_expr = ""
        tokens = self.split(expr, '+-')
        for token in tokens:
            sign = 1
            tmp = 0
            x = ""
            op = ""
            for i, c in enumerate(token):
                if c == '-':
                    sign *= -1
                elif c == '+':
                    continue
                elif c in "*/%^":
                    if len(x):
                        x = self.get_value(x)
                        if isinstance(x, str) is False:
                            x *= sign
                        elif sign == -1:
                            x = '- ' + x
                        elif len(new_expr) != 0:
                            x = '+ ' + x
                        sign = 1
                        if len(op):
                            val = self.do_operation(val, x, op)
                        else:
                            val = x
                        x = ""
                        op = c
                    else:
                        op += c
                else:
                    x += c
            x = self.get_value(x)
            if isinstance(x, str) is False:
                x *= sign
            elif sign == -1:
                x = '- ' + x
            elif len(new_expr) != 0:
                x = '+ ' + x
            if len(op):
                val = self.do_operation(val, x, op)
            else:
                val = x
            new_expr += self.format_val(val, len(new_expr))
        return new_expr

    def calculate(self):
        expr = self.tokens.replace(' ', '')
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
        if isinstance(x1, str) and op == "^":
            i = 0
            sign = ''
            if x1[0] in '+-':
                i = 2
                sign = x1[:2]
            return "{}{}^{}".format(sign, x1[i:], x2)
        if isinstance(x1, str):
            i = 0
            sign = ''
            if x1[0] in '+-':
                i = 2
                sign = x1[:2]
            return "{}{} {} {}".format(sign, abs(x2), op, x1[i:])
        elif isinstance(x2, str):
            i = 0
            sign = ''
            if x2[0] in '+-':
                i = 2
                sign = x2[:2]
            return "{}{} {} {}".format(sign, abs(x1), op, x2[i:])
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
