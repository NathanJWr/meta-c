from logging import log_error
from output import Output

from collections import deque
class Vector:
    output: str

    # should be given output.vector_out
    def __init__(self, output: Output):
        self.output = output

    def parse(self, tokens: deque) -> None:
        tokens.popleft() # eat 'vector'
        token = tokens[0]
        if token.string != "<":
            log_error(token, "Expected '<' in vector declaration")
        tokens.popleft() # eat '<'
        vec_type = tokens[0]
        self.generate_definition(vec_type.string)
        return

    def generate_definition(self, vec_type: str) -> str:
        tab = "    "
        output = self.output.vector_out
        name = "vector_" + vec_type

        output += "#ifndef VECTOR_" + vec_type + "_\n"
        output += "#define VECTOR_" + vec_type + "_\n"

        # generate the vec struct
        # Typedef struct {
        #     Type* Items;
        #     int TotSize;
        #     int CurSize;
        # } vector_Type;
        output += "typedef struct {\n"
        output += tab + "Type* Items;\n"
        output += tab + "int TotSize\n"
        output += tab + "int CurSize\n"
        output += "} vector_" + vec_type + "\n"


        # void Vector_'Type'_init(Vector_'Type' *Vec) {
        #      Vec->Items = malloc(100 * sizeof('Type'));
        #      Vec->TotSize = 100;
        #      Vec->CurSize = 0;
        # }

        output += "#endif // VECTOR_" + vec_type + "_\n"

        self.output.vector_out = output

        return name
