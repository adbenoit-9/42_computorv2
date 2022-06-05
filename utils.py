from ft_complex import Complex
import re

def isrealnumber(n):
    if isinstance(n, float) or isinstance(n, int):
        return True
    return False


def isnumber(n):
    if isrealnumber(n) or \
            isinstance(n, Complex):
        return True
    return False

def rm_useless_brackets(expr):
    regex = r"\([^\(\)]*\)"
    matches = list(re.finditer(regex, expr))
    change = 1
    while len(matches) and change:
        change = 0
        for elem in matches:
            span = elem.span()
            if (span[0] == 0 or expr[span[0] - 1] in "(+-") and \
                    (span[1] == len(expr) or expr[span[1]] in "+-)"):
                expr = expr[:span[0]] + elem.group()[1:-1] + expr[span[1]:]
                change = 1
                break
        matches = list(re.finditer(regex, expr))
    return expr
