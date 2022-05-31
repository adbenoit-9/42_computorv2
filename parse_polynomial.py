class State:
    ERROR = -1
    BEGIN = 0
    GET_SIGN = 1
    GET_VALUE = 2
    GET_MUL = 3
    GET_POWER = 4


def parse_power(coefs, x, state, val, side):
    if state != State.GET_VALUE and state != State.GET_POWER \
            and state != State.BEGIN:
        return State.ERROR, coefs, val
    if state != State.GET_POWER:
        val *= side
    if x.startswith('X^'):
        coefs[int(x[2:])] += val
    elif x == 'X':
        coefs[1] += val
    else:
        return State.ERROR, coefs, val
    val = 1.
    return State.GET_SIGN, coefs, val


def parse_sign(coefs, sign, state, val):
    if state == State.GET_MUL:
        coefs[0] += val
        val = 1.
    elif state != State.GET_SIGN and state != State.BEGIN:
        return State.ERROR, coefs, val
    if sign == '-':
        val *= -1
    elif sign != '+':
        return State.ERROR, coefs, val
    return State.GET_VALUE, coefs, val


def parse_value(x, state, val, side):
    if state != State.GET_VALUE and state != State.BEGIN:
        return State.ERROR, val
    if x.startswith('X') is False:
        val = val * float(x) * side
    return State.GET_MUL, val


def parse_equal(coefs, x, state, val, side):
    if state == State.GET_MUL:
        coefs[0] += val
        val = 1.
    elif state != State.GET_SIGN or side == -1:
        return State.ERROR, coefs, val, side
    return State.BEGIN, coefs, val, -1


def fix_polynomial(eq):
    n = len(eq)
    i = 0
    while i < n:
        add = 1
        if eq[i] in "-+=*X":
            if i != 0 and eq[i - 1] != ' ':
                eq = eq[:i] + ' ' + eq[i:]
                i += 1
                n += 1
            if i != n - 1 and eq[i + 1] != ' ' and eq[i] != 'X':
                eq = eq[:i + 1] + ' ' + eq[i + 1:]
                i += 1
                n += 1
        i += add
    return eq


def parse_polynomial(polynomial):
    polynomial = fix_polynomial(polynomial)
    split_p = polynomial.split()
    state = State.BEGIN
    side = 1
    val = 1.
    n = 0
    for x in split_p:
        if x.startswith('X^') and int(x[2:]) > n:
            n = int(x[2:])
        elif x == 'X' and n < 1:
            n = 1
    coefs = [0] * (n + 1)
    for x in split_p:
        if x == '=':
            state, coefs, val, side = parse_equal(coefs, x, state, val, side)
        elif x.startswith('X'):
            state, coefs, val = parse_power(coefs, x, state, val, side)
        elif x in '+-':
            state, coefs, val = parse_sign(coefs, x, state, val)
        elif x == '*' and state == State.GET_MUL:
            state = State.GET_POWER
        else:
            state, val = parse_value(x, state, val, side)
        if state == State.ERROR:
            return None
    if state == State.GET_MUL:
        coefs[0] += val
    elif state != State.GET_SIGN or side != -1:
        return None
    for i in range(len(coefs)):
        if isinstance(coefs[i], float) and coefs[i].is_integer():
            coefs[i] = int(coefs[i])
    return coefs
