from parser import Parser
from calculator import calculator
from ft_matrix import Matrix
from function import Function
import string, re


def isfunction(expr):
    index = expr.find('(')
    if index == -1:
        return expr, None
    end = expr.find(')')
    if end == -1:
        raise ValueError('syntax error')
    return expr[:index], expr[index + 1:end]


def cli(data, cmd):
    parser = Parser(data, cmd)
    cmd = parser.cmd
    name, param = isfunction(cmd[0])
    typ = 'variable' if param is None else 'function'
    if cmd[1] == '?':
        result = calculator(cmd[0], parser)
    elif cmd[1].endswith('?'):
        if typ != 'function':
            raise ValueError('syntax error')
        if name not in data.keys():
            raise ValueError("function '{}' not defined".format(name))
        data[name].resolve(param, cmd[1][:-1], parser)
        return None
    else:
        if name.isalpha() is False:
            raise ValueError('illegal {} name: {}'.format(t, name))
        if name in ['i', 'cos', 'sin', 'tan', 'abs', 'sqrt']:
            raise ValueError('illegal {} name: {}'.format(t, name))
        if typ == 'variable':
            data[name] = calculator(cmd[1], parser)
        else:
            expr = parser.start(cmd[1])
            data[name] = Function(parser, expr, param)
        result = data[name]
    return parser.end(result)


def main():
    cmd_list = []
    data = {}
    while True:
        try:
            cmd = input('> ')
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print('\nUse quit to exit.')
            continue
        if len(cmd.replace(' ', '')) == 0:
            continue
        cmd_list.append(cmd)
        cmd = cmd.replace(' ', '')
        if cmd == "quit":
            return 0
        try:
            result = cli(data, cmd)
            if result is not None:
                print(result)
        except ValueError as err:
            print(err)
    return 0


if __name__ == "__main__":
    main()
