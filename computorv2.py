import sys
from parsing import parse_cmd

def cli(data, cmd):
    cmd = cmd.split('=')
    if len(cmd) == 1:
        result = compute(cmd)
    elif len(cmd) == 2:
        result = parse_cmd(data, cmd)
    else:
        result = 'parse error'
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
        data = cli(data, cmd)
