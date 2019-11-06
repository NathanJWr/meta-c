from vector import Vector
from output import Output
from c_token import CToken, Tok
from c_parser_utils import get_whole_name, eat_white_space
from c_list import CList

from collections import deque
from typing import List
    
include_list: List[str] = []
def generate_include(output: Output, definitions: List[str], container: str) -> None:
    #global include_list
    #if not name in include_list:
    #    output.global_out += "#include \"__" + name + ".h\"\n"
    #    include_list.append(name)
    for definition in definitions:
        output.global_out += "#include \"__" + container + "_" + definition + ".h\"\n"
    return

class CParser:
    function_types = ["char", "short", "int", "long", "void"]

    def parse_function(self,
                       output: Output,
                       tokens: deque,
                       source_file: int,
                       name: str,
                       c_type: str,
                       vector: Vector,
                       c_list: CList) -> None:
        print("Parsing " + name)
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
                if not string in vector.variables:
                    output.normal_out += string
                else:
                    vector.parse_variable(tokens, string)
            else:
                output.normal_out += token.string
                tokens.popleft()

        # get rid of local variables from lists so they don't
        # affect other areas of the source code
        # generate_include(output, vector.definitions)
        vector.purge_variables(local_vars)

    def parse(self,
              output: Output,
              tokens: deque,
              source_file: int) -> None:
        vector = Vector(output)
        c_list = CList(output)
        while tokens:
            token = tokens[0]
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

                elif not string in vector.variables:
                    output.normal_out += string
                else:
                    vector.parse_variable(tokens, string)
            else:
                output.normal_out += token.string
                tokens.popleft()
        generate_include(output, vector.definitions, "vector")
        generate_include(output, c_list.definitions, "list")
        return

    def parse_typedef(self, output: Output, tokens: deque) -> None:
        token = tokens.popleft() # eat 'typedef'

        while token.val != Tok.identifier:
            token = tokens.popleft()

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
