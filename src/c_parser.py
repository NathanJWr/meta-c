from output import Output
from c_token import CToken, Tok
from c_parser_utils import get_whole_name, eat_white_space, get_func_args, eat_after_semicolon
from c_list import CList
from c_vector import CVector
from c_logging import log_error

from collections import deque
from typing import List
    
include_list: List[str] = []
def generate_include(output: Output, definitions: List[str], container: str) -> None:
    for definition in definitions:
        output.global_out += "#include \"__" + container + "_" + definition + ".h\"\n"
    return

def ignore_quotation(output: Output, tokens: deque) -> None:
    output.normal_out += tokens.popleft().string
    token = tokens[0]
    while token.val != Tok.quotation:
        output.normal_out += token.string
        tokens.popleft()
        token = tokens[0]

class CParser:
    function_types = ["char", "short", "int", "long", "void"]
    bounds_checked: bool
    null_on_free: bool
    def __init__(self, bounds_checked: bool, null_on_free: bool):
        self.bounds_checked = bounds_checked
        self.null_on_free = null_on_free

    def parse_function(self,
                       output: Output,
                       tokens: deque,
                       source_file: int,
                       name: str,
                       c_type: str,
                       vector: CVector,
                       c_list: CList) -> None:
        local_vars: List[str] = []
        output.normal_out += c_type + " " + name
        nesting = -1
        while tokens and nesting != 0:
            token = tokens[0]
            if token.val == Tok.left_bracket:
                if nesting == -1:
                    nesting = 1
                else:
                    nesting += 1
            elif token.val == Tok.right_bracket:
                nesting -= 1
            if token.val == Tok.semicolon and nesting == -1:
                # This is just a function statement,
                # not a definition
                return


            if token.val == Tok.quotation:
                ignore_quotation(output, tokens)
            if token.val == Tok.typedef:
                self.parse_typedef(output, tokens)
            elif token.val == Tok.vector:
                var_name = vector.parse(tokens)
                local_vars.append(var_name)
            elif token.val == Tok.c_list:
                var_name = c_list.parse(tokens)
                local_vars.append(var_name)
            elif token.val == Tok.identifier:
                string = get_whole_name(tokens)
                if string in vector.variables:
                    vector.parse_variable(tokens, string)
                elif string in c_list.variables:
                    c_list.parse_variable(tokens, string)
                elif string == "free" and self.null_on_free:
                    output.normal_out += token.string
                    num_tabs = token.num_tabs
                    free_var: List = get_func_args(tokens)
                    eat_after_semicolon(tokens)
                    output.normal_out += "(" + free_var[0] + ");\n"
                    for _ in range(0, num_tabs):
                        output.normal_out += "    "
                        output.normal_out += free_var[0] + " = NULL;\n"
                        tabs = tokens[0].num_tabs
                else:
                    output.normal_out += string
            else:
                output.normal_out += token.string
                tokens.popleft()

        # get rid of local variables from lists so they don't
        # affect other areas of the source code
        # generate_include(output, vector.definitions)
        vector.purge_variables(local_vars)
        print("Done parsing " + name)

    def parse(self,
              output: Output,
              tokens: deque,
              source_file: int) -> None:
        vector = CVector(output, self.bounds_checked)
        c_list = CList(output, self.bounds_checked)
        while tokens:
            token = tokens[0]
            if token.val == Tok.quotation:
                ignore_quotation(output, tokens)

            if token.val == Tok.typedef:
                self.parse_typedef(output, tokens)
            elif token.val == Tok.vector:
                vector.parse(tokens)
            elif token.val == Tok.c_list:
                c_list.parse(tokens)

            elif token.val == Tok.identifier:
                string = get_whole_name(tokens)

                to_compare = string.replace('*', '')
                if to_compare in self.function_types:
                    # see if we are parsing a function
                    # or a variable declaration
                    c_type = string
                    eat_white_space(tokens)
                    name = get_whole_name(tokens)
                    eat_white_space(tokens)
                    if tokens[0].val == Tok.left_paren:
                        self.parse_function(output,
                                            tokens,
                                            source_file,
                                            name,
                                            c_type,
                                            vector,
                                            c_list)

                elif string in vector.variables:
                    vector.parse_variable(tokens, string)
                elif string in c_list.variables:
                    c_list.parse_variable(tokens, string)
                else:
                    output.normal_out += string
            else:
                output.normal_out += token.string
                tokens.popleft()
        generate_include(output, vector.definitions, "vector")
        generate_include(output, c_list.definitions, "list")
        return

    def parse_typedef(self, output: Output, tokens: deque) -> None:
        tokens.popleft() # eat 'typedef'

        eat_white_space(tokens)
        token = tokens[0]
        if token.val == Tok.struct:
            output.global_out += "typedef " + token.string
            while token.val != Tok.right_bracket:
                token = tokens.popleft()
                output.global_out += token.string

            eat_white_space(tokens)
            name = get_whole_name(tokens)
            print("Typedef: " + name)
            self.function_types.append(name)
            output.global_out += " " + name

            while token.val != Tok.semicolon:
                token = tokens.popleft()
                output.global_out += token.string

            tokens.popleft() # eat newline
            output.global_out += "\n"
        return
