from vector import Vector
from output import Output
from c_token import CToken, Tok

from collections import deque
    
def parse(output: Output, tokens: deque) -> None:
    vector = Vector(output)
    while tokens:
        token = tokens[0]
        if token.val == Tok.typedef:
            parse_typedef(output, tokens)
        elif token.val == Tok.vector:
            vector.parse(tokens)
        elif token.val == Tok.identifier:
            if not token.string in vector.variables:
                output.normal_out += token.string
                tokens.popleft()
            else:
                vector.parse_variable(tokens)
        else:
            token = tokens.popleft()
            output.normal_out += token.string
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
