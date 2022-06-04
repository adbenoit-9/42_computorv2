from parser import Parser
from calculator import calculator
from ft_matrix import Matrix
from function import Function
import string


def isfunction(expr):
    index = expr.find('(')
    if index == -1:
        return expr, None
    end = expr.find(')')
    if end != len(expr) - 1:
        raise ValueError('Invalid command line')
    return expr[:index], expr[index + 1:end]



def cli(data, cmd):
    cmd = cmd.split('=')
    parser = Parser(data)
    if len(cmd) == 1 or cmd[1] == '?':
        result = parser.start(cmd[0])
        result = calculator(result, parser)
    elif cmd[1].endswith('?'):
        name, param = isfunction(cmd[0])
        if param == None:
            raise ValueError('Invalid command line')
        if name not in data.keys():
            raise ValueError("Function '{}' not defined".format(name))
        data[name].resolve(cmd[1][:-1], param)
        return None
    elif len(cmd) == 2:
        name, param = isfunction(cmd[0])
        for i in name:
            if i in string.punctuation:
                raise ValueError("variable name '{}' is invalid".format(name))
        if name in ['i', 'cos', 'sin', 'tan', 'abs', 'sqrt']:
            raise ValueError("variable name '{}' is invalid".format(name))
        expr = parser.start(cmd[1])
        if param is None:
            data[name] = calculator(expr, parser)
        else:
            data[name] = Function(expr, param)
        result = data[name]
    else:
        raise ValueError('Invalid command line')
    if isinstance(result, Matrix):
        return result.__repr__()
    return str(result)


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
            print(result)
        except ValueError as err:
            print(err)
    return 0


if __name__ == "__main__":
    main()
