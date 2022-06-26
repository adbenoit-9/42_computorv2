import re
from ft_complex import Complex
from ft_matrix import Matrix
from decompose import decompose
from utils import isrealnumber, get_unknown_var
from ft_math import ft_abs
from conversion import str_to_value


def do_operation(x1, x2, op):
    not_var = ['tan', 'abs', 'sin', 'cos', 'exp', 'i', 't', 'sqrt']
    if isinstance(x1, str) and isinstance(x2, str) and x1 != x2 and \
            x1.isalpha() and x2.isalpha() and \
            x1 not in not_var and x2 not in not_var:
        raise ValueError('multiple variables not supported')
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
    try:
        if op == '+':
            result = x1 + x2
        elif op == '-':
            result = x1 - x2
        elif op == '*':
            if isinstance(x2, Matrix):
                result = x2 * x1
            else:
                result = x1 * x2
        elif op == '/':
            result = x1 / x2
        elif op == '%':
            result = ft_abs(x1) % ft_abs(x2)
            result = -result if x1 < 0 else result
        elif op == '^':
            result = x1 ** x2
        elif op == '**':
            if isinstance(x1, Matrix) is False:
                raise TypeError("Matrix product with '{}' not supported"
                                .format(type(x1).__name__))
            result = x1.dot(x2)
        else:
            raise ValueError("operator '{}' not supported.".format(op))
    except TypeError:
        raise ValueError("operator '{}' not supported between '{}' and '{}'."
                         .format(op, type(x1).__name__, type(x2).__name__))
    if isinstance(result, Complex) and result.im == 0:
        result = result.real
    if isinstance(result, float):
        result = round(result, 4)
    return result


def split_operation(expr):
    matches = re.finditer(r"[+-]", expr)
    tokens = []
    tmp = 0
    for elem in matches:
        begin, end = elem.span()
        if begin != 0 and expr[begin - 1] not in "*/%^[":
            if begin != 0:
                tokens.append(expr[tmp:begin])
            tokens.append(elem.group())
            tmp = end
    tokens.append(expr[tmp:])
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()
    return tokens


def do_sum(expr):
    tokens = split_operation(expr)
    result = 0
    value = 0
    op = None
    tmp = []
    for token in tokens:
        if token in '-+':
            op = token
            continue
        value = str_to_value(token, {})
        if isinstance(value, str):
            if op is not None:
                tmp.append(op + value)
            else:
                tmp.append('+' + value)
        elif op is not None:
            result = do_operation(result, value, op)
        else:
            result = value
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


def calculator(expr, parser, option=0):
    expr = parser.start(expr)
    tmp = expr
    match = re.search(r"\([^\(\)]+\)", expr)
    if len(get_unknown_var(expr)) == 0:
        option = 0
    while match is not None:
        new_expr = do_sum(match.group()[1:-1])
        expr = expr.replace(match.group(), "({})".format(new_expr))
        expr = parser.start(expr)
        if tmp == expr:
            if option == 0:
                tmp = expr
                expr = decompose(expr)
                if tmp == expr:
                    break
            break
        tmp = expr
        match = re.search(r"\([^\(\)]+\)", expr)
    expr = parser.start(expr)
    return do_sum(expr)
