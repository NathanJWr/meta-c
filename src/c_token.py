from enum import Enum, auto
class Tok(Enum):
    eof = auto()
    identifier = auto()
    vector = auto()
    c_list = auto()
    template = auto()
    typedef = auto()
    struct = auto()
    constant = auto()
    char = auto()
    left_bracket = auto()
    right_bracket = auto()
    left_bracket_sq = auto()
    right_bracket_sq = auto()
    semicolon = auto()
    left_paren = auto()
    right_paren = auto()
    less_than = auto()
    greater_than = auto()
    pound = auto()
    space = auto()
    newline = auto()
    quotation = auto()

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

