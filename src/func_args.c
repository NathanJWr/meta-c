typedef struct _func_call_args { 
    char* Arg;

    struct _func_call_args *Next;
} func_call_args;

static void get_func_arg(char* Arg) {
    while (1) {
        if (CurTok == ',')
            return;
        if (isspace(CurTok))
            return;
        if (CurTok == ')')
            return;
            
        if (CurTok == tok_identifier) {
            strcat(Arg, IdentifierStr);
        } else {
            int Len = strlen(Arg);
            Arg[Len] = CurTok;
        }
        get_next_token();
    }
}

static void free_func_call_args(func_call_args Args) {
    func_call_args *Iterator = &Args;

    // The first Node doesn't have to free the func_call_args
    // struct because it was allocated on the stack
    free(Iterator->Arg);
    Iterator = Iterator->Next;
    while (Iterator != NULL) {
        free(Iterator->Arg);
        func_call_args *Temp = Iterator->Next;
        free(Iterator);
        Iterator = Temp;
    }
}
static func_call_args get_func_args() {
    func_call_args FuncArgs = { 0 };

    func_call_args* Iterator = &FuncArgs;
    while (CurTok != ')') {

        while (CurTok == ',' || isspace(CurTok))
            get_next_token();

        char Arg[100] = { 0 };
        get_func_arg(Arg);

        if (FuncArgs.Arg == NULL) {
            FuncArgs.Arg = malloc(strlen(Arg) * sizeof(char));
            strcpy(FuncArgs.Arg, Arg);
            continue;
        } else {
            func_call_args *Next = malloc(sizeof(func_call_args));
            Next->Arg = malloc(strlen(Arg) * sizeof(char));

            strcpy(Next->Arg, Arg);

            Next->Next = NULL;

            Iterator->Next = Next;
        }

        Iterator = Iterator->Next;
    }

    return FuncArgs;
}

static void output_remaining_func_line() {
    // If you've already hit the end of the function args
    if (CurTok == ')') {
        NormalOutput[NormalIndex++] = (char) CurTok;
        return;
    }

    // Normal outputting
    do {
        get_next_token();
        if (CurTok == tok_identifier) {
            ADD_TO_NORMAL(IdentifierStr);
        } else {
            NormalOutput[NormalIndex++] = (char) CurTok;
        }
    } while (CurTok != ')');
}

