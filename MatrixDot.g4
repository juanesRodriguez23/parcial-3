grammar MatrixDot;

options { language = Python3; }

@header {
# encoding: utf-8
}

prog:   stat* EOF ;

stat:   matrix_decl ';'
    |   assign_stmt ';'
    |   expr_stmt ';'
    |   print_stmt ';'
    ;

matrix_decl
    : 'matrix' ID '=' matrix_literal
    ;

assign_stmt
    : ID '=' expr
    ;

expr_stmt
    : expr
    ;

print_stmt
    : 'print' '(' expr ')'
    ;

expr
    : function_call
    | matrix_literal
    | ID
    | NUMBER
    ;

function_call
    : 'dot' '(' expr ',' expr ')'
    | 'matmul' '(' expr ',' expr ')'
    ;

matrix_literal
    : '[' row_list? ']'
    ;

row_list
    : row (',' row)*
    ;

row
    : '[' number_list? ']'
    ;

number_list
    : NUMBER (',' NUMBER)*
    ;

ID      : [a-zA-Z_] [a-zA-Z0-9_]* ;
NUMBER  : ('-'? DIGIT+ ('.' DIGIT+)? ) ;
fragment DIGIT : [0-9] ;

WS      : [ \t\r\n]+ -> skip ;
COMMENT : '/*' .*? '*/' -> skip ;
LINE_COMMENT : '//' ~[\r\n]* -> skip ;
