from logging import log_error
from output import Output
from c_token import CToken, Tok
from c_parser_utils import get_whole_name, get_func_args

from collections import deque
from typing import Dict, List, Union

class CList:
    output: Output
    variables: Dict[str, str] = dict()
    definitions: List[str] = []
    function_defs: str

    def __init__(self, output: Output):
        self.output = output
        self.definitions.clear()
        self.variables.clear()
        self.function_defs = ""

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
        print(list_name)

        tokens.popleft() # eat '>'
        token = tokens[0]
        if token.string != ">":
            log_error(token, "Expected '>' in listtor declaration")

        # make sure you don't hit the end of statment before finding a var name
        while token.val != Tok.identifier:
            if token.val == Tok.semicolon:
                log_error(token, "Expected variable name in listtor declaration")
            tokens.popleft()
            token = tokens[0]

        # get whole var name
        var_name = get_whole_name(tokens)

        # The variable should be discarded when leaving a function
        self.variables[var_name] = list_type

        while (token.val != Tok.semicolon) and (token.string != ")"):
            token = tokens.popleft()

        if (token.val == Tok.semicolon):
            tokens.popleft()
            # listtor_'type' name;
            normal_out += list_name + " " + var_name + ";\n"
        elif (token.val == Tok.left_paren):
            normal_out += list_name + " " + var_name

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
            normal_out += "(&" + var_name
        if token.string == "push":
            tokens.popleft() # eat 'push'
            tokens.popleft() # eat '('
            args = get_func_args(tokens)
            if len(args) != 2:
                log_error(tokens[0], "Invalid number of arguments in call to 'list_push'")
            var_name = args[0]
            var_type = self.get_var_type(var_name, tokens[0])
            item = args[1]
            normal_out += "list_" + var_type + "_push"
            normal_out += "(&" + var_name + ", " + item

        token = tokens[0]
        while token.val != Tok.semicolon:
            normal_out += token.string
            tokens.popleft()
            token = tokens[0]
        normal_out += ";"
        tokens.popleft()
        self.output.normal_out = normal_out

    def get_var_type(self, var_name: str, token: CToken) -> str:
        var_type = ""
        if var_name in self.variables:
            var_type = self.variables[var_name]
        else: 
            log_error(token, "Variable '" + var_name + "' does not exist.")
        return var_type

    def parse_variable(self, tokens: deque, var_name: str) -> None:
        if tokens[0].string == "[":
            tokens.popleft()
            normal_out = self.output.normal_out
            normal_out += "*list_" + self.get_var_type(var_name, tokens[0])
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
    def generate_definition(self, list_type: str) -> str:
        name = "list_" + list_type
        if list_type in self.definitions:
            return name

        self.definitions.append(list_type)
        tab = "    "
        output = self.function_defs

        output += "#include <stdlib.h>\n"
        output += "#ifndef LIST_" + list_type + "_\n"
        output += "#define LIST_" + list_type + "_\n"

        # typedef strcut _Node_type {
        #     type item;
        #     struct _Node* next
        # } Node_type;
        node_name = "Node_" + list_type
        output += "typedef struct _" + node_name + " {\n"
        output += tab + list_type + " item;\n"
        output += tab + "struct _" + node_name + "* next;\n"
        output += "} " + node_name + ";\n"

        # typedef struct {
        #     size_t length;
        #     node_name* head;
        #     node_name* tail;
        # } list_type;
        list_name = "list_" + list_type
        output += "typedef struct {\n"
        output += tab + "size_t length;\n"
        output += tab + node_name + "* head;\n"
        output += tab + node_name + "* tail;\n"
        output += "} " + list_name + ";\n"

        # void list_type_init(list_type* list) {
        #     list->head = NULL;
        #     list->tail = NULL;
        #     list->length = 0
        # }
        function_stub = "list_" + list_type
        output += "static void " + function_stub + "_init(" + function_stub + "* list) {\n"
        output += tab + "list->head = NULL;\n"
        output += tab + "list->tail = NULL;\n"
        output += tab + "list->length = 0;\n"
        output += "}\n"

        # void list_type_push(list_type* list, type item) {
        #     node = malloc(sizeof(node));
        #     node.item = item;
        #     if (!list->head) {
        #         list->head = node;
        #         list->tail = node;
        #         list->length++;
        #         return;
        #     }
        #     node->next = list->head;
        #     list->head = node;
        #     list->length++;
        # }
        output += "static void " + function_stub + "_push(" + function_stub + "* list, " + list_type + " item) {\n"
        output += tab + node_name + "* node = malloc(sizeof(" + node_name + "));\n"
        output += tab + "node->item = item;\n"
        output += tab + "if (!list->head) {\n"
        output += tab + tab + "list->head = node;\n"
        output += tab + tab + "list->tail = node;\n"
        output += tab + tab + "list->length++;\n"
        output += tab + tab + "return;\n"
        output += tab + "}\n"
        output += tab + "node->next = list->head;\n"
        output += tab + "list->head = node;\n"
        output += tab + "list->length++;\n"
        output += "}\n"

        output += "#endif //LIST_" + list_type + "_\n"
        self.function_defs = output
        self.write_to_file(list_type)

        return name

