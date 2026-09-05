from functools import partial

bind = partial

def entity(x):
    return x

def eq(a, b):
    return a == b

def neq(a, b):
    return a != b

def do_notation(bind_func):
    def decorator_do_notation(gen_func):
        def wrapper(*args, **kwargs):
            gen = gen_func(*args, **kwargs)
            try:
                def k(v):
                    try:
                        return bind_func(k, gen.send(v))
                    except StopIteration as e:
                        return e.value
                return bind_func(k, next(gen))
            except StopIteration as e:
                return e.value
        return wrapper
    return decorator_do_notation

def map4none(f, x):
    if x is None:
        return None
    res = f(x)
    if res is None: # TODO
        raise Exception(f"The result of map cannot be None!: {res}")
    return res

def bind4none(f, x):
    if x is None:
        return None
    return f(x)

def into_none(pred, x):
    if pred(x):
        return x
    return None

def unless_none(f, x):
    if x is not None:
        f(x)

if __name__ == "__main__":
    @do_notation(bind4none)
    def test_func1(x):
        y = yield x
        return y

    print(test_func1(3))
    print(test_func1(None))

    @do_notation(bind4none)
    def test_func2(ch):
        ch = yield into_none(lambda x: x == 4, ch)
        return ch

    print(test_func2(4))
    print(test_func2(3))