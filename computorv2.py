from parser import Parser
from calculator import calculator
from conversion import str_to_complex, str_to_value
from function import Function
from ft_complex import Complex
from utils import check_brackets
import re
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory


def isfunction(expr):
    re_funct = r"(?P<name>[a-z]+)\((?P<param>.*)\)"
    match = re.fullmatch(re_funct, expr)
    if match:
        if check_brackets(match.group('param')):
            return match.group('name'), match.group('param')
    return expr, None


def data_to_str(data):
    ret = ""
    for i, key in enumerate(data.keys()):
        if isinstance(data[key], Function) is False:
            if i != 0:
                ret += '\n'
            if isinstance(data[key], Complex):
                ret += "{}: {}".format(key, repr(data[key]))
            else:
                ret += "{}: {}".format(key, data[key])
    if len(ret) == 0:
        return None
    return ret


def resolve(name, x, y, parser):
    if name is None:
        print('syntax error')
        return
    if name not in parser.data.keys():
        raise ValueError("function '{}' undefined".format(name))
    expr = str(parser.data[name].image(x))
    expr = calculator(expr, parser)
    funct = Function(expr, x)
    try:
        funct.resolve(x, calculator(y, parser))
    except ValueError:
        print('non-solvable expression')


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
        return resolve(name, param, cmd[1][:-1], parser)
    else:
        if name.isalpha() is False:
            raise ValueError('illegal {} name: {}'.format(type_, name))
        if name in ['i', 'cos', 'sin', 'tan', 'abs', 'sqrt', 'exp', 't']:
            raise ValueError('illegal {} name: {}'.format(type_, name))
        if type_ == 'variable':
            result = calculator(cmd[1], parser)
            regex = r"[a-z]+"
            matches = re.finditer(regex, result)
            for match in matches:
                if match.group() != 'i':
                    raise ValueError("variable '{}' undefined"
                                     .format(match.group()))
            data[name] = str_to_value(result, data)
        else:
            expr = calculator(cmd[1], parser, 1)
            data[name] = Function(expr, param)
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
        # except Exception:
        #     print('command failed')
    return 0


if __name__ == "__main__":
    main()
