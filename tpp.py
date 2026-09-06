class Symbol:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return self.s

    def __str__(self):
        return self.s

class Symboler:
    def __init__(self):
        pass

    def __getitem__(self, s):
        return Symbol(s)

def parse(s):
    return eval(s, {}, Symboler())

def evaluate(ls, ctx):
    return ls
