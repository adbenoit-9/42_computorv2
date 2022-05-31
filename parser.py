class Parser:
    '''Parse a mathematic expression.'''

    ERROR = -1,
    BEGIN = 0,
    MUL = 1,
    DIV = 2,
    MOD = 3,
    ADD = 4,
    SUB = 5,
    END = 10

    def __init__(self, data) -> None:
        self.tokens = None
        self.state = None
        self.type = None
        self.data = data

    def start(self, expr, expr_type):
        type_list = ['function', 'f', 'funct', 'variable', 'var', 'v']
        if isinstance(expr, str) is False or \
                isinstance(expr_type, str) is False or \
                expr_type not in type_list:
            raise ValueError('Parser: invalid argument')
        self.tokens = expr
        self.state = self.BEGIN
        self.type = expr_type
        if expr_type in type_list[:2]:
            return self.get_polynom()
        while self.state != self.END:
            new_tokens = []
            for i, token in enumerate(self.tokens):
                new_tokens.append(self.priority(token))
            self.tokens = new_tokens

    def split(self, string, sep, rm_sep=0):
        if isinstance(string, str) is False or \
                isinstance(sep, str) is False or \
                isinstance(rm_sep, int) is False:
            raise ValueError('Parser: split failed')
        tokens = []
        tmp = 0
        for i, c in enumerate(string):
            if c in sep:
                tokens.append(string[tmp:i])
                tmp = i + rm_sep
        if tmp < len(string):
            tokens.append(string[tmp:])
        return tokens

    def calculate(self):
        self.tokens = self.split(self.tokens, '+')
        # for token in self.tokens: