#!/usr/bin/env python3

import atexit
import os
import sys
import readline # TODO
from str_util import match_paren
import tpp
import tpp.core as core
from result import Ok, Err, Result, is_ok, is_err

PROMPT = ">> "
CONT_PROMPT = ".. "

def read_input():
    s = input(PROMPT)
    new_s = s
    stk = []

    while True:
        matched = match_paren(new_s, stk)
        if not matched:
            return Err(f"Unmatched parentheses: {new_s}")
        if len(stk) == 0:
            break
        new_s = input(CONT_PROMPT)
        s += new_s

    return Ok(s)


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
    env = core.get_default_env()

    while True:
        try:
            res = read_input()
        except EOFError:
            break
        if res.is_err():
            print(res.err_value, file=sys.stderr)
            continue

        try:
            s = res.ok_value
            exp = tpp.parse(s)
        except Exception as e:
            print(e, file=sys.stderr)
            continue

        try:
            v = tpp.evaluate(exp, env)
        except Exception as e:
            print(e, file=sys.stderr)
            continue

        if v is not None:
            print(v)


def main():
    return do_repl()

if __name__ == "__main__":
    main()
