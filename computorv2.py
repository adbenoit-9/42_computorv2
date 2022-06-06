from parser import Parser
from calculator import calculator
from ft_matrix import Matrix
from function import Function
import re
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory


def isfunction(expr):
    index = expr.find('(')
    if index == -1:
        return expr, None
    end = expr.find(')')
    if end == -1:
        raise ValueError('syntax error')
    return expr[:index], expr[index + 1:end]


def data_to_str(data):
    ret = ""
    for i, key in enumerate(data.keys()):
        if isinstance(data[key], Function) is False:
            if i != 0:
                ret += '\n'
            ret += "{} = {}".format(key, data[key])
    if len(ret) == 0:
        return None
    return ret


def cli(data, cmd):
    parser = Parser(data, cmd)
    cmd = parser.cmd
    name, param = isfunction(cmd[0])
    type_ = 'variable' if param is None else 'function'
    if cmd[0] == "show data":
        return data_to_str(data)
    elif cmd[1] == '?':
        result = calculator(cmd[0], parser)
    elif cmd[1].endswith('?'):
        if type_ != 'function':
            raise ValueError('syntax error')
        if name not in data.keys():
            raise ValueError("function '{}' undefined".format(name))
        data[name].resolve(param, cmd[1][:-1], parser)
        return None
    else:
        if name.isalpha() is False:
            raise ValueError('illegal {} name: {}'.format(type_, name))
        if name in ['i', 'cos', 'sin', 'tan', 'abs', 'sqrt']:
            raise ValueError('illegal {} name: {}'.format(type_, name))
        if type_ == 'variable':
            data[name] = calculator(cmd[1], parser)
            regex = r"[a-z]+"
            match = re.search(regex, data[name])
            if match is not None and match.group() != 'i':
                raise ValueError("variable '{}' undefined".format(match.group()))
        else:
            expr = calculator(cmd[1], parser)
            data[name] = Function(parser, expr, param)
        result = data[name]
    return parser.end(result)


def main():
    cmd_list = []
    data = {}
    session = PromptSession(history=FileHistory('.computorv2_history'))
    while True:
        try:
            cmd = session.prompt('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            print('Use quit to exit.')
            continue
        if len(cmd.replace(' ', '')) == 0:
            continue
        cmd_list.append(cmd)
        if cmd == "quit":
            return 0
        try:
            result = cli(data, cmd)
            if result is not None:
                print(result)
        except ValueError as err:
            print(err)
        except ZeroDivisionError as err:
            print(err)
        except Exception:
            print('command failed')
    return 0


if __name__ == "__main__":
    main()
