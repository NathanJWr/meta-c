from c_logging import log_error
import c_parser_utils as parser_utils
from c_token import CToken, Tok
from container_def import ContainerDef
from collections import deque
from typing import List
def write_to_file(self, vec_type) -> None:
    output_file = open("__vector_" + vec_type + ".h", 'w')
    output_file.write(self.function_defs)
    output_file.close()

def purge_variables(self, variables: List[str]) -> None:
    for var in variables:
        if var in self.variables:
            del self.variables[var]

def parse_function(self, tokens: deque) -> None:
    invalid_num_args = "Invalid number of arguments in call to"
    normal_out = self.output.normal_out
    tokens.popleft() # "eat '_'
    token = tokens[0]
    var_type = ""

    if token.string == "push":
        tokens.popleft() # "eat 'push'
        tokens.popleft() # "eat '('
        args = parser_utils.get_func_args(tokens)
        if len(args) != 2:
            log_error(tokens[0], invalid_num_args + "'vector_push'")

        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "vector_" + var_type + "_push"
        reference = self.variables[var_name].pointer
        normal_out += parser_utils.insert_address(reference)
        normal_out += var_name + ", " + args[1]
    elif token.string == "at":
        tokens.popleft() # "eat 'at'
        tokens.popleft() # "eat '('
        args = parser_utils.get_func_args(tokens)
        if len(args) != 2:
            log_error(tokens[0], invalid_num_args + "vector_at'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "*vector_" + var_type + "_at"
        reference = self.variables[var_name].pointer
        normal_out += parser_utils.insert_copy(reference)
        normal_out += var_name + ", " + args[1]
    elif token.string == "front":
        tokens.popleft() # Eat 'front'
        tokens.popleft() # Eat '('
        args = parser_utils.get_func_args(tokens)
        if len(args) != 1:
            log_error(tokens[0], invalid_num_args + "'vector_front'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "*vector_" + var_type + "_front"
        reference = self.variables[var_name].pointer
        normal_out += parser_utils.insert_copy(reference)
        normal_out += var_name
    elif token.string == "insert":
        tokens.popleft() # Eat 'insert'
        tokens.popleft() # Eat '('
        args = parser_utils.get_func_args(tokens)
        if len(args) != 3:
            log_error(tokens[0], invalid_num_args + "'vector_insert'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "vector_" + var_type + "_insert"
        reference = self.variables[var_name].pointer
        normal_out += parser_utils.insert_address(reference)
        normal_out += var_name + ", " + args[1] + ", " + args[2]
    elif token.string == "free":
        tokens.popleft() # Eat 'free'
        tokens.popleft() # Eat '('
        args = parser_utils.get_func_args(tokens)
        if len(args) != 1:
            log_error(tokens[0], invalid_num_args + "'vector_free'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "vector_" + var_type + "_free"
        reference = self.variables[var_name].pointer
        normal_out += parser_utils.insert_address(reference)
        normal_out += var_name    
    elif token.string == "init":
        tokens.popleft() # Eat 'init'
        tokens.popleft() # Eat '('
        args = parser_utils.get_func_args(tokens)
        if len(args) != 1:
            log_error(tokens[0], invalid_num_args + "'vector_init'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "vector_" + var_type + "_init"
        reference = self.variables[var_name].pointer
        normal_out += parser_utils.insert_address(reference)
        normal_out += var_name
    else:
        log_error(tokens[0], "Function is not supported by the list container")

    token = tokens[0]
    while token.string != ";":
        normal_out += token.string
        tokens.popleft()
        token = tokens[0]

    normal_out += ";"
    tokens.popleft()
    self.output.normal_out = normal_out

def get_var_type(self, var_name: str, token: CToken) -> str:
    var_type = ""
    if var_name in self.variables:
        var_type = self.variables[var_name].c_type
    else:
        log_error(token, "Variable '" + var_name + "' does not exist.")
    return var_type

def parse_variable(self, tokens: deque, var_name: str) -> None:
    if tokens[0].string == "[":
        tokens.popleft()
        normal_out = self.output.normal_out
        normal_out += "*vector_" + self.get_var_type(var_name, tokens[0])
        normal_out += "_at("
        reference = self.variables[var_name].pointer
        normal_out += parser_utils.insert_copy(reference)
        normal_out += var_name + ", "

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
def generate_definition(self, vec_type: str) -> str:
    name = "vector_" + vec_type
    if vec_type not in self.definitions:
        self.definitions.append(vec_type)
        cdef = ContainerDef(self.bounds_checked)
        self.function_defs = cdef.generate_vector(vec_type)
        write_to_file(self, vec_type)
    return name