import sys
from parse_cmd import parse_cmd

def cli(data, cmd):
    cmd = cmd.split('=')
    if len(cmd) == 1:
        result = compute(cmd)
    elif len(cmd) == 2:
        result = parse_cmd(data, cmd)
    else:
        raise ValueError('parse error')
    print(result)
    return data


if __name__ == "__main__":
    cmd_list = []
    data = {}
    while True:
        cmd = input('> ')
        cmd_list.append(cmd)
        if cmd == "quit":
            break
        try:
            data = cli(data, cmd)
        except Exception as err:
            print(err)
