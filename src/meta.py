from c_token import CToken, Tok
from c_parser import CParser
from output import Output
from c_tokenizer import Tokenizer
import sys, argparse
import time

from collections import deque
from typing import Deque, TextIO

init_time = time.time()

file_list = []
source_file_count = 0
bounds_checked = False
null_on_free = False

def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", nargs='+', help="Input C files.")
    parser.add_argument("-b", "--bounds-checked", action='store_true', help="Generate bounds checked data structures.")
    parser.add_argument("-n", "--null-on-free", action='store_true', help="Set variables to NULL whenever a free is called.")

    options = parser.parse_args(args)
    return options

options = get_options()
bounds_checked = options.bounds_checked
null_on_free = options.null_on_free
file_list = options.input

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
    parser = CParser(bounds_checked, null_on_free)
    parser.parse(output, token_list, source_file_count)

    # output to files
    output.output_to_file(source_file_count, cur_file)
    source_file_count += 1
    print(source_file_count)
    cur_file.close()

finish_time = time.time()

print("Time taken: " + str(finish_time - init_time) + "s")
