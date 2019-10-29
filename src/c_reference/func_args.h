#ifndef FUNC_ARGS_H_
#define FUNC_ARGS_H_
typedef struct _func_call_args { 
    char* Arg;

    struct _func_call_args *Next;
} func_call_args;

static void get_func_arg(char* Arg);
static void free_func_call_args(func_call_args Args);
static func_call_args get_func_args();
static void output_remaining_func_line();
#endif

