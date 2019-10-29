#include "c_parser.h"
static int
gettok() {
    if (LastChar == '\n')
        CurrentLine++;
    if (LastChar == '{')
        NumTabs++;
    if (LastChar == '}')
        NumTabs--;

    if (isalpha(LastChar)) { // identifier: [a-zA-Z][a-zA-Z0-9]*
        // Clear the old IdentifierStr
        memset(&IdentifierStr[0], 0, sizeof(IdentifierStr));

        IdentifierStr[0] = LastChar;
        int i = 1;
        while (isalnum((LastChar = fgetc(SourceFile)))) {
            IdentifierStr[i++] = LastChar;
        }

        if (strcmp(IdentifierStr, "vector") == 0) {
			return tok_vector;
		}
        if (strcmp(IdentifierStr, "typedef") == 0) {
            return tok_typedef;
        }

        return tok_identifier;
    }
    if (isdigit(LastChar)) {
        char NumStr[100] = {0};
        for (int i = 0; i < 100; i++) {
            NumStr[i] = LastChar;	
            LastChar = fgetc(SourceFile);
            if (!isdigit(LastChar) || LastChar != '.') {
                break;
            }
        }
        strcpy(IdentifierStr, NumStr);
        return tok_constant;
    }

    if (LastChar == EOF)
        return tok_eof;

    // Otherwise, just return the character as its ascii value.
    int ThisChar = LastChar;
    LastChar = fgetc(SourceFile);
    return ThisChar;
}

static int
get_next_token() {
    return CurTok = gettok();
}

static void
parse_typedef() {
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
