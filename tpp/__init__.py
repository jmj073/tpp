from collections.abc import Iterable

__all__ = [
    "parse",
    "evaluate",
    "Symbol",
    "Macro",
]

class EvaluationFailed(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

class Symbol:
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return self.s

    def __str__(self):
        return self.s

    def __hash__(self): # TODO
        return hash(self.s)

    def __eq__(self, other):
        return self.s == other.s

class Symboler:
    def __init__(self):
        pass

    def __getitem__(self, s):
        return Symbol(s)

class Macro:
    def __init__(self, f):
        self.f = f

    def __call__(self, ls, env):
        return self.f(ls, env)

class Environment:
    def __init__(self, table=dict(), parent=None):
        self.table = table
        self.parent = parent

    def __setitem__(self, key, value):
        self.table[key] = value

    def __getitem__(self, key):
        try:
            return self.table[key]
        except KeyError:
            if self.parent is None:
                raise KeyError()
            return self.parent[key]

def parse(s):
    return eval(s, {}, Symboler())

def __eval_iterable(exp, env):
    if isinstance(exp, dict):
        return dict(map((lambda tup: (evaluate(tup[0], env), evaluate(tup[1], env))), exp.items()))
    return exp.__class__(map((lambda e: evaluate(e, env)), exp))

def __is_nested_literal(exp):
    if isinstance(exp, str):
        return False

    return isinstance(exp, set) \
        or isinstance(exp, list) \
        or isinstance(exp, dict)


def evaluate(exp, env):
    if not isinstance(exp, tuple):
        if __is_nested_literal(exp):
            return __eval_iterable(exp, env)
        if isinstance(exp, Symbol):
            return env[exp]

        return exp

    tup = exp
    if len(tup) == 0:
        raise EvaluationFailed(f"Invalid Expression: {tup}")
    f = evaluate(tup[0], env)

    if isinstance(f, Macro):
        return f(tup[1:], env)

    args = map((lambda e: evaluate(e, env)), tup[1:])
    return f(*args)
