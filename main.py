#!/usr/bin/env python3

import atexit
import os
import readline
from str_util import match_paren
from check_none import there_is, ThereIsNo
import tpp

PROMPT = ">> "
CONT_PROMPT = ".. "

def read_input():
    try:
        s = input(PROMPT)
        new_s = s
        stk = []

        while True:
            stk = there_is(match_paren(new_s, stk))
            if not stk:
                break
            new_s = input(CONT_PROMPT)
            s += new_s

        return s

    except ThereIsNo:
        return None


def init_repl():
    histfile = os.path.join(os.path.expanduser("~"), ".tpp_history")
    try:
        readline.read_history_file(histfile)
        h_len = readline.get_current_history_length()
    except FileNotFoundError:
        open(histfile, 'wb').close()
        h_len = 0

    def save(prev_h_len, histfile):
        new_h_len = readline.get_current_history_length()
        readline.set_history_length(1000)
        readline.append_history_file(new_h_len - prev_h_len, histfile)

    atexit.register(save, h_len, histfile)



def do_repl():
    init_repl()

    while True:
        s = read_input()

        if s is None:
            print("Invalid syntax!")
            continue

        ls = tpp.parse(s)
        v = tpp.evaluate(ls, {})
        if v is not None:
            print(v)


def main():
    return do_repl()

if __name__ == "__main__":
    main()