from logging import log_error
from output import Output
from c_token import CToken, Tok

from collections import deque
from typing import Dict, List

def get_func_arg(tokens: deque) -> str:
    arg = ""
    while 1:
        token = tokens[0]
        if token.string == ",":
            return arg
        elif token.string.isspace():
            return arg
        elif token.string == ")":
            return arg
        elif token.val == Tok.identifier:
            arg += token.string
        else:
            arg += token.string
        tokens.popleft()


def get_func_args(tokens: deque) -> List:
    token = tokens[0]
    args = []
    while token.string != ")":
        while token.string == "," or token.string.isspace():
            tokens.popleft()
            token = tokens[0]
        args.append(get_func_arg(tokens))
        token = tokens[0]
    return args

class Vector:
    output: Output
    variables: Dict[str, str] = dict()
    init_list: List[str] = []

    # should be given output.vector_out
    def __init__(self, output: Output):
        self.output = output
        # need the standard lib for malloc/realloc
        output.vector_out += "#include <stdlib.h>\n"

    def purge_variables(self, variables: List[str]) -> None:
        for var in variables:
            if var in self.variables:
                del self.variables[var]


    def parse(self, tokens: deque) -> str:
        normal_out: str = self.output.normal_out
        token: CToken
        var_name: str = ""
        vec_name: str = ""
        vec_type: str = ""

        tokens.popleft() # eat 'vector'
        token = tokens[0]
        if token.string == "_":
            self.parse_function(tokens)
            return var_name
        if token.string != "<":
            log_error(token, "Expected '<' in vector declaration")
        tokens.popleft() # eat '<'

        vec_type = tokens[0].string
        vec_name = self.generate_definition(vec_type)
        print(vec_name)

        tokens.popleft() # eat '>'
        token = tokens[0]
        if token.string != ">":
            log_error(token, "Expected '>' in vector declaration")

        # make sure you don't hit the end of statment before finding a var name
        while token.val != Tok.identifier:
            if token.val == Tok.semicolon:
                log_error(token, "Expected variable name in vector declaration")
            tokens.popleft()
            token = tokens[0]

        # get whole var name
        while token.val != Tok.semicolon and token.string != ")":
            var_name += token.string
            tokens.popleft()
            token = tokens[0]

        # The variable should be discarded when leaving a function
        self.variables[var_name] = vec_type

        while (token.val != Tok.semicolon) and (token.string != ")"):
            token = tokens.popleft()

        if (token.val == Tok.semicolon):
            tokens.popleft()
            tokens.popleft()
            # vector_'type' name;
            normal_out += vec_name + " " + var_name + ";\n"
        elif (token.string == ")"):
            normal_out += vec_name + " " + var_name


        self.output.normal_out = normal_out
        return var_name
    def parse_variable(self, tokens: deque, var_name: str) -> None:
        if tokens[0].string == "[":
            tokens.popleft()
            normal_out = self.output.normal_out
            normal_out += "*vector_" + self.get_var_type(var_name, tokens[0])
            normal_out += "_at(" + var_name + ", "

            token = tokens[0]
            if token.val == Tok.constant or token.val == Tok.identifier or token.val == Tok.char:
                normal_out += token.string
            else:
                log_error(token, "Expected a number or variable after '['")
            tokens.popleft()
            tokens.popleft()

            normal_out += ")"
            self.output.normal_out = normal_out
        else:
            self.output.normal_out += var_name

        return

    def get_var_type(self, var_name: str, token: CToken) -> str:
        var_type = ""
        if var_name in self.variables:
            var_type = self.variables[var_name]
        else: 
            log_error(token, "Variable '" + var_name + "' does not exist.")
        return var_type

    def parse_function(self, tokens: deque) -> None:
        normal_out = self.output.normal_out
        tokens.popleft() # "eat '_'
        token = tokens[0]
        var_type = ""

        if token.string == "push":
            tokens.popleft() # "eat 'push'
            tokens.popleft() # "eat '('
            args = get_func_args(tokens)
            if len(args) != 2:
                log_error(tokens[0], "Invalid number of arguments in call to 'vector_push'")

            var_name = args[0] # expect first arg to be name
            var_type = self.get_var_type(var_name, tokens[0])

            normal_out += "vector_" + var_type + "_push"
            normal_out += "(&" + var_name + ", " + args[1]
        if token.string == "at":
            tokens.popleft()
            tokens.popleft()
            args = get_func_args(tokens)
            if len(args) != 2:
                log_error(tokens[0], "Invalid number of arguments in call to 'vector_at'")
            var_name = args[0]
            var_type = self.get_var_type(var_name, tokens[0])
            normal_out += "*vector_" + var_type
            normal_out += "_at(" + var_name + ", " + args[1]
        if token.string == "front":
            tokens.popleft() # Eat 'front'
            tokens.popleft() # Eat '('
            args = get_func_args(tokens)
            if len(args) != 1:
                log_error(tokens[0], "Invalid number of arguments in call to 'vector_front'")
            var_name = args[0]
            var_type = self.get_var_type(var_name, tokens[0])
            normal_out += "*vector_" + var_type + "_front(" + var_name
        if token.string == "insert":
            tokens.popleft() # Eat 'insert'
            tokens.popleft() # Eat '('
            args = get_func_args(tokens)
            if len(args) != 3:
                log_error(tokens[0], "Invalid number of arguments in call to 'vector_insert'")
            var_name = args[0]
            var_type = self.get_var_type(var_name, tokens[0])
            normal_out += "vector_" + var_type + "_insert(&"
            normal_out += args[0] + ", " + args[1] + ", " + args[2]
        if token.string == "free":
            tokens.popleft() # Eat 'free'
            tokens.popleft() # Eat '('
            args = get_func_args(tokens)
            if len(args) != 1:
                log_error(tokens[0], "Invalid number of arguments in call to 'vector_free'")
            var_name = args[0]
            var_type = self.get_var_type(var_name, tokens[0])
            normal_out += "vector_" + var_type + "_free"
            normal_out += "(&" + var_name
        if token.string == "init":
            tokens.popleft() # Eat 'init'
            tokens.popleft() # Eat '('
            args = get_func_args(tokens)
            if len(args) != 1:
                log_error(tokens[0], "Invalid number of arguments in call to 'vector_init'")
            var_name = args[0]
            var_type = self.get_var_type(var_name, tokens[0])
            normal_out += "vector_" + var_type + "_init"
            normal_out += "(&" + var_name



        token = tokens[0]
        while token.val != Tok.semicolon:
            normal_out += token.string
            tokens.popleft()
            token = tokens[0]
        normal_out += ";"
        tokens.popleft()
        self.output.normal_out = normal_out




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
        output += tab + vec_type + "* items;\n"
        output += tab + "int tot_size;\n"
        output += tab + "int cur_size;\n"
        output += "} vector_" + vec_type + ";\n"


        # void Vector_'Type'_init(Vector_'Type' *Vec) {
        #      Vec->Items = malloc(100 * sizeof('Type'));
        #      Vec->TotSize = 100;
        #      Vec->CurSize = 0;
        # }
        output += "void " + name + "_init(" + name + " *vec) {\n"
        output += tab + "vec->items = "
        output += "(" + vec_type + " *) "
        output +="malloc(100 * sizeof(" + vec_type + "));\n"
        output += tab + "vec->tot_size = 100;\n"
        output += tab + "vec->cur_size = 0;\n"
        output += "}\n"

        # void vector_'Type'_expand(vector_'Type' *Vec) {
        #     Vec->TotSize = Vec->TotSize  * 2;
        #     Vec->Items = realloc(Vec->Items, sizeof('Type') * Vec->TotSize);
        # }
        output += "void vector_" + vec_type + "_expand(vector_" + vec_type + " *vec) {\n"
        output += tab + "vec->tot_size = vec->tot_size * 2;\n"
        output += tab + "vec->items = (" + vec_type + " *) "
        output += "realloc(vec->items, sizeof(" + vec_type + ") * vec->tot_size);\n"
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
        output += "void vector_" + vec_type + "_insert(vector_" + vec_type + " *vec, int pos, " + vec_type + " item) {\n"
        output += tab + "for (int i = vec->cur_size + 1; i > pos - 1; i--) {\n"
        output += tab + tab + "vec->items[i+1] = vec->items[i];\n"
        output += tab + "}\n"
        output += tab + "vec->items[pos] = item;\n"
        output += tab + "vec->cur_size++;\n"
        output += "}\n"

        #  inline 'Type'* vector_'Type'_at(vector_'Type' Vec, int Pos) {
        #      return &Vec.Items[Pos]
        #  }
        output += "static inline " + vec_type + "* vector_" + vec_type +"_at(vector_" +vec_type + " vec, int pos) {\n"
        output += tab + "return &vec.items[pos];\n"
        output += "}\n"

        # inline 'Type'* vector_'Type'_front(vector_'Type' vec) {
        #       return &vec->items[0]
        # }
        output += "static inline " + vec_type + "* vector_" + vec_type
        output += "_front(vector_" + vec_type + " vec) {\n"
        output += tab + "return &vec.items[0];\n"
        output += "}\n"

        
        # static inline void vector_'Type'_free(vector_'Type' *Vec) {
        #      free(Vec->Items);
        #      Vec->Items = 0;
        #      Vec->CurSize = 0;
        #      Vec->TotSize = 0;
        # }
        output += "static inline void vector_" + vec_type + "_free(vector_" + vec_type + " *vec) {\n"
        output += tab + "free(vec->items);\n"
        output += tab + "vec->items = 0;\n"
        output += tab + "vec->cur_size = 0;\n"
        output += tab + "vec->tot_size = 0;\n"
        output += "}\n"

        output += "#endif // VECTOR_" + vec_type + "_\n"

        self.output.vector_out = output
        return name
