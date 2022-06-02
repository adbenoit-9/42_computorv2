from ft_matrix import Matrix


def ft_pow(elem, p):
    if isinstance(p, int) is False:
        return None
    if isinstance(elem, Matrix) is True:
        return elem.pow(p)
    return elem ** p
    