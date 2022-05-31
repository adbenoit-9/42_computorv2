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

    def start(self, expr, expr_type, param='x'):
        type_list = ['function', 'f', 'funct', 'variable', 'var', 'v']
        if isinstance(expr, str) is False or \
                isinstance(expr_type, str) is False or \
                expr_type not in type_list:
            raise ValueError('Parser: invalid argument')
        self.state = self.BEGIN
        self.type = expr_type
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
        sign = 1
        tmp = 0
        x = ""
        op = ""
        for i, c in enumerate(expr):
            if c == '-':
                sign *= -1
                val = self.get_value(x)
                x = ""
                new_expr += self.format_val(val, len(new_expr))
            elif c == '+':
                val = self.get_value(x)
                x = ""
                new_expr += self.format_val(val, len(new_expr))
            elif c in "*/%^":
                if len(x):
                    x = self.get_value(x) * sign
                    sign = 1
                    if len(op):
                        val = self.do_operation(tmp, x, op)
                    else:
                        tmp = x
                    x = ""
                    op = c
                else:
                    op += c
            elif c != '+':
                x += c
        x = self.get_value(x) * sign
        if len(op):
            val = self.do_operation(tmp, x, op)
        else:
            val = x
        new_expr += self.format_val(val, len(new_expr))
        print(new_expr)
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
        if x in self.data.keys():
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

    def do_operation(self, x1, x2, op, len):
            
        if isinstance(x1, str):
            if len > 0 and :
            return "{} {} {}".format(abs(x2), op, x1)
        elif isinstance(x2, str):
            return "{} {} {}".format(abs(x1), op, x2)
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
        print('operation : {} {} {} = {}'.format(x1, op, x2, result))
        return result
