from ast import Param, expr
import sys, signal, string
from parser import Parser
from unicodedata import name

from ft_matrix import Matrix

class str_type:
    STRING = 0,
    FLOAT = 1,
    INTEGER = 3,
    COMPLEX = 4,
    MATRIX = 5

    def get_type(self, elem):
        try:
            nb = float(self)
            if nb.is_integer():
                return self.INTEGER
            return self.FLOAT
        except ValueError:
            for c in elem:
                if c not in " [],;0123456789+-*/i":
                    return self.STRING
            for c in elem:
                if c not in " [],;":
                    return self.COMPLEX
            return self.MATRIX

def isfunction(expr):
    index = expr.find('(')
    if index == -1:
        return expr, None
    end = expr.find(')')
    if end != len(expr) - 1:
        raise ValueError('Invalid command line')
    return expr[:index], expr[index + 1:end]

def calculate(parser, cmd, data):
    if len(cmd) == 2:
        name, param = isfunction(cmd[0])
        if param is None:
            result = parser.start(name, 'var')
        else:
            if name not in data.keys():
                raise ValueError("Function '{}' not defined".format(name))
            if param in data.keys():
                result = data[name].image(data[param])
            else:
                result = data[name].image(param)
    else:
        result = parser.start(cmd, 'var')
    return result


def cli(data, cmd):
    cmd = cmd.split('=')
    parser = Parser(data)
    if len(cmd) == 1 or cmd[1] == '?':
        result = parser.start(cmd[0], 'var')
    elif cmd[1].endswith('?'):
        name, param = isfunction(cmd[0])
        if param == None:
            raise ValueError('Invalid command line')
        if name not in data.keys():
            raise ValueError("Function '{}' not defined".format(name))
        data[name].resolve(cmd[1][:-1], param)
        return data
    elif len(cmd) == 2:
        name, param = isfunction(cmd[0])
        expr = cmd[1]
        if param is None:
            for i in name:
                if i in string.punctuation:
                    raise ValueError("function parameter '{}' is invalid".format(param))
            if name in ['i', 'cos', 'sin', 'tan', 'abs', 'sqrt']:
                raise ValueError("function parameter '{}' is invalid".format(param))
            data[name] = parser.start(expr, 'var')
            result = data[name]
        else:
            for i in param:
                if i in string.punctuation:
                    raise ValueError("function parameter '{}' is invalid".format(param))
            data[name] = parser.start(expr, 'funct', param)
            return data
        result = data[name]
    else:
        raise ValueError('Invalid command line')
    if isinstance(result, Matrix):
        print(result.__repr__())
    else:
        print(result)
    return data


def handle_signal(signum, frame):
    if signum == signal.SIGINT:
        sys.stdout.write('\nUse quit to exit.\n> ')
        return
    

if __name__ == "__main__":
    signal.signal(signal.SIGINT,handle_signal)
    cmd_list = []
    data = {}
    while True:
        try:
            cmd = input('> ')
        except EOFError:
            print()
            break
        cmd_list.append(cmd)
        cmd = cmd.replace(' ', '')
        if cmd == "quit":
            break
        try:
            data = cli(data, cmd)
        except ValueError as err:
            print(err)
