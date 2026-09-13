from tpp import evaluate, Macro

__all__ = [
    "get_default_env"
]

def __match_tuple(target, pattern):
    pass


def __macro_when(ls, env):
    t = __match_tuple(ls, ("cond", "then", "?else"))

    if evaluate(t["cond"]):
        return evaluate(t["then"], env)

    if "?else" in t:
        return evaluate(t["?else"], env)

    return None


def get_default_env():
    return {
        "print": print,
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "eq": lambda a, b: a == b,
        "neq": lambda a, b: a != b,
        "when": Macro(__macro_when),
    }
