from tpp import evaluate, Macro, Environment, Symbol
from operator import *
from sys import maxsize

__all__ = [
    "get_default_env"
]

class Quantifier:
    def __init__(self, pat, r=range(maxsize)):
        self.pat = pat
        self.r = r

Q = type(
    "QuantifierGenerator", (object,),
    {    "__add__", (lambda _, pat: Quantifier(pat, range(1, maxsize))) },
    {    "__mul__", (lambda _, pat: Quantifier(pat, range(0, maxsize))) },
    { "__matmul__", (lambda _, pat: Quantifier(pat, range(0,       2))) },
)

# TODO
def __match_tuple(target, pattern):
    assert isinstance(target, tuple)

    if isinstance(pattern, Quantifier):
        q = Quantifier(pattern, range(1, 2))
    else:
        q = pattern

    assert target

    res = dict()
    esac = (isinstance(target[0], tuple), isinstance(q.pat, tuple))

    match esac:
        case (False, False):
            res[q.pat] = target[0]
            res.update( # TODO
        case (False, True):
            raise Exception(f"Unmatched pattern: target[{target}], pattern[{pattern}]")
        case (True, False):
            res[pattern] = target
        case (True, True):
            assert len(target) >= len(pattern) - 1
            for t, p in zip(target, pattern[:-1]):
                res.update(__match_tuple(t, p))

            rest_target = target[len(pattern)-1:]
            last_pat = pattern[-1]
            assert isinstance(last_pat, tuple) or isinstance(last_pat, str)

            if isinstance(last_pat, tuple):
                assert len(target) == len(pattern)
                res.update(__match_tuple(target[-1], last_pat))
            elif last_pat.startswith("*"):
                res[last_pat] = rest_target
            elif last_pat.startswith("?"):
                match len(rest_target):
                    case 0:
                        res[last_pat] = None
                    case 1:
                        res[last_pat] = rest_target[0]
                    case _:
                        raise Exception(f"Unmatched pattern: target[{target}], pattern[{pattern}]")
            elif last_pat.startswith("+"):
                assert len(rest_target) > 0
                res[last_pat] = rest_target
            else:
                assert len(rest_target) == 1
                res[last_pat] = rest_target[0]

    return res


def __macro_when(ls, env):
    t = __match_tuple(ls, ("cond", "then", "?else"))

    if evaluate(t["cond"], env):
        return evaluate(t["then"], env)

    if "?else" in t:
        return evaluate(t["?else"], env)

    return None

def __macro_fn(ls, env):
    t = __match_tuple(ls, ("args", "+exps"))
    params = t["args"]
    exps = t["+exps"]

    def func(*args):
        table = dict(zip(params, args))
        new_env = Environment(table, env)
        ret = None

        for e in exps:
            ret = evaluate(e, new_env)

        return ret

    return func

def __macro_define(ls, env):
    t = __match_tuple(ls, ("sym", "exp"))
    name = t["sym"]
    v = evaluate(t["exp"], env)
    env[name] = v

    return None

def get_default_env():
    S = Symbol
    return Environment({
        S("print"): print,
        S("add"): add,
        S("sub"): sub,
        S("mul"): mul,
        S("eq"): eq,
        S("ne"): ne,
        S("when"): Macro(__macro_when),
        S("fn"): Macro(__macro_fn),
        S("define"): Macro(__macro_define),
    })
