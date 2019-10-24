from logging import log_error
from output import Output

from collections import deque
class Vector:
    output: Output

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
        output += tab + "Type* items;\n"
        output += tab + "int tot_size\n"
        output += tab + "int cur_size\n"
        output += "} vector_" + vec_type + "\n"


        # void Vector_'Type'_init(Vector_'Type' *Vec) {
        #      Vec->Items = malloc(100 * sizeof('Type'));
        #      Vec->TotSize = 100;
        #      Vec->CurSize = 0;
        # }
        output += "void " + name + "_init(" + name + " *vec) {\n"
        output += tab + "vec->items = malloc(100 * sizeof(" + vec_type + "));\n"
        output += tab + "vec->tot_size = 100;\n"
        output += tab + "vec->cur_size = 0;\n"
        output += "}\n"

        # void vector_'Type'_expand(vector_'Type' *Vec) {
        #     Vec->TotSize = Vec->TotSize  * 2;
        #     Vec->Items = realloc(Vec->Items, sizeof('Type') * Vec->TotSize);
        # }
        output += "void vector_" + vec_type + "_expand(vector_" + vec_type + " *vec) {\n"
        output += tab + "vec->tot_size = vec->tot_size * 2;\n"
        output += tab + "vec->items = realloc(vec->items, sizeof(" + vec_type + ") * vec->tot_size);\n"
        output += "}\n"

        # void Vector_'Type'_push(Vector_'Type' *Vec, 'Type' Item) {
        #      if (Vec->TotSize == Vec->CurSize) {
        #      }
        #      Vec->Items[Vec->CurSize++] = Item;
        #  }
        output += "void " + name + "_push(" + name + " *vec, " + vec_type + " item) {\n"
        output += tab + "if (vec->tot_size == vec->cur_size) {\n"
        output += tab + tab + "vector_" + vec_type + "_expand(vec);\n"
        output += tab + "}\n"
        output += tab + "vec->items[vec->cur_size++] = item;\n"
        output += "}\n"

        # void vector_'Type'_insert(vector_'Type' *Vec, 'Type' Pos, 'Type' Item) {
        #    for ('Type' i = Vec->CurSize + 1; i > Pos - 1; i--) {
        #        Vec->Items[i+1] = Vec->Items[i]; 
        #    }
        #    Vec->Items[Pos] = Item;
        #    Vec->CurSize++;
        # }
        output += "vector_" + vec_type + "_insert(vector_" + vec_type + " *vec, int pos, " + vec_type + " item) {\n"
        output += tab + "for (int i = vec->cur_size + 1; i > pos - 1; i--) {\n"
        output += tab + tab + "vec->items[i+1] = vec->items[i];\n"
        output += tab + "}\n"
        output += tab + "vec->items[pos] = item;\n"
        output += tab + "vec->cur_size++;\n"
        output += "}\n"

        output += "#endif // VECTOR_" + vec_type + "_\n"

        self.output.vector_out = output

        return name
