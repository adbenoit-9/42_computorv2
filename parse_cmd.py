from polynomial import Polynomial
from utils import isnumber
from ft_complex import Complex
from function import Function
import re
from parser import Parser

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


# class State:
#     ERROR = -1,
#     BEGIN = 0,
#     GET_VAL = 2,
#     GET_OP = 3


# def get_value(val, data):
#     try:
#         nb = float(val)
#         if nb.is_integer():
#             return int(nb)
#         return nb
#     except:
#         if val in data.keys():
#             return data[val]
        # check if complex, else undefined var
        

# def do_operation(data, x1, x2, op):
#     if op == '+':
#         return x1 + x2
#     elif op == '-':
#         return x1 - x2
#     elif op == '*':
#         return x1 * x2
#     elif op == '/':
#         return x1 / x2
#     elif op == '%':
#         return x1 % x2
#     elif op == '^':
#         return x1 ** x2
#     elif op == '**':
#         return x1 * x2
#     else:
#         raise ValueError('parse error: operation invalid')

# def set_priority(value):
#     # print(value)
#     ret = []
#     begin = 0
#     state = 0
#     value = value.strip()
#     for i, c in enumerate(value):
#         if c in "-+" and state == 0 and i != 0:
#             print(value[i:])
#             ret.append(set_priority(value[begin:i]))
#             begin = i + 1
#         if c == "(":
#             state += 1
#         if c == ")":
#             state -= 1
#     ret.append(value[begin:])
#     # print(ret)
#     return ret


# def parse_value(data, value):
#     val = ""
#     expr = re.split('()', value) # not solution: prob if (())
#     result = [{'value': 0,
#                 'op': "" }] * len(expr)
#     for i, value in enumerate(expr):
#         state = State.BEGIN
#         value = value.strip()
#         for j, c in enumerate(value):
#             if c in "+-*/%^ ": # prob priority on mul, div and mod
#                 val = get_value(data, val)
#                 result[i].val = do_operation(result[i], val, op)
#                 state = State.GET_OP
#                 val = ""
#                 if c != ' ':
#                     op += c
#             else:
#                 op = ""
#                 state = State.GET_VAL
#                 val += c
#         if state == State.GET_OP:
#             result[i].op = op
#     return value


# def parse_function(data, value, param):
#     expr= value.replace('X', param)
#     try:
#         funct = Function(Polynomial(expr))
#     except:
#         raise ValueError('Function invalid')
#     return funct


def parse_cmd(data, cmd):
    name = cmd[0].strip()
    value = cmd[1].strip()
    parser = Parser(data)
    index = name.find('(')
    if index == -1:
        if value == '?':
            return parser.start(value, 'var')
        else:
            data[name] = parser.start(value, 'var')
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
            data[name] = parser.start(value, 'funct')
    return data[name]
