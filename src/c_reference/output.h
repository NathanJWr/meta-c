#ifndef OUTPUT_H_
#define OUTPUT_H_

#define TAB "    "
// These should be initialized at the start of the program
static char* GlobalOutput;
static int GlobalIndex;

static char* NormalOutput;
static int NormalIndex;

static char* VectorOutput;
static int VectorIndex;

static int NumTabs = 0;

static void add_to_output(char *Output, int *Index, char *Str);
#define ADD_TO_VEC(Str) \
    add_to_output(VectorOutput, &VectorIndex, Str)
#define ADD_TO_NORMAL(Str) \
    add_to_output(NormalOutput, &NormalIndex, Str)
#define ADD_TO_GLOBAL(Str) \
    add_to_output(GlobalOutput, &GlobalIndex, Str)
static void add_tabs_to_normal_output();
static bool log_error(const char *Str, int CurLine);

#endif

