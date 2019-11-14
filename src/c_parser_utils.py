from c_token import Tok
from collections import deque
from typing import List

def get_whole_name(tokens: deque) -> str:
    name = ""
    token = tokens[0]
    while (token.val != Tok.semicolon 
        and token.val != Tok.left_paren
        and token.val != Tok.right_paren
        and token.val != Tok.space
        and token.val != Tok.greater_than
        and token.val != Tok.less_than
        and token.val != Tok.left_bracket
        and token.val != Tok.right_bracket
        and token.val != Tok.left_bracket_sq
        and token.val != Tok.right_bracket_sq
        and token.val != Tok.pound
        and token.val != Tok.newline):

        name += token.string
        tokens.popleft()
        token = tokens[0]
    return name

def eat_white_space(tokens: deque) -> None:
    while tokens[0].string.isspace():
        tokens.popleft()

def get_func_args(tokens: deque) -> List:
    token = tokens[0]
    args = []
    while token.string != ")":
        while token.string == "," or token.string.isspace():
            tokens.popleft()
            token = tokens[0]
        args.append(get_func_arg(tokens))
        token = tokens[0]
    return args

def get_func_arg(tokens: deque) -> str:
    arg = ""
    while 1:
        token = tokens[0]
        if token.string == ",":
            return arg
        elif token.string == ")":
            return arg
        elif token.val == Tok.identifier:
            arg += token.string
        else:
            arg += token.string
        tokens.popleft()

def insert_address(reference_count) -> str:
    string = ""
    if reference_count > 1:
        string += "("
        for _ in range(1, reference_count):
            string += "*"
    elif reference_count == 0:
        string += "(&"
    else:
        string += "("
    return string
def insert_copy(reference_count) -> str:
    string = ""
    if reference_count >= 1:
        string += "("
        for _ in range(0, reference_count):
            string += "*"
    else:
        string += "("
    return string