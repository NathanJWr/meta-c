from token import Token, Tok
def log_error(token: Token, error: str) -> None:
    print(f'{token.line_num}' + ": " + error)
