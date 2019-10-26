from c_token import CToken, Tok
def log_error(token: CToken, error: str) -> None:
    print(f'{token.line_num}' + ": " + error)
