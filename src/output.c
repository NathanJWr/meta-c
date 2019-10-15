#define TAB "    "

// These should be initialized at the start of the program
static char* GlobalOutput;
static int GlobalIndex;

static char* NormalOutput;
static int NormalIndex;

static char* VectorOutput;
static int VectorIndex;

static int NumTabs = 0;

static void add_to_normal_output(char* str) {
    for (int i = 0; i < strlen(str); i++) {
        NormalOutput[NormalIndex++] = str[i];
    }
}

static void add_to_global_output(char* str) {
    for (int i = 0; i < strlen(str); i++) {
        GlobalOutput[GlobalIndex++] = str[i];
    }
}

static void add_to_vector_output(char *str) {
    for (int i = 0; i < strlen(str); i++) {
        VectorOutput[VectorIndex++] = str[i];
    }
}

static void add_tabs_to_normal_output() {
    for (int i = 0; i < NumTabs; i++) {
        add_to_normal_output(TAB);
    }
}

static void add_to_output(char *Output, int *Index, char *Str) {
    int Size = strlen(Str);
    for (int i = 0; i < Size; i++) {
        Output[(*Index)++] = Str[i];
    }
}

bool log_error(const char *Str, int CurLine) {
    fprintf(stderr, "Error:%d: %s\n", CurLine + 1, Str);
    return false;
}
