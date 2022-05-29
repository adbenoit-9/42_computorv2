from ft_complex import Complex


def isrealnumber(n):
    if isinstance(n, float) or isinstance(n, int):
        return True
    return False


def isnumber(n):
    if isrealnumber(n) or \
            isinstance(n, Complex):
        return True
    return False
