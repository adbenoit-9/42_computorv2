from ft_function import Function
from ft_matrix import Matrix
from ft_complex import Complex
from ft_real import Real
import re


def str_to_matrix(mat, data={}):
    if isinstance(mat, str) is False:
        raise ValueError("str_to_matrix: type '{}' not supported"
                         .format(type(mat).__name__))
    if len(mat) < 2:
        return None
    if mat[0] != '[' or mat[-1] != ']':
        return None
    rows = mat[1:-1].split(';')
    lst = [[] for _ in range(len(rows))]
    for i, row in enumerate(rows):
        if row[0] != '[' or row[-1] != ']':
            return None
        elem_lst = row[1:-1].split(',')
        for elem in elem_lst:
            if '[' in elem or ']' in elem:
                return None
            lst[i].append(str_to_value(elem, data))
    return Matrix(lst)


def str_to_complex(comp):
    comp = comp.replace('-i', '-1*i')
    if isinstance(comp, str) is False:
        raise ValueError("str_to_complex: type '{}' not supported"
                         .format(type(comp).__name__))
    re_im = r"([-+]?[\d\.]+[+-])?([-+]?[\d\.]+[\*]?)?i"
    match = re.fullmatch(re_im, comp)
    if match is None:
        re_im = r"([+-]?[\d\.]+[\*]?)?i[+-][\d\.]+"
        match = re.fullmatch(re_im, comp)
        if match is None:
            return None
    re_nb = r"[+-]?[\d\.]+"
    matches = list(re.finditer(re_nb, comp))
    n = len(matches)
    if n == 0:
        return Complex(im=1)
    elif n == 1:
        if matches[0].span()[1] == len(comp):
            return Complex(1, Real(matches[0].group()))
        if comp[matches[0].span()[1]] == '*' or \
                comp[matches[0].span()[1]] == 'i':
            return Complex(im=Real(matches[0].group()))
        return Complex(real=Real(matches[0].group()), im=1)
    elif comp[matches[0].span()[1]] == '*' or \
            comp[matches[0].span()[1]] == 'i':
        return Complex(im=Real(matches[0].group()),
                       real=Real(matches[1].group()))
    return Complex(real=Real(matches[0].group()),
                   im=Real(matches[1].group()))


def str_to_value(x, data):
    if isinstance(x, str) is False:
        raise ValueError("str_to_value: type '{}' not supported"
                         .format(type(x).__name__))
    if x in data.keys() and isinstance(data[x], Function) is False:
        return data[x]
    comp = str_to_complex(x)
    if comp is not None:
        return comp
    mat = str_to_matrix(x)
    if mat is not None:
        return mat
    try:
        x = Real(x)
        return x
    except Exception:
        if len(x) and x.isalpha() is False and \
                any(operator in "[]()-+/*=%^,;" for operator in x) is False:
            raise ValueError('illegal variable name: {}'.format(x))
        return x
