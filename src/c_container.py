from c_parser_utils import get_whole_name, eat_white_space
from c_token import CToken, Tok
from c_var import CVarData

from collections import deque
def parse(container, tokens: deque, container_name: str) -> str:
    normal_out = container.output.normal_out
    token: CToken
    var_name: str = ""
    list_name: str = ""
    list_type: str = ""

    tokens.popleft() # eat 'list'
    token = tokens[0]
    if token.string == "_":
        container.parse_function(tokens)
        return var_name
    if token.string != "<":
        log_error(token, "Expected '<' in " + container_name + " declaration")
    tokens.popleft() # eat '<'

    list_type = tokens[0].string
    list_name = container.generate_definition(list_type)

    tokens.popleft()
    token = tokens[0]
    if token.string != ">":
        log_error(token, "Expected '>' in " + container_name + " declaration")

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
    container.variables[var_name] = CVarData(list_type, pointer)

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

    container.output.normal_out = normal_out
    return var_name
