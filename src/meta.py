from token import Token, Tok
from c_parser import parse
from output import Output
from tokenizer import nexttok

from collections import deque
from typing import Union
from typing import Tuple
from typing import Deque


cur_file = open("test.c", 'r')
token_list: Deque[Token] = deque()
nexttok(cur_file)

while (1):
    tok = nexttok(cur_file)
    token_list.append(tok)
    if tok.val == Tok.eof:
        break

output = Output()
parse(output, token_list)
print(output.vector_out)
