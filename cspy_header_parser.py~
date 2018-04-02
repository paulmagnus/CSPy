#------------------------------------------------------------------------------#
# cspy_header_parser.py                                                        #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, and Matthew R. Jenkins '20       #
# Summer 2017                                                                  #
#                                                                              #
# A parser for the language CSPy created using PLY. Contains the grammar rules #
# for the CSPy header file.                                                    #
#------------------------------------------------------------------------------#
import re, sys
from cspy_data_struct import ast

# Precedence table taken from Python documentation Operator precedence table
precedence = (
    ('nonassoc', 'EPSILON'),
    ('left', 'COMMA'),
    ('right', 'RPAREN', 'RBRACKET'),
    ('left', 'LPAREN', 'LBRACKET'))

# Start rule
start = "file"

#------------------------------------------------------------------------------#
# FILE                                                                         #
# The file rule incorporates the entire file. It also contains top level       #
# environment, used for importing.                                             #
#------------------------------------------------------------------------------#
def p_file(p):
    '''file : optdoc importblock declaration_suite'''
    p[0] = ast(p, "FILE", 1, 2, 3)

#------------------------------------------------------------------------------#
# EMPTY                                                                        #
# The empty rule allows for a rule to have an optional component               #
#------------------------------------------------------------------------------#
def p_empty(p):
    '''empty : %prec EPSILON'''
    p[0] = ast(p, "EMPTY")

#------------------------------------------------------------------------------#
# OPTDOC                                                                       #
# The optdoc rule allows for the optional use of docstrings at the top of      #
# the file and at the top of indentation blocks.                               #
#------------------------------------------------------------------------------#
def p_optdoc(p):
    # ''' ... ''' or """ ... """
    '''optdoc : DOCSTRING NL
              | empty'''
    p[0] = ast(p, "DOCSTRING", 1)

#------------------------------------------------------------------------------#
# PYIMPORT                                                                     #
# This family of rules covers the grammar for pyimport statements allowing     #
# for the importing of other python files.                                     #
#                                                                              #
# NOTE: Each imported python file must have a corresponding cspyh file.        #
#------------------------------------------------------------------------------#

def p_importblock(p):
    '''importblock : nonempty_importblock
                   | empty'''
    p[0] = p[1]

def p_nonempty_importblock_single(p):
    '''nonempty_importblock : singleimport'''
    p[0] = p[1]

def p_singleimport(p):
    '''singleimport : pyimport_statement'''
    p[0] = ast(p, "IMPORTBLOCK_SINGLE", 1)

def p_nonempty_importblock_multi(p):
    '''nonempty_importblock : nonempty_importblock singleimport'''
    p[0] = ast(p, "IMPORTBLOCK_MULTI", 1, 2)

def p_pyimport_statement_simple(p):
    # pyimport module
    '''pyimport_statement : PYIMPORT IDENTIFIER NL'''
    p[0] = ast(p, "PYIMPORT_SIMPLE", 2)

def p_pyimport_statement_alias(p):
    # pyimport module as name
    '''pyimport_statement : PYIMPORT IDENTIFIER AS IDENTIFIER NL'''
    p[0] = ast(p, "PYIMPORT_ALIAS", 2, 4)

def p_pyimport_statement_bulk(p):
    # from module pyimport *
    '''pyimport_statement : FROM IDENTIFIER PYIMPORT TIMES NL'''
    p[0] = ast(p, "PYIMPORT_BULK", 2)

def p_pyimport_statement_discrete(p):
    # from module pyimport fn1, fn2...
    '''pyimport_statement : FROM IDENTIFIER PYIMPORT importlist NL'''
    p[0] = ast(p, "PYIMPORT_DISCRETE", 2, 4)

def p_importlist_single(p):
    '''importlist : IDENTIFIER'''
    p[0] = ast(p, "IMPORTLIST_SIMPLE", 1)

def p_importlist_alias(p):
    '''importlist : IDENTIFIER AS IDENTIFIER'''
    p[0] = ast(p, "IMPORTLIST_ALIAS", 1, 3)

def p_importlist_multi(p):
    '''importlist : importlist COMMA importlist'''
    p[0] = ast(p, "IMPORTLIST_MULTI", 1, 3)

#------------------------------------------------------------------------------#
# DECLARATION_SUITE                                                            #
# This rule is simply a container for declaration blocks, used in the file and #
# in class definitions                                                         #
#------------------------------------------------------------------------------#
def p_declaration_suite(p):
    '''declaration_suite : variableblock classblock methodblock'''
    p[0] = ast(p, "DECLARATION_SUITE", 1, 2, 3)

#------------------------------------------------------------------------------#
# VARIABLEBLOCK                                                                #
# This family of rules allow for a block of variable declarations, used at     #
# the top of code blocks, and in the case of file, just below importblock      #
#------------------------------------------------------------------------------#
def p_variableblock(p):
    # :: ... ::
    '''variableblock : COLONCOLON nonempty_variableblock COLONCOLON NL
                     | empty empty'''
    p[0] = p[2]

def p_nonempty_variableblock_single(p):
    # :: x : int ::
    '''nonempty_variableblock : declaration'''
    p[0] = ast(p, "VARIABLEBLOCK_SINGLE", 1)

def p_nonempty_variableblock_multi(p):
    # :: x : int, y : string ::
    '''nonempty_variableblock : nonempty_variableblock COMMA nonempty_variableblock'''
    p[0] = ast(p, "VARIABLEBLOCK_MULTI", 1, 3)

#------------------------------------------------------------------------------#
# DECLARATION                                                                  #
# This rule allows for the declaration of new variables                        #
#------------------------------------------------------------------------------#
def p_declaration_simple(p):
    # x : int
    '''declaration : IDENTIFIER COLON type'''
    p[0] = ast(p, "DECLARATION_SIMPLE", 1, 3)


#------------------------------------------------------------------------------#
# CLASSBLOCK                                                                   #
# These two rules allow for a series of zero or more class definitions         #
#------------------------------------------------------------------------------#
def p_classblock(p):
    '''classblock : class_definition classblock'''
    p[0] = ast(p, "CLASSBLOCK", 1, 2)

def p_classblock_empty(p):
    '''classblock : empty'''
    p[0] = p[1]

#------------------------------------------------------------------------------#
# CLASS DEFINITION                                                             #
# This family of rules allows for the definition of classes                    #
#------------------------------------------------------------------------------#
def p_class_definition(p):
    # class Pet:
    # class Dog extends Pet:
    '''class_definition : CLASS IDENTIFIER opt_extends COLON NL INDENT class_suite DEDENT'''
    p[0] = ast(p, "CLASS_DEFINITION", 2, 3, 7)

def p_class_suite(p):
    '''class_suite : optdoc declaration_suite'''
    p[0] = ast(p, "CLASS_SUITE", 1, 2)

def p_opt_extends(p):
    '''opt_extends : EXTENDS type
                   | empty empty'''
    p[0] = p[2]

#------------------------------------------------------------------------------#
# METHODBLOCK                                                                  #
# These two rules allow for a series of zero or more subroutine definitions,   #
# both inside a class definition and outside                                   #
#------------------------------------------------------------------------------#
def p_methodblock(p):
    '''methodblock : subroutine_definition methodblock'''
    p[0] = ast(p, "METHODBLOCK", 1, 2)

def p_methodblock_empty(p):
    '''methodblock : empty'''
    p[0] = p[1]

#------------------------------------------------------------------------------#
# SUBROUTINE DEFINITION                                                        #
# These rules allow for the definition of subroutines                          #
#------------------------------------------------------------------------------#

# Container rule for subroutines
def p_subroutine_definition(p):
    '''subroutine_definition : function_definition
                             | procedure_definition'''
    p[0] = p[1]

def p_function_definition(p):
    # def add(x : int, y : int) -> int
    '''function_definition : DEF IDENTIFIER LPAREN argumentlist RPAREN ARROW type NL'''
    p[0] = ast(p, "FUNCTION_DEFINITION", 2, 4, 7)

def p_procedure_definition(p):
    # def write(s:string)
    '''procedure_definition : DEF IDENTIFIER LPAREN argumentlist RPAREN NL'''
    p[0] = ast(p, "PROCEDURE_DEFINITION", 2, 4)

#------------------------------------------------------------------------------#
# ARGUMENT LIST                                                                #
# Used in subroutine definitions                                               #
#------------------------------------------------------------------------------#

def p_argumentlist(p):
    '''argumentlist : nonempty_argumentlist COMMA nonempty_defaultlist
                    | nonempty_argumentlist empty empty
                    | empty empty empty'''
    p[0] = ast(p, "ARGUMENTLIST", 1, 3)

def p_argumentlist_default(p):
    '''argumentlist : nonempty_defaultlist empty empty'''
    p[0] = ast(p, "ARGUMENTLIST", 3, 1)

def p_argumentlist_single(p):
    '''nonempty_argumentlist : IDENTIFIER COLON type'''
    p[0] = ast(p, "ARGUMENTLIST_SINGLE", 1, 3)

def p_argumentlist_multi(p):
    '''nonempty_argumentlist : nonempty_argumentlist COMMA nonempty_argumentlist'''
    p[0] = ast(p, "ARGUMENTLIST_MULTI", 1, 3)

def p_defaultlist_multi(p):
    '''nonempty_defaultlist : nonempty_defaultlist COMMA nonempty_defaultlist'''
    p[0] = ast(p, "DEFAULTLIST_MULTI", 1, 3)

def p_defaultlist_single(p):
    '''nonempty_defaultlist : IDENTIFIER COLON QMARK type'''
    p[0] = ast(p, "DEFAULTLIST_SINGLE", 1, 4)

#------------------------------------------------------------------------------#
# TYPE                                                                         #
# This family of rules allows for the use of type names                        #
#------------------------------------------------------------------------------#

def p_type_simple(p):
    '''type : function_type
            | procedure_type
            | tuple_type
            | list_type
            | dictionary_type
            | set_type
            | frozenset_type
            | generator_type
            | IDENTIFIER'''
    p[0] = ast(p, "TYPE", 1)

def p_function_type(p):
    '''function_type : FN LPAREN typelist RPAREN ARROW type'''
    p[0] = ast(p, "FUNCTION_TYPE", 3, 6)

def p_procedure_type(p):
    # proc (string)
    '''procedure_type : PROC LPAREN typelist RPAREN'''
    p[0] = ast(p, "PROCEDURE_TYPE", 3)

def p_typelist(p):
    # int, int, ?string
    '''typelist : nonempty_typelist COMMA nonempty_default_typelist
                | nonempty_typelist empty empty
                | empty empty nonempty_default_typelist
                | empty empty empty'''
    p[0] = ast(p, "TYPELIST", 1, 3)

def p_nonempty_typelist_single(p):
    '''nonempty_typelist : type'''
    p[0] = ast(p, "TYPELIST_SINGLE", 1)

def p_nonempty_typelist_multi(p):
    '''nonempty_typelist : nonempty_typelist COMMA nonempty_typelist'''
    p[0] = ast(p, "TYPELIST_MULTI", 1, 3)

def p_default_typelist_single(p):
    # ?string
    '''nonempty_default_typelist : QMARK type'''
    p[0] = ast(p, "DEFAULT_TYPELIST_SINGLE", 2)

def p_default_typelist_multi(p):
    '''nonempty_default_typelist : nonempty_default_typelist COMMA nonempty_default_typelist'''
    p[0] = ast(p, "DEFAULT_TYPELIST_MULTI", 1, 3)

def p_tuple_type(p):
    '''tuple_type : tupleof
                  | tupleparens'''
    p[0] = p[1]

def p_tupleof(p):
    # tuple of (int * string * int)
    '''tupleof : TUPLE OF LPAREN tuple_typelist RPAREN'''
    p[0] = ast(p, "TUPLE_TYPE", 4)

def p_tupleparens(p):
    # (int * string)
    '''tupleparens : LPAREN tuple_typelist RPAREN'''
    p[0] = ast(p, "TUPLE_TYPE", 2)

def p_tuple_typelist(p):
    '''tuple_typelist : nonempty_tuple_typelist
                      | empty'''
    p[0] = p[1]

def p_nonempty_tuple_typelist_single(p):
    '''nonempty_tuple_typelist : type'''
    p[0] = ast(p, "TUPLE_TYPELIST_SINGLE", 1)

def p_nonempty_tuple_typelist_multi(p):
    '''nonempty_tuple_typelist : nonempty_tuple_typelist TIMES nonempty_tuple_typelist'''
    p[0] = ast(p, "TUPLE_TYPELIST_MULTI", 1, 3)

def p_list_type(p):
    '''list_type : listof
                 | listbracket'''
    p[0] = p[1]

def p_listof(p):
    # list of int
    # list of list of int
    '''listof : LIST OF type'''
    p[0] = ast(p, "LIST_TYPE", 3)

def p_listbracket(p):
    # [int]
    # [[int]]
    '''listbracket : LBRACKET type RBRACKET'''
    p[0] = ast(p, "LIST_TYPE", 2)

def p_set_type(p):
    # set of int
    '''set_type : SET OF type'''
    p[0] = ast(p, "SET_TYPE", 3)

def p_frozenset_type(p):
    # frozenset of int
    '''frozenset_type : FROZENSET OF type'''
    p[0] = ast(p, "FROZENSET_TYPE", 3)

def p_generator_type(p):
    # generator of int
    '''generator_type : GENERATOR OF type'''
    p[0] = ast(p, "GENERATOR_TYPE", 3)

def p_dictionary_type(p):
    # dict of [int|string]
    '''dictionary_type : DICT OF LBRACKET type BITOR type RBRACKET'''
    p[0] = ast(p, "DICTIONARY_TYPE", 4, 6)

#----------------------------ERROR HANDLING------------------------------------#

#------------------------------------------------------------------------------#
# p_error(p:LexToken)                                                          #
#   Displays an error message when parse errors are encountered.               #
#                                                                              #
#   CSPy : Header File SyntaxError                                             #
#   Line NUM, Column NUM                                                       #
#                                                                              #
#   code code error code                                                       #
#             ^^^^^                                                            #
#   If there is an error rule defined in the grammar (see definitions below),  #
#   the parser will attempt to resynchronize itself by finding the next        #
#   terminal that follows the error token in the rule and continue parsing     #
#   input from that point, allowing it to catch more than one synatx error     #
#   in a file. If the error is followed by a nonterminal, or fails             #
#   to encounter the next terminal, the parser will be unable to resynchronize #
#   itself and will either stop parsing or mistakenly identify good code as    #
#   syntax errors.                                                             #
#------------------------------------------------------------------------------#
def p_error(p):
    # Invalid character - Lexer takes care of this error
    if not p:
        return
    
    print >> sys.stderr, "CSPy : Header File SyntaxError"

    # Get the line from the source code
    source = p.lexer.lexdata.split('\n')
    lineno = p.lineno
    line = source[lineno - 1]

    # Assume error occurred on previous line if current line is whitespace
    # Find previous nonwhitespace or noncomment line
    white_space = re.compile('^([ \t]+[#].*)$')
    while (white_space.match(line) or line == '') and lineno != 1:
        lineno = lineno - 1
        line = source[lineno - 1]

    error_length = p.value if (p.type == 'DEDENT' or p.type == 'INDENT') else len(p.value)

    # Find the column of the token in the source code
    if p.type == 'NL':
        col = len(line) + 1
    elif p.type == 'DEDENT' or p.type == 'INDENT':
        col = 1
    else:
        last_nl = p.lexer.lexdata.rfind('\n', 0, p.lexpos)
        if last_nl < 0:
            last_nl = -1
        next_nl = p.lexer.lexdata.find('\n', p.lexpos + error_length,\
                                           len(p.lexer.lexdata))
        if next_nl < 0:
            next_nl = len(p.lexer.lexdata)
        col = p.lexpos - last_nl
    # CITE: Modified from ast.set_column_num method in data_structures.py
    message = "Line " + str(lineno) + ", Column " + str(col) + "\n\n" \
        + line + "\n" + " " * (col - 1) + "^" * (error_length)
    print >> sys.stderr, message

    # Indentation error
    if p.type == 'DEDENT' or p.type == 'INDENT':
        print >> sys.stderr, "IndentationError: outer indentation and unindentation do not match \n"

    if p.type == 'NL':
        print >> sys.stderr, "Unexpected new line."
    exit(1)

#--Variable Blocks and Declarations--------------------------------------------#

# Missing starting or ending '::'
def p_variableblock_error(p):
    '''variableblock : COLONCOLON error COLONCOLON NL'''
    print >> sys.stderr, "Variable declaration invalid syntax.\n"

#--Class Definitions-----------------------------------------------------------#

def p_class_definition_error(p):
    '''class_definition : CLASS IDENTIFIER opt_extends error NL INDENT class_suite DEDENT
                        | CLASS IDENTIFIER opt_extends COLON NL INDENT error DEDENT'''
    print >> sys.stderr, "Class definition invalid syntax.\n"

#--Function and Procedure Definitions------------------------------------------#

def p_function_definition_error(p):
    '''function_definition : DEF error LPAREN argumentlist RPAREN ARROW type
                           | DEF IDENTIFIER LPAREN argumentlist error ARROW type
                           | DEF IDENTIFIER LPAREN argumentlist RPAREN ARROW error'''
    print >> sys.stderr, "Function definition invalid syntax.\n"

def p_procedure_definition_error(p):
    '''procedure_definition : DEF error LPAREN argumentlist RPAREN
                            | DEF IDENTIFIER LPAREN argumentlist error'''
    print >> sys.stderr, "Procedure definition invalid syntax.\n"

def p_argumnetlist_single_error(p):
    '''nonempty_argumentlist : error COLON type'''
    print >> sys.stderr, "Invalid identifier.\n"

#--TYPES-----------------------------------------------------------------------#

def p_function_type_error(p):
    '''function_type : FN LPAREN error RPAREN ARROW type'''
    print >> sys.stderr, "Type list invalid syntax.\n"

def p_procedure_type_error(p):
    '''procedure_type : PROC LPAREN error RPAREN'''
    print >> sys.stderr, "Type list invalid syntax.\n"

def p_dictionary_type_error(p):
    '''dictionary_type : DICT error LBRACKET type BITOR type RBRACKET
                       | DICT OF LBRACKET error BITOR type RBRACKET
                       | DICT OF LBRACKET type BITOR error RBRACKET'''
    print >> sys.stderr, "Dictionary type declaration invalid syntax.\n"