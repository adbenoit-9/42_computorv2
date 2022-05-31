from ast import Param, expr
import sys, signal
from parser import Parser
from unicodedata import name

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

def isfunction(expr):
    index = expr.find('(')
    if index == -1:
        return expr, None
    end = expr.find(')')
    if end != len(expr) - 1:
        raise ValueError('CLI: Invalid command line')
    return expr[:index], expr[index + 1: end - 1]

def calculate(parser, cmd, data):
    if len(cmd) == 2:
        name, param = isfunction(cmd[0])
        if param is None:
            result = parser.start(name, 'var')
        else:
            if name not in data.key():
                raise ValueError('CLI: Function {} not defined'.format(name))
            result = data[name].image(param)
    else:
        result = parser.start(cmd, 'var')
    return result


def cli(data, cmd):
    cmd = cmd.split('=')
    parser = Parser(data)
    if len(cmd) == 1 or cmd[1] == '?':
        result = calculate(parser, cmd, data)
    elif len(cmd) == 2:
        name, param = isfunction(cmd[0])
        expr = cmd[1]
        if param is None:
            data[name] = parser.start(expr, 'var')
        else:
            data[name] = parser.start(expr, 'funct')
        result = data[name]
    else:
        raise ValueError('CLI: Invalid command line')
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
        except Exception as err:
            print(err)
