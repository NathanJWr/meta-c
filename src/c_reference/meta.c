#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#define ARRAYSIZE(Array) \
	((int)(sizeof(Array)/sizeof(Array[0])))
FILE *SourceFile;
static int SourceFileCount = 0;
#include "output.c"
#include "c_parser.c"
#include "lists.c"
#include "func_args.c"
#include "vector.c"

#define OutputBufferSize 20000
static void output_to_file(char* Src) {
	char OutputName[100] = { 0 };
	strcat(OutputName, "__");
	strcat(OutputName, Src);

	FILE *OutFile = fopen(OutputName, "w");
	fwrite(GlobalOutput, sizeof(char), strlen(GlobalOutput) * sizeof(char), OutFile);
	fwrite(NormalOutput, sizeof(char), strlen(NormalOutput) * sizeof(char), OutFile);
	fclose(OutFile);

	memset(GlobalOutput, 0, OutputBufferSize * sizeof(char));
	memset(NormalOutput, 0, OutputBufferSize * sizeof(char));
	GlobalIndex = 0;
	NormalIndex = 0;

    // Output vector stuff to a file
    char* VecOutName = get_vector_file_name();

    FILE *VecFile = fopen(VecOutName, "w");
    free(VecOutName);
    fwrite(VectorOutput, sizeof(char), strlen(VectorOutput) * sizeof(char), VecFile);
	memset(VectorOutput, 0, OutputBufferSize * sizeof(char));
    VectorIndex = 0;
	fclose(VecFile);
}


static bool
tracked_var(char *IdentifierStr) {
    if (var_in_list(&VecVariables, IdentifierStr)) {
        parse_vector_var(IdentifierStr);
        return true;
    }
    return false;
}

int main() {
	char *SourceList[] = { "test3.c"};
	printf("%d\n", ARRAYSIZE(SourceList));
    SourceFile = fopen(SourceList[SourceFileCount], "r");
    GlobalOutput = (char *) calloc(OutputBufferSize, sizeof(char));
    GlobalIndex = 0;

    NormalOutput = (char *) calloc(OutputBufferSize, sizeof(char));
    NormalIndex = 0;

    VectorOutput = (char *) calloc(OutputBufferSize, sizeof(char));
    VectorIndex = 0;
    get_next_token();

    bool Running = true;
    while (Running) {
        get_next_token();

        switch (CurTok) {
        case tok_vector:
            if (!parse_vector())
                exit(1);
            break;
        case tok_typedef:
            parse_typedef();
            break;
        case tok_identifier:
            if (!tracked_var(IdentifierStr)) {
                ADD_TO_NORMAL(IdentifierStr);
            }
            break;
        case tok_eof:
			output_to_file(SourceList[SourceFileCount]);
            empty_vec_types();
			fclose(SourceFile);
			if (SourceFileCount < ARRAYSIZE(SourceList) - 1) {
				SourceFileCount++;
    			SourceFile = fopen(SourceList[SourceFileCount], "r");
				LastChar = ' ';
				get_next_token();
			} else {
            	Running = false;
			}
            break;
        case tok_constant:
            ADD_TO_NORMAL(IdentifierStr);
            break;
        default:
            NormalOutput[NormalIndex++] = (char) CurTok;
            break;
        }
    }


}
