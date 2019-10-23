from enum import Enum
from collections import deque
from typing import Union
from typing import Tuple
from typing import Deque

class Tok(Enum):
    eof = -1,
    identifier = -2
    vector = -3
    template = -4
    typedef = -5
    constant = -6
    char = -7
    end_bracket = -8
    semicolon = -9

class Token:
    def __init__(self, token, string, line_num):
        self.val = token
        self.string = string
        self.line_num = line_num

    val: Tok
    string: str
    line_num: int


last_char: str = ' '
identifier_string: str = ""
num_string: str
current_line = 0
num_tabs = 0
cur_tok: Union[Token, str]
cur_file = open("test.c", 'r')

class Output:
    global_out = ""
    normal_out = ""
    vector_out = ""


def parse_typedef(output: Output, tokens: deque) -> None:
    token = tokens.popleft() # eat 'typedef'

    while token.val != Tok.identifier:
        token = tokens.popleft()

    if token.string == "struct":
        output.global_out += "typedef " + token.string
        while token.val != Tok.end_bracket:
            token = tokens.popleft()
            output.global_out += token.string
        while token.val != Tok.semicolon:
            token = tokens.popleft()
            output.global_out += token.string

        tokens.popleft() # eat newline
        output.global_out += "\n"

    print(output.global_out)
    return

def parse_vector(output: Output, tokens: deque) -> None:
    tokens.popleft() # eat 'vector'
    token = tokens[0]
    if token.string != "<":
        log_error(token, "Expected '<' in vector declaration")

    return

def log_error(token: Token, error: str) -> None:
    print(str(token.line_num) + ": " + error)

def parse(output: Output, tokens: deque) -> None:
    while tokens:
        token = tokens[0]
        if token.val == Tok.typedef:
            print("Parsing typedef")
            parse_typedef(output, tokens)
        elif token.val == Tok.vector:
            parse_vector(output, tokens)
        else:
            tokens.popleft()
    return

def nexttok() -> Token:
    global cur_tok
    cur_tok = gettok()
    return cur_tok

def gettok() -> Token:
    global last_char, current_line, num_tabs, identifier_string
    this_char: str

    identifier_string = ""
    if last_char == "\n":
        current_line += 1

    elif last_char == "{":
        num_tabs += 1

    elif last_char == "}":
        num_tabs -= 1
        identifier_string = last_char
        last_char = cur_file.read(1)
        return Token(Tok.end_bracket, "}", current_line)

    elif last_char == ";":
        identifier_string = last_char
        last_char = cur_file.read(1)
        return Token(Tok.semicolon, identifier_string, current_line)

    elif last_char.isalpha():
        while last_char.isalnum():
            identifier_string += last_char
            last_char = cur_file.read(1)
        if identifier_string == "vector":
            return Token(Tok.vector, identifier_string, current_line)
        elif identifier_string == "typedef":
            return Token(Tok.typedef, identifier_string, current_line)
        else:
            return Token(Tok.identifier, identifier_string, current_line)

    elif last_char.isdigit():
        while last_char.isdigit() or last_char == ".":
            identifier_string += last_char
            last_char = cur_file.read(1)
        return Token(Tok.constant, identifier_string, current_line)


    elif not last_char:
        return Token(Tok.eof, "", current_line)

    identifier_string = last_char
    last_char = cur_file.read(1)
    return Token(Tok.char, identifier_string, current_line)
    

token_list: Deque[Token] = deque()
nexttok()
while (1):
    tok = nexttok()
    token_list.append(tok)
    if tok.val == Tok.eof:
        break
output = Output()
parse(output, token_list)

