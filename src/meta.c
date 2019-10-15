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

static void parse_typedef() {
    get_next_token(); // Eat 'typedef'

    while (CurTok != tok_identifier) {
        get_next_token();
    }

    if (strcmp(IdentifierStr, "struct") == 0) {
        ADD_TO_GLOBAL("typedef ");
        ADD_TO_GLOBAL(IdentifierStr);

        while (CurTok != '}') {
            get_next_token();
            if (CurTok == tok_identifier) {
                ADD_TO_GLOBAL(IdentifierStr);
            } else {
                GlobalOutput[GlobalIndex++] = (char) CurTok;
            }
        }
        while (CurTok != ';') {
            get_next_token();
            if (CurTok == tok_identifier) {
                ADD_TO_GLOBAL(IdentifierStr);
            } else {
                GlobalOutput[GlobalIndex++] = (char) CurTok;
            }
        }
        get_next_token(); // Eat newline.
        GlobalOutput[GlobalIndex++] = '\n';
    }
}

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

int main() {
	char *SourceList[] = { "test.c",
						   "test2.c",};
    SourceFile = fopen(SourceList[SourceFileCount], "r");
    GlobalOutput = (char *) malloc(OutputBufferSize * sizeof(char));
    GlobalIndex = 0;

    NormalOutput = (char *) malloc(OutputBufferSize * sizeof(char));
    NormalIndex = 0;

    VectorOutput = (char *) malloc(OutputBufferSize * sizeof(char));
    VectorIndex = 0;

    // Insert the correct includes for vector code to
    // do stuff like malloc
    ADD_TO_GLOBAL("#include <stdlib.h>\n");

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
            ADD_TO_NORMAL(IdentifierStr);
            break;
        case tok_eof:
			printf("%d", ARRAYSIZE(SourceList));
			output_to_file(SourceList[SourceFileCount]);
            empty_vec_types();
			fclose(SourceFile);
			if (SourceFileCount < 1) {
				SourceFileCount++;
    			SourceFile = fopen(SourceList[SourceFileCount], "r");
				LastChar = ' ';
				get_next_token();
			} else {
            	Running = false;
			}
            break;
        default:
            NormalOutput[NormalIndex++] = (char) CurTok;
            break;
        }
    }


}
