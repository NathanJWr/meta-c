typedef enum {
    tok_eof = -1,
    tok_identifier = -2,

    tok_vector = -3,
    tok_template = -4,
    tok_typedef = -5,
} token;

char IdentifierStr[100];
static int CurrentLine = 0;
static int LastChar = ' ';

static int gettok() {

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

    if (LastChar == EOF)
        return tok_eof;

    // Otherwise, just return the character as its ascii value.
    int ThisChar = LastChar;
    LastChar = fgetc(SourceFile);
    return ThisChar;
}

static int CurTok;
static int get_next_token() {
    return CurTok = gettok();
}
