#ifndef VECTOR_H_
#define VECTOR_H_
static types VecTypes = { 0 };
static variables VecVariables = { 0 };
static int CurVecFile = -1;

static char* generate_vector(char* Type);
static bool parse_vector_function();
static bool parse_vector_var(char* VarName);
static char* get_vector_file_name();
static bool parse_vector();
static void empty_vec_types();

#endif

