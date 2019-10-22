from enum import Enum
from typing import Union

class Token(Enum):
    eof = -1,
    identifier = -2
    vector = -3
    template = -4
    typedef = -5
    constant = -6

last_char: str = ' '
identifier_string: str
current_line = 0
cur_file = open("test3.c", 'r')
def gettok() -> Union[Token, str]:
    global last_char, current_line

    if last_char == "\n":
        current_line += current_line
    if last_char.isalpha():
        identifier_string = "";
        while last_char.isalnum():
            identifier_string += last_char
            last_char = cur_file.read(1)
        if identifier_string == "vector":
            return Token.vector
        elif identifier_string == "typedef":
            return Token.typdef
        else:
            return Token.identifier


    if not last_char:
        return Token.eof

    this_char: str = last_char
    last_char = cur_file.read(1)
    return this_char
    

while (1):
    val = gettok()
    if val == Token.eof:
        break

    print(val)

