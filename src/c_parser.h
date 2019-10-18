#ifndef C_PARSER_H_
#define C_PARSER_H_
typedef enum {
    tok_eof = -1,
    tok_identifier = -2,

    tok_vector = -3,
    tok_template = -4,
    tok_typedef = -5,
	tok_constant = -6,
} token;

char IdentifierStr[100];
static int CurrentLine = 0;
static int LastChar = ' ';

static int CurTok;

static int gettok();
static int get_next_token();
static void parse_typedef();

#endif

