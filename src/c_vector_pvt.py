def write_to_file(self, vec_type) -> None:
    output_file = open("__vector_" + vec_type + ".h", 'w')
    output_file.write(self.function_defs)
    output_file.close()

def purge_variables(self, variables: List[str]) -> None:
    for var in variables:
        if var in self.variables:
            del self.variables[var]

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

        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "vector_" + var_type + "_push"
        reference = self.variables[var_name].pointer
        normal_out += insert_address(reference)
        normal_out += var_name + ", " + args[1]
    if token.string == "at":
        tokens.popleft() # "eat 'at'
        tokens.popleft() # "eat '('
        args = get_func_args(tokens)
        if len(args) != 2:
            log_error(tokens[0], "Invalid number of arguments in call to 'vector_at'")
        var_name = args[0]
        var_type = self.get_var_type(var_name, tokens[0])
        normal_out += "*vector_" + var_type + "_at"
        reference = self.variables[var_name].pointer
        normal_out += insert_copy(reference)
        normal_out += var_name + ", " + args[1]


