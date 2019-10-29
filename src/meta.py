from c_token import CToken, Tok
from c_parser import parse
from output import Output
from c_tokenizer import Tokenizer

from collections import deque
from typing import Deque


cur_file = open("test.c", 'r')
source_file_count = 0
token_list: Deque[CToken] = deque()
tokenizer = Tokenizer()
tokenizer.nexttok(cur_file)


while (1):
    tok = tokenizer.nexttok(cur_file)
    token_list.append(tok)
    if tok.val == Tok.eof:
        break

output = Output()
parse(output, token_list)

# output to files
output_file_name = "__" + cur_file.name
vector_file_name = "__vector" + str(source_file_count) + ".h"
output_file = open(output_file_name, 'w')
vector_file = open(vector_file_name, 'w')

output_file.write(output.global_out)
output_file.write(output.normal_out)

vector_file.write(output.vector_out)

vector_file.close()
output_file.close()


