from polynomial import Polynomial
from utils import isnumber
from ft_complex import Complex
from function import Function
import re

class str_type:
    STRING = 0,
    FLOAT = 1,
    INTEGER = 3,
    COMPLEX = 4

    def get_type(self, elem):
        try:
            nb = float(self)
            if nb.is_integer():
                return self.INTEGER
            return self.FLOAT
        except ValueError:
            for c in elem:
                if c not in " 0123456789+-*/i":
                    return self.STRING
            return self.COMPLEX


class State:
    ERROR = -1,
    BEGIN = 0,
    GET_NUM = 1,
    GET_VAR = 2,
    GET_OP = 3

def do_operation(data, x1, x2, op):
    if op == '+':
        return x1 + x2
    elif op == '-':
        return x1 - x2
    elif op == '*':
        return x1 * x2
    elif op == '/':
        return x1 / x2
    elif op == '%':
        return x1 % x2
    elif op == '^':
        return x1 ** x2

def parse_value(data, value):
    nb = ""
    ret = 0
    var_name = ""
    expr = re.split('()', value)
    result = [{'value': 0,
                'op': "" }] * len(expr)
    for i, value in enumerate(expr):
        state = State.BEGIN
        value = value.strip()
        for j, c in enumerate(value):
            if c in "0123456789.":
                state = State.GET_NUM
                val += c
            elif c in "+-*/%^":
                val = get_value(val, state)
                do_operation(result[i], val, op)
                state = State.GET_OP
                val = ""
                op = c
                result[i]
            elif c == ' ':
                continue
            else:
                state = State.GET_VAR
                val += c
        if state == State.GET_OP:
            result[i].op = op
    return value


def parse_function(data, value, param):
    expr= value.replace('X', param)
    try:
        funct = Function(Polynomial(expr))
    except:
        raise ValueError('Function invalid')
    return funct


def parse_cmd(data, cmd):
    name = cmd[0].strip()
    value = cmd[1].strip()
    index = name.find('(')
    if index == -1:
        if value == '?':
            return parse_value(data, name)
        else:
            data[name] = parse_value(data, value)
    else:
        end = name.find(')')
        if end != len(name) - 1:
            raise ValueError('parse error')
        param = name[index + 1: end - 1]
        name = name[:index]
        if str_type.get_type(param) == str_type.STRING:
            if name in data.keys():
                return data[name].image(param)
            raise ValueError('Function {} not defined'.format(name))
        else:
            data[name] = parse_function(data, value, param)
    return data[name]
