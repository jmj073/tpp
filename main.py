#!/usr/bin/env python3

import atexit
import os
import readline
from str_util import match_paren
from functional import *

PROMPT = ">> "
CONT_PROMPT = ".. "

@do_notation(bind4none)
def read_input():
    s = input(PROMPT)
    stk = []

    while True:
        stk = yield match_paren(s, stk)
        if not stk:
            break
        s += input(CONT_PROMPT)
    
    return s

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
        line = read_input()


def main():
    return do_repl()

if __name__ == "__main__":
    do_repl()