import re
from utils import rm_useless_brackets


def get_factored_expr(expr):
    begin = expr.rfind('(')
    stop = 1
    if begin == -1:
        return None, None
    match = expr[begin:]
    end = match.find(')')
    if end == -1:
        raise ValueError("')' is missing")
    end += begin + 1
    if begin > 0 and expr[begin - 1] in '*/^':
        x2 = expr[begin + 1:end - 1]
        op = expr[begin - 1]
        for i in range(begin - 2, 0, -1):
            if expr[i] == ')':
                stop = 0
            if expr[i] == '(':
                stop = 1
            if expr[i] in "+-)(" and stop:
                if expr[i] == '(':
                    x1 = expr[i:begin - 1]
                else:
                    x1 = expr[i:begin - 2]
                return expr[i:end], [x1, op, x2]
        return expr[:end], [expr[:begin - 1], op, x2]
    elif end < len(expr) and expr[end] in '*/^':
        x1 = expr[begin + 1:end - 1]
        op = expr[end]
        for i in range(end + 1, len(expr)):
            if expr[i] in "+-)(":
                x2 = expr[end + 1:i]
                return expr[begin:i], [x1, op, x2]
        return expr[begin:], [x1, op, expr[end + 1:]]
    return expr[begin:end], [expr[begin + 1:end - 1], '*', '1']


def power_to_mul(expr, power):
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
    match = re.search(r"[^\+\*\/\%]+\-", expr)
    if match is None:
        return expr
    new_expr = match.group()[:-1] + '+-'
    expr = expr.replace(match.group(), new_expr)
    return add_plus(expr)


def decompose(expr):
    expr = expr.replace(' ', '')
    expr = rm_useless_brackets(expr)
    match, tokens = get_factored_expr(expr)
    if match is None:
        return expr
    new_expr = ""
    op = tokens[1]
    tokens = [tokens[0], tokens[2]]
    for i in range(2):
        if tokens[i] == '1':
            expr = expr.replace(match, tokens[1 - i])
            return decompose(expr)
    if op == '^':
        new_expr = power_to_mul(tokens[0], tokens[1])
        expr = expr.replace(match, new_expr)
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
                new_expr += tokens[i - 1][j] + op + tokens[i][k]
    # print(expr)
    expr = expr.replace(match, '({})'.format(new_expr))
    # print(expr)
    return decompose(expr)
