#define TAB "    "

// These should be initialized at the start of the program
static char* GlobalOutput;
static int GlobalIndex;

static char* NormalOutput;
static int NormalIndex;

static char* VectorOutput;
static int VectorIndex;

static int NumTabs = 0;

static void add_to_output(char *Output, int *Index, char *Str) {
    int Size = strlen(Str);
    for (int i = 0; i < Size; i++) {
        Output[(*Index)++] = Str[i];
    }
}

#define ADD_TO_VEC(Str) \
    add_to_output(VectorOutput, &VectorIndex, Str)
#define ADD_TO_NORMAL(Str) \
    add_to_output(NormalOutput, &NormalIndex, Str)
#define ADD_TO_GLOBAL(Str) \
    add_to_output(GlobalOutput, &GlobalIndex, Str)

static void add_tabs_to_normal_output() {
    for (int i = 0; i < NumTabs; i++) {
        ADD_TO_NORMAL(TAB);
    }
}


bool log_error(const char *Str, int CurLine) {
    fprintf(stderr, "Error:%d: %s\n", CurLine + 1, Str);
    return false;
}
