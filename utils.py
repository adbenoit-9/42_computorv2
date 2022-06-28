from ft_complex import Complex
from ft_real import Real
import re


def ismatrix(mat):
    if isinstance(mat, str) is False:
        raise ValueError("ismatrix: type '{}' not supported"
                         .format(type(mat).__name__))
    if len(mat) < 2:
        return False
    if mat[0] != '[' or mat[-1] != ']':
        return False
    rows = mat[1:-1].split(';')
    for i, row in enumerate(rows):
        if len(row) < 2:
            return False
        if row[0] != '[' or row[-1] != ']':
            return False
        if '[' in row[1:-1] or ']' in row[1:-1]:
            return False
    return True


def isrealnumber(n):
    if isinstance(n, Real):
        return True
    elif isinstance(n, float) or isinstance(n, int):
        return True
    return False


def isnumber(n):
    if isrealnumber(n) or \
            isinstance(n, Complex):
        return True
    return False


def extract_function(expr, to_find=None):
    '''Extract a funtion from an expression.
        Args:
            expr: string.
            to_find: function to extract. If is None, extract any function.
        Returns:
            name: function name.
            param: funtion parameter, None if function not found.
    '''
    if to_find is None:
        regex = r"[a-z]+\("
    else:
        regex = to_find + r"\("
    match = list(re.finditer(regex, expr))
    if len(match) == 0:
        return expr, None
    match = match[-1]
    begin = match.span()[0] + len(match.group())
    end = begin
    name = match.group()[:-1]
    count = 1
    while count:
        if expr[end] == '(':
            count += 1
        if expr[end] == ')':
            count -= 1
        end += 1
    param = expr[begin:end - 1]
    if to_find is None and name in ['cos', 'sin', 'tan', 'exp', 'abs', 'sqrt']:
        matches = re.finditer(r"[a-z]+", param)
        for match in matches:
            if match.group() != 'i':
                return expr, None
    return name, param


def rm_brackets(expr):
    '''Removes useless brackets from an expression'''
    regex = r"\([^\(\)]*\)"
    matches = list(re.finditer(regex, expr))
    change = 1
    while len(matches) and change:
        change = 0
        for elem in matches:
            span = elem.span()
            try:
                Real(elem.group()[1:-1])
                if span[0] == 0 or expr[span[0] - 1].isalpha() is False:
                    expr = expr[:span[0]] + elem.group()[1:-1] + expr[span[1]:]
                    change = 1
                    break
            except Exception:
                if ismatrix(elem.group()[1:-1]):
                    expr = expr[:span[0]] + elem.group()[1:-1] + expr[span[1]:]
                    change = 1
                    break
                elif (elem.group()[1:-1].isalpha() and
                        (span[0] == 0 or expr[span[0] - 1].isalpha() is False)) or \
                        ((span[0] == 0 or expr[span[0] - 1] in "(+-") and
                         (span[1] == len(expr) or expr[span[1]] in "+-)")):
                    expr = expr[:span[0]] + elem.group()[1:-1] + expr[span[1]:]
                    change = 1
                    break
        matches = list(re.finditer(regex, expr))
    return expr


def put_space(expr):
    '''Put space around operators'''
    matches = re.finditer(r"[^\(\[;,][^\w\^\.\(\)\[\],;\|]+", expr)
    i = 0
    for elem in matches:
        expr = expr[:elem.span()[0] + i + 1] + \
                " {} ".format(elem.group()[1:]) + expr[elem.span()[1] + i:]
        i += 2
    return expr.strip()


def check_brackets(expr, option=True):
    '''
    Check if all brackets of an expression match
    Args:
        expr: string
        option: an otion to check the order of the match
    '''
    i = 0
    j = 0
    for c in expr:
        if c == '(':
            i += 1
        elif c == ')':
            i -= 1
        elif c == '[':
            j += 1
        elif c == ']':
            j -= 1
        if i < 0 or j < 0 and option:
            return False
    if i != 0 or j != 0:
        return False
    return True


def list_variable(expr):
    '''
    Returns all the unknown variables of an expression.
    '''
    matches = re.finditer(r"[a-z]+", expr)
    var = []
    for match in matches:
        if match.group() in ['i', 't', 'tan', 'exp', 'tan', 'cos',
                             'sin', 'sqrt']:
            continue
        if match.group() not in var:
            var.append(match.group())
    return var
