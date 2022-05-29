from utils import isnumber


def parse_value(data, name, value):
    data[name] = value
    return value


def parse_function(data, name, value):
    return value


def parse_cmd(data, cmd):
    name = cmd[0].strip()
    value = cmd[1].strip()
    index = name.find('(')
    if index == -1:
        return parse_value(data, name, value)
    else:
        end = name.find(')')
        if end != len(name) - 1:
            return 'parse error'
        param = name[index + 1: end - 1]
        name = name[:index]
        if isnumber(param): # bon la ca va pas cest une string
            if name in data.keys():
                compute_image(data[name])
            else:
                return 'Function {} not defined'.format(name)
        else:
            return parse_function(data, name, value)
