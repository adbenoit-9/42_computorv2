import re
from ft_matrix import Matrix
from decompose import decompose
from utils import isrealnumber


def do_operation(x1, x2, op):
    if isinstance(x1, str):
        if isinstance(x2, int) and x2 == 0 and op in '*/':
            return 0
        if op == "*":
            return "{}{}{}".format(x2, op, x1)
        return "{}{}{}".format(x1, op, x2)
    if isinstance(x2, str):
        if isinstance(x1, int) and x1 == 0 and op in '*/':
            return 0
        return "{}{}{}".format(x1, op, x2)
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


def split_operation(expr):
    matches = re.finditer(r"[+-]", expr)
    tokens = []
    tmp = 0
    for elem in matches:
        begin, end = elem.span()
        if begin != 0 and expr[begin - 1] not in "*/%^":
            if begin != 0:
                tokens.append(expr[tmp:begin])
            tokens.append(elem.group())
            tmp = end
    tokens.append(expr[tmp:])
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()
    return tokens


def calculator(expr, parser):
    expr = parser.start(expr)
    if re.search(r"[^\di\+\-\*\/\%\^\[\]\.;,\(\)]+", expr) is None:
        expr = decompose(expr)
        expr = parser.start(expr)
        expr = parser.start(expr) # pk il faut mettre une deuxieme fois ? (3 + 8i) * 2
    tokens = split_operation(expr)
    result = 0
    value = 0
    op = None
    tmp = []
    for token in tokens:
        if token in '-+':
            op = token
            continue
        value = parser.str_to_value(token)
        if isinstance(value, str):
            if op is not None:
                tmp.append(op + value)
            else:
                tmp.append('+' + value)
        elif op is not None:
            result = do_operation(result, value, op)
        else:
            result = value
    if op is None:
        return expr
    expr = ""
    for val in tmp:
        expr += val
    if len(expr) == 0 or isrealnumber(result) is False or result != 0:
        result = str(result)
        if result[0] != '-':
            expr += '+'
        expr += result
    if expr[0] == "+":
        return expr[1:]
    return expr
