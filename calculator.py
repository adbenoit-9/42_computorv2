import re
from ft_matrix import Matrix
from decompose import decompose


def do_operation(x1, x2, op):
    if isinstance(x2, str):
        return "{}{}{}".format(x1, op, x2)
    elif isinstance(x1, str):

        return "{}{}{}".format(x2, op, x1)
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
    matches = re.finditer(r"[^\w\^\.\(\)\[\],;]+", expr)
    tokens = []
    tmp = 0
    for elem in matches:
        begin, end = elem.span()
        tokens.append(expr[tmp:begin])
        tokens.append(elem.group())
        tmp = end
    tokens.append(expr[tmp:])
    for i in range(len(tokens)):
        tokens[i] = tokens[i].strip()
    return tokens


def calculator(expr, parser):
    expr = decompose(expr)
    tokens = split_operation(expr)
    result = 0
    value = 0
    op = None
    for token in tokens:
        if token in '-+':
            op = token
            continue
        if token in '*/%':
            return expr
        value = parser.str_to_value(token)
        if op is not None:
            result = do_operation(result, value, op)
        else:
            result = value
    if op is None:
        return expr
    return result
