from c_token import CToken, Tok
from c_parser import CParser
from output import Output
from c_tokenizer import Tokenizer

from collections import deque
from typing import Deque, TextIO

file_list = ["test3.c"]
source_file_count = 0

while source_file_count < len(file_list):
    cur_file = open(file_list[source_file_count], 'r')
    token_list: Deque[CToken] = deque()
    tokenizer = Tokenizer()
    tokenizer.nexttok(cur_file)
    while (1):
        tok = tokenizer.nexttok(cur_file)
        token_list.append(tok)
        if tok.val == Tok.eof:
            break

    output = Output()
    parser = CParser()
    parser.parse(output, token_list, source_file_count)

    # output to files
    output.output_to_file(source_file_count, cur_file)
    source_file_count += 1
    cur_file.close()

