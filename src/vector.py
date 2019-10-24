from output import Output
from logging import log_error

from collections import deque

class Vector:
    output: Output

    def __init__(self, output: Output):
        self.output = output

    def parse(self, tokens: deque) -> None:
        tokens.popleft() # eat 'vector'
        token = tokens[0]
        if token.string != "<":
            log_error(token, "Expected '<' in vector declaration")
        tokens.popleft() # eat '<'
        vec_type = tokens[0]
        self.generate(vec_type.string)
        return

    def generate(self, vec_type: str) -> str:
        name = "vector_" + vec_type
        self.output.vector_out += "#ifndef VECTOR_" + vec_type + "_\n"
        print(self.output.vector_out)
