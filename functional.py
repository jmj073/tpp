from functools import partial

bind = partial

def entity(x):
    return x

def eq(a, b):
    return a == b

def neq(a, b):
    return a != b