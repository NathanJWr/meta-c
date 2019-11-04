from c_token import CToken, Tok
from c_parser import parse
from output import Output
from c_tokenizer import Tokenizer

from collections import deque
from typing import Deque, TextIO

file_list = ["test3.c"]
source_file_count = 0

def output_to_file(output: Output, cur_file: TextIO) -> None:
    global source_file_count

    output_file_name = "__" + cur_file.name
    vector_file_name = "__vector" + str(source_file_count) + ".h"
    output_file = open(output_file_name, 'w')
    vector_file = open(vector_file_name, 'w')

    output_file.write(output.global_out)
    output_file.write(output.normal_out)

    vector_file.write(output.vector_out)

    vector_file.close()
    output_file.close()
    source_file_count += 1


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
    parse(output, token_list, source_file_count)

    # output to files
    output_to_file(output, cur_file)
    cur_file.close()


