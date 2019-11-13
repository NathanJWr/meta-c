from c_token import CToken, Tok
from c_parser_utils import get_whole_name, get_func_args, eat_white_space
from c_var import CVarData
from logging import log_error
from container_def import ContainerDef

from collections import deque
from typing import Dict, List

def insert_address(reference_count) -> str:
    string = ""
    if reference_count > 1:
        string += "("
        for i in range(1, reference_count):
            string += "*"
    elif reference_count == 0:
        string += "(&"
    else:
        string += "("
    return string
def insert_copy(reference_count) -> str:
    string = ""
    if reference_count >= 1:
        string += "("
        for i in range(0, reference_count):
            string += "*"
    else:
        string += "("
    return string

def write_to_file(self, list_type) -> None:
    output_file = open("__list_" + list_type + ".h", 'w')
    output_file.write(self.function_defs)
    output_file.close()

def purge_variables(self, variables: List[str]) -> None:
    for var in variables:
        if var in self.variables:
            del self.variables[var]

def parse(self, tokens: deque) -> str:
    normal_out = self.output.normal_out
    token: CToken
    var_name: str = ""
    list_name: str = ""
    list_type: str = ""

    tokens.popleft() # eat 'list'
    token = tokens[0]
    if token.string == "_":
        self.parse_function(tokens)
        return var_name
    if token.string != "<":
        log_error(token, "Expected '<' in listtor declaration")
    tokens.popleft() # eat '<'

    list_type = tokens[0].string
    list_name = self.generate_definition(list_type)

    tokens.popleft()
    token = tokens[0]
    if token.string != ">":
        log_error(token, "Expected '>' in list declaration")

    tokens.popleft() # eat '>'
    eat_white_space(tokens)

    preamble = ""
    pointer = 0
    while tokens[0].string == "*":
        tokens.popleft()
        preamble += "*"
        pointer += 1

    # get whole var name
    eat_white_space(tokens)
    var_name = get_whole_name(tokens)


    # The variable should be discarded when leaving a function
    self.variables[var_name] = CVarData(list_type, pointer)

    while (token.val != Tok.semicolon
            and token.string != ")"
            and token.string != "="):
        token = tokens.popleft()

    if (var_name == ""):
        # Assume user just wants replacement to struct name
        normal_out += list_name + preamble + token.string

    elif (token.val == Tok.semicolon):
        tokens.popleft()
        # listtor_'type' name;
        normal_out += list_name + preamble + " "+ var_name + ";\n"
    elif (token.val == Tok.right_paren):
        normal_out += list_name + preamble + " " + var_name + ")"
    else:
        normal_out += list_name + preamble + " " + var_name + " " + token.string

    self.output.normal_out = normal_out
    return var_name

def parse_function(self, tokens: deque) -> None:
    normal_out = self.output.normal_out
    tokens.popleft() # "eat '_'
    token = tokens[0]
    var_type = ""

    if token.string == "init":
        tokens.popleft() # eat 'init'
        tokens.popleft() # eat '('
        args = get_func_args(tokens)
        if len(args) != 1:
            log_error(tokens[0], "Invalid number of arguments in call to 'list_init'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "list_" + var_type + "_init"
        reference = self.variables[var_name].pointer
        normal_out += insert_address(reference)
        normal_out +=  var_name
    elif token.string == "pushfront":
        tokens.popleft() # eat 'pushfront'
        tokens.popleft() # eat '('
        args = get_func_args(tokens)
        if len(args) != 2:
            log_error(tokens[0], "Invalid number of arguments in call to 'list_pushfront'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        item = args[1]
        normal_out += "list_" + var_type + "_pushfront"
        reference = self.variables[var_name].pointer
        normal_out += insert_address(reference)
        normal_out += var_name + ", " + item
    elif token.string == "pushback":
        tokens.popleft() # eat 'pushback'
        tokens.popleft() # eat '('
        args = get_func_args(tokens)

        if len(args) != 2:
            log_error(tokens[0], "Invalid number of arguments in call to 'list_pushback'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        item = args[1]
        normal_out += "list_" + var_type + "_pushback"
        reference = self.variables[var_name].pointer
        normal_out += insert_address(reference)
        normal_out += var_name + ", " + item
    elif token.string == "front":
        tokens.popleft() # eat 'front'
        tokens.popleft() # eat '('
        args = get_func_args(tokens)
        if len(args) != 1:
            log_error(tokens[0], "Invalid number of arguments in call to 'list_pushfront'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "*list_" + var_type + "_front"
        reference = self.variables[var_name].pointer
        normal_out += insert_copy(reference)
        normal_out += var_name
    elif token.string == "popfront":
        tokens.popleft() # eat 'popfront'
        tokens.popleft() # eat '('
        args = get_func_args(tokens)
        if len(args) != 1:
            log_error(tokens[0], "Invalid number of arguments in call to 'list_pushfront'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "list_" + var_type + "_popfront"
        reference = self.variables[var_name].pointer
        normal_out += insert_address(reference)
        normal_out += var_name
    elif token.string == "at":
        tokens.popleft() # eat 'at'
        tokens.popleft() # eat '('
        args = get_func_args(tokens)
        if len(args) != 2:
            log_error(tokens[0], "Invalid number of arguments in call to 'list_pushfront'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        index = args[1]
        normal_out += "*list_" + var_type + "_at"
        reference = self.variables[var_name].pointer
        normal_out += insert_copy(reference)
        normal_out += var_name + ", " + index

    elif token.string == "free":
        tokens.popleft() # eat 'free'
        tokens.popleft() # eat '('
        args = get_func_args(tokens)
        if len(args) != 1:
            log_error(tokens[0], "Invalid number of arguments in call to 'list_pushfront'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        reference = self.variables[var_name].pointer
        normal_out += "list_" + var_type + "_free"
        normal_out += insert_address(reference)
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
        normal_out += "*list_" + self.get_var_type(var_name, tokens[0])
        normal_out += "_at"
        reference = self.variables[var_name].pointer
        normal_out += insert_copy(reference)
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
def generate_definition(self, list_type: str) -> str:
    name = "list_" + list_type
    if list_type not in self.definitions:
        self.definitions.append(list_type)
        cdef = ContainerDef(self.bounds_checked)
        self.function_defs = cdef.generate_list(list_type)
        write_to_file(self, list_type)
    return name
