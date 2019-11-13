from c_token import CToken, Tok
from c_parser import CParser
from output import Output
from c_tokenizer import Tokenizer
import getopt, sys
import time

from collections import deque
from typing import Deque, TextIO

init_time = time.time()

file_list = ["test_list.c"]
source_file_count = 0
bounds_checked = False

fullCmdArguments = sys.argv
argumentList = fullCmdArguments[1:]

unixOptions = "hvb"
gnuOptions = ["help", "verbose", "bounds_checked"]
try:
    arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

for current_arg, current_val in arguments:
    if current_arg in ("-v", "--verbose"):
        print("verbose mode")
    elif current_arg in ("-h", "--help"):
        print("displaying help")
    elif current_arg in ("-b", "--bounds_checked"):
        bounds_checked = True

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
    parser = CParser(bounds_checked)
    parser.parse(output, token_list, source_file_count)

    # output to files
    output.output_to_file(source_file_count, cur_file)
    source_file_count += 1
    print(source_file_count)
    cur_file.close()

finish_time = time.time()

print("Time taken: " + str(finish_time - init_time) + "s")
