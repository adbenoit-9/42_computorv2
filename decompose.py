import re
from utils import rm_brackets


def get_factored_expr(expr):
    '''Extract a factored expression.'''
    regex = [r"(?P<x1>\-?[\w\.\/\%]+)\*\((?P<x2>[\w\.\+\-\*\/]+)\)",
             r"\((?P<x1>[\w\.\+\-\*\/]+)\)\*(?P<x2>[\w\.]+)",
             r"\((?P<x1>[\w\.\+\-\*\/]+)\)\*(?P<x2>\([\w\.\+\-\*\/]+\))",
             r"\((?P<x1>[\w\.\+\-\*\/]+)\)\/(?P<x2>[\w\.]+)"]
    for i in range(4):
        match = re.search(regex[i], expr)
        if match is None:
            continue
        if i == 3:
            return match.group(), [match.group('x1'), '/', match.group('x2')]
        return match.group(), [match.group('x1'), '*', match.group('x2')]
    return None, []


def power_to_mul(expr, power):
    '''Decompose power to multiplications'''
    new_expr = ""
    try:
        power = int(power)
        for i in range(power):
            if i != 0:
                new_expr += '*'
            new_expr += "({})".format(expr)
        return new_expr
    except Exception:
        raise ValueError('non-decomposable expression')


def add_plus(expr):
    '''add operator + in front of operator -'''
    match = re.search(r"[^\+\*\/\%]+\-", expr)
    if match is None:
        return expr
    new_expr = match.group()[:-1] + '+-'
    expr = expr.replace(match.group(), new_expr)
    return add_plus(expr)


def op_to_str(x1, x2, op):
    '''Convert an operation to a string.'''
    if x2 == "1":
        return x1
    if x1 == "0":
        return "0"
    elif op == '*':
        if x2 == "0":
            return "0"
        if x1 == "1":
            return x2
    return x1 + op + x2


def decompose(expr):
    '''Decompose an expression.'''
    expr = expr.replace(' ', '')
    expr = rm_brackets(expr)
    re_pow = r"\((?P<x>[\w\.\+\-\*\/]+)\)[\^](?P<pow>[\d\.]+)"
    matches = re.finditer(re_pow, expr)
    for match in matches:
        new_expr = power_to_mul(match.group('x'), match.group('pow'))
        expr = expr.replace(match.group(), '({})'.format(new_expr))
    match, tokens = get_factored_expr(expr)
    if match is None:
        return expr
    new_expr = ""
    op = tokens[1]
    tokens = [tokens[0], tokens[2]]
    for i in range(2):
        if tokens[i] == '1':
            expr = expr.replace(match, '({})'.format(tokens[1 - i]))
            return decompose(expr)
    for i in range(len(tokens)):
        if '(' not in tokens[i]:
            tokens[i] = add_plus(tokens[i])
            tokens[i] = tokens[i].split('+')
        else:
            tokens[i] = [tokens[i]]
    for i in range(1, len(tokens)):
        for j in range(len(tokens[i - 1])):
            for k in range(len(tokens[i])):
                if len(new_expr):
                    new_expr += '+'
                new_expr += op_to_str(tokens[i - 1][j], tokens[i][k], op)
    expr = expr.replace(match, '({})'.format(new_expr))
    return decompose(expr)
