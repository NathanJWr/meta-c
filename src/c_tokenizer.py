from c_token import CToken, Tok

class Tokenizer:
    last_char: str
    current_line: int
    num_tabs: int
    cur_tok: CToken

    def __init__(self):
        self.last_char = " "
        self.current_line = 1
        self.num_tabs = 0
        

    def nexttok(self, cur_file) -> CToken:
        self.cur_tok = self.gettok(cur_file)
        return self.cur_tok

    def gettok(self, cur_file) -> CToken:
        this_char: str

        identifier_string = ""
        if self.last_char == "\n":
            self.current_line += 1
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.newline, "\n", self.current_line, self.num_tabs)

        elif self.last_char == "{":
            self.num_tabs += 1
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.left_bracket, "{", self.current_line, self.num_tabs)

        elif self.last_char == "}":
            self.num_tabs -= 1
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.right_bracket, "}", self.current_line, self.num_tabs)

        elif self.last_char == "(":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.left_paren, "(", self.current_line, self.num_tabs)
        elif self.last_char == ")":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.right_paren, ")", self.current_line, self.num_tabs)
        elif self.last_char == "<":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.less_than, "<", self.current_line, self.num_tabs)
        elif self.last_char == ">":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.greater_than, ">", self.current_line, self.num_tabs)
        elif self.last_char == "#":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.pound, "#", self.current_line, self.num_tabs)
        elif self.last_char == "[":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.left_bracket_sq, "[", self.current_line, self.num_tabs)
        elif self.last_char == "]":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.right_bracket_sq, "]", self.current_line, self.num_tabs)
        elif self.last_char == " ":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.space, " ", self.current_line, self.num_tabs)

        elif self.last_char == ";":
            identifier_string = self.last_char
            self.last_char = cur_file.read(1)
            return CToken(Tok.semicolon, identifier_string, self.current_line, self.num_tabs)

        elif self.last_char.isalpha():
            while self.last_char.isalnum():
                identifier_string += self.last_char
                self.last_char = cur_file.read(1)
            if identifier_string == "vector":
                return CToken(Tok.vector, identifier_string, self.current_line, self.num_tabs)
            if identifier_string == "list":
                return CToken(Tok.c_list, identifier_string, self.current_line, self.num_tabs)
            elif identifier_string == "typedef":
                return CToken(Tok.typedef, identifier_string, self.current_line, self.num_tabs)
            elif identifier_string == "struct":
                return CToken(Tok.struct, identifier_string, self.current_line, self.num_tabs)
            else:
                return CToken(Tok.identifier, identifier_string, self.current_line, self.num_tabs)

        elif self.last_char.isdigit():
            while self.last_char.isdigit() or self.last_char == ".":
                identifier_string += self.last_char
                self.last_char = cur_file.read(1)
            return CToken(Tok.constant, identifier_string, self.current_line, self.num_tabs)

        elif not self.last_char:
            return CToken(Tok.eof, "", self.current_line, self.num_tabs)

        identifier_string = self.last_char
        self.last_char = cur_file.read(1)
        return CToken(Tok.char, identifier_string, self.current_line, self.num_tabs)

