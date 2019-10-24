from token import Token, Tok
last_char: str = ' '
current_line = 1
num_tabs = 0
cur_tok: Token

def nexttok(cur_file) -> Token:
    global cur_tok
    cur_tok = gettok(cur_file)
    return cur_tok

def gettok(cur_file) -> Token:
    global last_char, current_line, num_tabs 
    this_char: str

    identifier_string = ""
    if last_char == "\n":
        current_line += 1

    elif last_char == "{":
        num_tabs += 1

    elif last_char == "}":
        num_tabs -= 1
        identifier_string = last_char
        last_char = cur_file.read(1)
        return Token(Tok.end_bracket, "}", current_line)

    elif last_char == ";":
        identifier_string = last_char
        last_char = cur_file.read(1)
        return Token(Tok.semicolon, identifier_string, current_line)

    elif last_char.isalpha():
        while last_char.isalnum():
            identifier_string += last_char
            last_char = cur_file.read(1)
        if identifier_string == "vector":
            return Token(Tok.vector, identifier_string, current_line)
        elif identifier_string == "typedef":
            return Token(Tok.typedef, identifier_string, current_line)
        else:
            return Token(Tok.identifier, identifier_string, current_line)

    elif last_char.isdigit():
        while last_char.isdigit() or last_char == ".":
            identifier_string += last_char
            last_char = cur_file.read(1)
        return Token(Tok.constant, identifier_string, current_line)


    elif not last_char:
        return Token(Tok.eof, "", current_line)

    identifier_string = last_char
    last_char = cur_file.read(1)
    return Token(Tok.char, identifier_string, current_line)
    

