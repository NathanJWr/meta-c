from enum import Enum
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

class CToken:
    def __init__(self, token, string, line_num, num_tabs):
        self.val = token
        self.string = string
        self.line_num = line_num
        self.num_tabs = num_tabs


    val: Tok
    string: str
    line_num: int
    num_tabs: int

