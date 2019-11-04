from vector import Vector
from output import Output
from c_token import CToken, Tok

from collections import deque
from typing import List
    
include_list: List[str] = []
def generate_include(output: Output, name: str) -> None:
    global include_list
    if not name in include_list:
        output.global_out += "#include \"__" + name + ".h\"\n"
        include_list.append(name)
    return

def get_whole_name(tokens: deque) -> str:
    name = ""
    token = tokens[0]
    while token.val != Tok.semicolon and token.string != ")" and token.string != " " and token.string != "(":
        name += token.string
        tokens.popleft()
        token = tokens[0]
    return name

def parse(output: Output, tokens: deque, source_file: int) -> None:
    vector = Vector(output)
    while tokens:
        token = tokens[0]
        if token.val == Tok.typedef:
            parse_typedef(output, tokens)
        elif token.val == Tok.vector:
            generate_include(output, "vector" + str(source_file))
            vector.parse(tokens)
        elif token.val == Tok.identifier:
            string = get_whole_name(tokens)

            if not string in vector.variables:
                output.normal_out += string
            else:
                vector.parse_variable(tokens)
        else:
            output.normal_out += token.string
            tokens.popleft()
    return

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
    return
