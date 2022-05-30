class State:
    ERROR = -1
    BEGIN = 0
    GET_SIGN = 1
    GET_VALUE = 2
    GET_MUL = 3
    GET_POWER = 4


def parse_power(values, x, state, val, side):
    if state != State.GET_VALUE and state != State.GET_POWER \
            and state != State.BEGIN:
        return State.ERROR, values, val
    if state != State.GET_POWER:
        val *= side
    if x.startswith('X^'):
        values[int(x[2:])] += val
    elif x == 'X':
        values[1] += val
    else:
        return State.ERROR, values, val
    val = 1.
    return State.GET_SIGN, values, val


def parse_sign(values, sign, state, val):
    if state == State.GET_MUL:
        values[0] += val
        val = 1.
    elif state != State.GET_SIGN and state != State.BEGIN:
        return State.ERROR, values, val
    if sign == '-':
        val *= -1
    elif sign != '+':
        return State.ERROR, values, val
    return State.GET_VALUE, values, val


def parse_value(x, state, val, side):
    if state != State.GET_VALUE and state != State.BEGIN:
        return State.ERROR, val
    if x.startswith('X') is False:
        val = val * float(x) * side
    return State.GET_MUL, val


def parse_equal(values, x, state, val, side):
    if state == State.GET_MUL:
        values[0] += val
        val = 1.
    elif state != State.GET_SIGN or side == -1:
        return State.ERROR, values, val, side
    return State.BEGIN, values, val, -1


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
    values = [0] * (n + 1)
    for x in split_p:
        if x == '=':
            state, values, val, side = parse_equal(values, x, state, val, side)
        elif x.startswith('X'):
            state, values, val = parse_power(values, x, state, val, side)
        elif x in '+-':
            state, values, val = parse_sign(values, x, state, val)
        elif x == '*' and state == State.GET_MUL:
            state = State.GET_POWER
        else:
            state, val = parse_value(x, state, val, side)
        if state == State.ERROR:
            return None
    if state == State.GET_MUL:
        values[0] += val
    elif state != State.GET_SIGN or side != -1:
        return None
    for i in range(len(values)):
        if values[i].is_integer():
            values[i] = int(values[i])
    return values
