from enum import Enum
from typing import Union
from typing import Tuple
from typing import List

class Token(Enum):
    eof = -1,
    identifier = -2
    vector = -3
    template = -4
    typedef = -5
    constant = -6

last_char: str = ' '
identifier_string: str = ""
num_string: str
current_line = 0
num_tabs = 0
cur_tok: Union[Token, str]
cur_file = open("test3.c", 'r')

def nexttok() -> Tuple[Union[Token, str], str]:
    global cur_tok, identifier_string
    cur_tok = gettok()
    return cur_tok, identifier_string

def gettok() -> Union[Token, str]:
    global last_char, current_line, num_tabs, identifier_string

    if last_char == "\n":
        current_line += 1

    elif last_char == "{":
        num_tabs += 1

    elif last_char == "}":
        num_tabs -= 1

    elif last_char.isalpha():
        identifier_string = "";
        while last_char.isalnum():
            identifier_string += last_char
            last_char = cur_file.read(1)
        if identifier_string == "vector":
            return Token.vector
        elif identifier_string == "typedef":
            return Token.typedef
        else:
            return Token.identifier

    elif last_char.isdigit():
        identifier_string = "";
        while last_char.isdigit() or last_char == ".":
            identifier_string += last_char
            last_char = cur_file.read(1)
        return Token.constant

    elif not last_char:
        return Token.eof

    this_char: str = last_char
    last_char = cur_file.read(1)
    return this_char
    

token_list: List[Tuple[Union[Token, str], str]] = []
nexttok()
while (1):
    val = nexttok()
    token_list.append(val)
    if val[0] == Token.eof:
        break

print(token_list)

