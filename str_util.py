from functional import *

def is_char(x):
    return (isinstance(x, str) and len(x) == 1)

def get_paren_pair(ch):
    return {
        '(': ')',
        ')': '(',
        '[': ']',
        ']': '[',
        '{': '}',
        '}': '{',
        '"': '"',
        "'": "'",
    }[ch]

def is_open_paren(ch):
    return (is_char(ch) and (ch in "([{"))

def is_close_paren(ch):
    return (is_char(ch) and (ch in ")]}"))

def is_paren(ch):
    return (is_char(ch) and (ch in "()[]{}"))

def is_quote(ch):
    return (is_char(ch) and (ch in "\"'"))

@do_notation(bind4none)
def match_paren(ls, stk=[]):
    for ch in ls:
        if not stk:
            ch = yield into_none(is_close_paren, ch)
            stk.append(ch)
        elif is_quote(ch) and ch == stk[-1]:
            stk.pop()
        elif not is_quote(stk[-1]):
            if is_close_paren(ch):
                open_paren = get_parent_pair(ch)
                yield into_none(bind(eq, stk[-1]), open_paren)
                stk.pop()
            else:
                stk.append(ch)

    return stk