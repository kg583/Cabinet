grammar Cabinet;


cabinet: NEWLINE* procDecl* EOF ;


// Procedures
procDecl: type=WORD name=WORD procSpec NEWLINE+ ;

procSpec: singleSpec | compoundSpec ;

singleSpec
    : (WORD time=NUMBER)? keyword=WORD block=procBlock    # runSpec
    | keyword=WORD block=usesBlock                        # usesSpec
    | keyword=WORD advancement=advancementSpec block=json # jsonSpec
    ;

advancementSpec: WORD | resource ;

compoundSpec: L_BRACE NEWLINE+ (NEWLINE* singleSpec NEWLINE*)+ R_BRACE ;


usesBlock: L_BRACE useDecl* R_BRACE ;

useDecl: score criterion NEWLINE+ ;


procBlock: L_BRACE NEWLINE+ procLine+ R_BRACE ;

procLine
    : cabinetLine NEWLINE+
    | command NEWLINE+
    ;

grouping: L_BRACKET atom atom atom? R_BRACKET ;

command: (atom | grouping | procBlock)+ ;


// Cabinet extensions
cabinetLine
    : cabinetAssign
    ;


cabinetAssign: (score | variable) operation cabinetExpr ;

cabinetExpr
    : cabinetGet
    | atom
    | L_PAREN cabinetExpr R_PAREN
    | cabinetExpr (STAR | SLASH | PERCENT) cabinetExpr
    | cabinetExpr (PLUS | MINUS ) cabinetExpr
    ;

cabinetGet
    : selector COLON nbtPath
    | selector COLON COLON WORD
    | selector L_BRACKET WORD R_BRACKET
    ;


// Atoms
atom
    : BANG
    | TILDE | CARET
    | NUMBER
    | STRING
    | WORD
    | comparison
    | criterion
    | nbt
    | nbtPath
    | operation
    | resource
    | score
    | selector
    | variable
    ;


json
    : jsonArray
    | jsonObj
    ;

jsonArray: L_BRACKET NEWLINE* (jsonValue (COMMA NEWLINE* jsonValue)*)? NEWLINE* R_BRACKET ;

jsonObj: L_BRACE NEWLINE* (jsonPair (COMMA NEWLINE* jsonPair)*)? NEWLINE* R_BRACE ;

jsonPair: STRING COLON jsonValue ;

jsonValue
    : NUMBER
    | STRING
    | WORD
    | jsonArray
    | jsonObj
    ;


nbt
    : nbtArray
    | nbtObj
    ;

nbtArray: L_BRACKET NEWLINE* ((WORD SEMI)? nbtValue (COMMA NEWLINE* nbtValue)*)? NEWLINE* R_BRACKET ;

nbtObj: L_BRACE NEWLINE* (nbtPair (COMMA NEWLINE* nbtPair)*)? R_BRACE ;

nbtPair: (STRING | WORD) COLON nbtValue ;

nbtValue
    : NUMBER
    | STRING
    | WORD
    | nbtObj
    | nbtArray
    ;

nbtPath: (STRING | WORD) nbt? (DOT nbtPath)? ;


comparison: EQUAL | GREATER | LESS | '>=' | '<=' ;

criterion: WORD (DOT WORD (COLON WORD DOT WORD)?)? ;

operation: EQUAL | GREATER | LESS | '><' | '+=' | '-=' | '*=' | '/=' | '%=' ;

resource: WORD COLON WORD ;

score : HASH? WORD ;

variable : DOLLAR  L_PAREN WORD R_PAREN ;


selector: ARROBA tag (L_BRACKET (selectorClause (COMMA selectorClause)*)? R_BRACKET)? ;

selectorClause: type=WORD EQUAL negation=BANG? value=atom ;

tag: COLON? COLON? WORD ;


// Strings
STRING : '"' (ESC | SAFECODEPOINT)* '"' ;

fragment ESC : '\\' (["\\/bfnrt] | UNICODE) ;
fragment UNICODE  : 'u' HEX HEX HEX HEX ;
fragment HEX : [0-9a-fA-F] ;
fragment SAFECODEPOINT : ~ ["\\\u0000-\u001F] ;


// Numbers
NUMBER : MINUS? DIGIT+ (DOT DIGIT+)? [bdslBDSLmt]? ;

fragment DIGIT : [0-9] ;


// Grouping
L_BRACE : '{' ;
R_BRACE : '}' ;
L_BRACKET : '[' ;
R_BRACKET : ']' ;
L_PAREN : '(' ;
R_PAREN : ')' ;


// Atoms
AMP : '&' ;
ARROBA : '@' ;
BANG : '!' ;
CARET : '^' ;
COLON : ':' ;
COMMA : ',' ;
DOLLAR : '$' ;
DOT : '.';
EQUAL : '=' ;
GREATER : '>' ;
HASH : '#' ;
LESS : '<' ;
MINUS : '-';
PERCENT : '%' ;
PLUS : '+' ;
SEMI : ';' ;
SLASH : '/' ;
STAR : '*' ;
TILDE : '~' ;
VERT : '|' ;

WORD : [+\-._A-Za-z0-9] [+\-./_A-Za-z0-9]* ;
SYMBOL : [%*+\-/<=>^~] ;


// Fluff
COMMENT : '# ' ~[\r\n\f]* -> channel(HIDDEN);
NEWLINE : [\r\n]+ ;
WS : [ \t\f]+ -> skip;
