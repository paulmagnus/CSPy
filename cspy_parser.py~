#------------------------------------------------------------------------------#
# cspy_parser.py                                                               #
#                                                                              #
# Originally written by Alex Dennis '18 and Eric Collins '17                   #
# Summer 2015                                                                  #
#                                                                              #
# Revised and edited by Lyndsay LaBarge '17 and Maya Montgomery '18            #
# Summer 2016                                                                  #
#                                                                              #
# Revised and edited by Paul Magnus '18, Ines Ayara and Matthew R. Jenkins '20 #
# Summer 2017                                                                  #
#                                                                              #
# A parser for the language CSPy created using PLY. Contains the grammar rules #
# for the language.                                                            #
#------------------------------------------------------------------------------#

# PYTHON MODULES
import re, sys

# LOCAL FILES
from cspy_data_struct import ast

################################################################################
# WARNING: Context-free gramar rules are defined in the docstring of each      #
# function. Changing the docstrings will change how this program functions.    #
################################################################################

# Precendence table taken from Python documentation Operator precendence table
precedence = (
    ('nonassoc', 'EPSILON'),
    ('nonassoc', 'error'),
    ('left','COMMA'),
    ('left', 'LAMBDA'),
    ('left', 'TERNARY'),
    ('left','BOOLOR', 'OR'),
    ('left', 'BOOLAND', 'AND'),
    ('right', 'BOOLNOT'),
    ('nonassoc', 'EQUALTO', 'REQUALTO', 'NEQUALTO', 'LT', 'LE', 'GT', 
                 'GE', 'IN', 'NOTIN', 'IS', 'ISNOT'),
    ('left', 'BITOR'),
    ('left', 'BITXOR'),
    ('left', 'BITAND'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO', 'INTDIV'),
    ('right', 'UMINUS', 'UPLUS', 'BITINVERT'),
    ('right', 'POW'),
    ('right', 'RPAREN', 'RBRACKET'),  
    ('left', 'LPAREN', 'LBRACKET', 'DOT'))


# Start rule
start = "file"

#------------------------------------------------------------------------------#
# FILE                                                                         #
# The file rule incorporates the entire file. It also contains the top level   #
# environment, used for importing.                                             #
#------------------------------------------------------------------------------#
def p_file(p):
    '''file : optdoc importblock declaration_suite nonempty_block
            | optdoc importblock declaration_suite empty'''
    p[0] = ast(p, "FILE", 1, 2, 3, 4)
   

#------------------------------------------------------------------------------#
# EMPTY                                                                        #
# The empty rule allows for a rule to have an optional component               #
#------------------------------------------------------------------------------#
def p_empty(p):
    '''empty : %prec EPSILON'''
    p[0] = ast(p, "EMPTY")


#------------------------------------------------------------------------------#
# OPTDOC                                                                       #
# The optdoc rule allows for the optional use of docstrings at the top of the  #
# file and at the top of indentation blocks.                                   #
#------------------------------------------------------------------------------#
def p_optdoc(p):
    # ''' ... ''' or """...."""
    '''optdoc : DOCSTRING NL
              | empty'''
    p[0] = ast(p, "DOCSTRING", 1)

#------------------------------------------------------------------------------#
# IMPORT                                                                       #
# This family of rules covers the grammar for import statements.               #
# NOTE: This grammar has NOT been updated to conform to the new import model   #
#       described in the importing file.                                       #
#------------------------------------------------------------------------------#

def p_importblock(p):
    '''importblock : nonempty_importblock
                   | empty'''
    p[0] = p[1]

def p_nonempty_importblock_single(p):
    '''nonempty_importblock : singleimport'''
    p[0] = p[1]

def p_singleimport(p):
    '''singleimport : import_statement
                    | pyimport_statement'''
    p[0] = ast(p, "IMPORTBLOCK_SINGLE", 1)

def p_nonempty_importblock_multi(p):
    '''nonempty_importblock : nonempty_importblock singleimport'''
    p[0] = ast(p, "IMPORTBLOCK_MULTI", 1, 2)

def p_import_statement_simple(p):
    # import module
    '''import_statement : IMPORT IDENTIFIER NL'''
    p[0] = ast(p, "IMPORT_SIMPLE", 2)

   
def p_import_statement_alias(p):
    # import module as name
    '''import_statement : IMPORT IDENTIFIER AS IDENTIFIER NL'''
    p[0] = ast(p, "IMPORT_ALIAS", 2, 4)

   
def p_import_statement_bulk(p):
    # from module import *
    '''import_statement : FROM IDENTIFIER IMPORT TIMES NL'''
    p[0] = ast(p, "IMPORT_BULK", 2)
  
def p_import_statement_discrete(p):
    # from module import fn1, fn2....
    '''import_statement : FROM IDENTIFIER IMPORT importlist NL'''
    p[0] = ast(p, "IMPORT_DISCRETE", 2, 4)

def p_importlist_simple(p):
    '''importlist : IDENTIFIER'''
    p[0] = ast(p, "IMPORTLIST_SIMPLE", 1)
    
def p_importlist_alias(p):
    '''importlist : IDENTIFIER AS IDENTIFIER'''
    p[0] = ast(p, "IMPORTLIST_ALIAS", 1, 3)
    
def p_importlist_multi(p):
    '''importlist : importlist COMMA importlist'''
    p[0] = ast(p, "IMPORTLIST_MULTI", 1, 3)

#------------------------------------------------------------------------------#
# PYIMPORT                                                                     #
# pyimport - Imports from python                                               #
# Importing from a python file requires an associated cspyh file that declares #
# all used types                                                               #
#------------------------------------------------------------------------------#

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
    p[0] = ast(p,"PYIMPORT_DISCRETE", 2, 4)

#------------------------------------------------------------------------------#
# DECLARATION_SUITE                                                            #
# This rule is simply a container for declaration blocks, used in the file and #
# in class definitions                                                         #
#------------------------------------------------------------------------------#

def p_declaration_suite(p):
    '''declaration_suite : variableblock classblock methodblock'''
    p[0] = ast(p, "DECLARATION_SUITE", 1, 2, 3)

def p_declaration_suite_empty(p):
    # all empty
    '''declaration_suite : PASS NL'''
    p[0] = ast(p, "DECLARATION_SUITE_PASS", 1)
   

#------------------------------------------------------------------------------#
# VARIABLEBLOCK                                                                #
# This family of rules allow for a block of variable declarations, used at the #
# top of code blocks, and in the case of file, just below importblock          #
#------------------------------------------------------------------------------#

def p_variableblock(p):
    # :: ... ::
    '''variableblock : COLONCOLON nonempty_variableblock COLONCOLON NL
                     | empty empty'''
    p[0] = p[2]

def p_nonempty_variableblock_single(p):
    # :: x:int ::
    '''nonempty_variableblock : declaration'''
    p[0] = ast(p, "VARIABLEBLOCK_SINGLE", 1)

   
def p_nonempty_variableblock_multi(p):
    # :: x:int, y:string ::
    '''nonempty_variableblock : nonempty_variableblock COMMA nonempty_variableblock'''
    p[0] = ast(p, "VARIABLEBLOCK_MULTI", 1, 3)

#------------------------------------------------------------------------------#
# DECLARATION                                                                  #
# These two rules allow for the declaration of new variables                   #
#------------------------------------------------------------------------------#

def p_declaration_simple(p):  
    # x:int
    '''declaration : IDENTIFIER COLON type'''
    p[0] = ast(p, "DECLARATION_SIMPLE", 1, 3)

def p_declaration_initialize(p):
    # y:string = "Hello World"
    '''declaration : IDENTIFIER COLON type EQUALS expression'''
    p[0] = ast(p, "DECLARATION_INITIALIZE", 1, 3, 5)

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

#-----------------------------------------------------------------------------#
# METHODBLOCK                                                                 #
# These two rules allow for a series of zero or more subroutine definitions,  #
# both inside a class definition and outside                                  #
#-----------------------------------------------------------------------------#
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
    # def add(x:int, y:int) -> int
    '''function_definition : DEF IDENTIFIER LPAREN argumentlist RPAREN ARROW type COLON suite'''
    p[0] = ast(p, "FUNCTION_DEFINITION", 2, 4, 7, 9)

def p_procedure_definition(p):
    # def write(s:string)
    '''procedure_definition : DEF IDENTIFIER LPAREN argumentlist RPAREN COLON suite'''
    p[0] = ast(p, "PROCEDURE_DEFINITION", 2, 4, 7)

#------------------------------------------------------------------------------#
# ARGUMENT LIST                                                                #
# Used in subroutine definitions and function and procedure literals.          #
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
    '''nonempty_defaultlist : IDENTIFIER COLON type EQUALS expression'''
    p[0] = ast(p, "DEFAULTLIST_SINGLE", 1, 3, 5)

#------------------------------------------------------------------------------#
# SUITE                                                                        #
# These rules allow for code indentation blocks other than class suites.       #
# Allows for docstrings                                                        #
#------------------------------------------------------------------------------#
def p_suite_block(p):
    '''suite : NL INDENT optdoc block DEDENT'''
    p[0] = ast(p, "SUITE_BLOCK", 3, 4)
   
def p_suite_inline(p):
    '''suite : statement_simple NL'''
    p[0] = ast(p, "SUITE_INLINE", 1)


#------------------------------------------------------------------------------#
# BLOCK                                                                        #
# A series of statements, used inside indentation blocks. Limits constructs    #
# like loops and conditionals from defining subroutines and classes            #
#------------------------------------------------------------------------------#
def p_block(p):
    '''block : variableblock nonempty_block'''
    p[0] = ast(p, "BLOCK_WITH_ENVIRONMENT", 1, 2)


   
def p_nonempty_block(p):
    '''nonempty_block : statement_complex empty
                      | statement_complex nonempty_block'''
    p[0] = ast(p,"BLOCK", 1, 2)

    
#------------------------------------------------------------------------------#
# STATEMENT                                                                    #
# A family of rules allowing for the use of imperative statements, such as     #
# loops,conditionals, assignments, function calls, and exception handling.     #
#------------------------------------------------------------------------------#

def p_statement_complex(p):
    '''statement_complex : loop
                         | conditional
                         | try_except
                         | statement_multi NL
                         | statement_multi SEMICOLON NL'''
    p[0] = p[1]
    
def p_statement_multi(p):
    '''statement_multi : statement_multi SEMICOLON statement_simple'''
    p[0] = ast(p, "STATEMENT_MULTI", 1, 3)

def p_statement_single(p):
    '''statement_multi : statement_simple'''
    p[0] = p[1]

def p_statement_simple(p):
    '''statement_simple : assignment
                        | procedure_call
                        | return
                        | assert
                        | yield
                        | CONTINUE
                        | BREAK
                        | PASS
                        | raise
                        | delete '''
    p[0] = ast(p, "STATEMENT_SINGLE", 1) 

def p_raise(p):
    '''raise : RAISE IDENTIFIER
             | RAISE function_call
             | RAISE empty'''
    p[0] = ast(p,"RAISE", 2)

def p_delete(p):
    '''delete : DEL expression'''
    p[0] = ast(p, "DELETE", 2)

#------------------------------------------------------------------------------#
# LOOPS                                                                        #
# This family of rules allows for the parsing of loop constructs               #
#------------------------------------------------------------------------------#
def p_loop(p):
    '''loop : while_loop
            | for_loop'''
    p[0] = p[1]


def p_while(p):
    # while x != y:
    '''while_loop : WHILE expression COLON suite'''
    p[0] = ast(p, "WHILELOOP", 2, 4)    


def p_for_iter(p):
    # for item:type in list:
    '''for_loop : FOR IDENTIFIER IN expression COLON suite''' 
    p[0] = ast(p, "FORLOOP_ITER", 2, 4, 6)               

def p_for_count(p):
    # for i in 4..9:
    '''for_loop : FOR IDENTIFIER IN expression DOTDOT expression COLON suite'''
    p[0] = ast(p, "FORLOOP_COUNT", 2, 4, 6, 8)
                  
#------------------------------------------------------------------------------#
# CONDITIONAL                                                                  #
# This family of rules allow for the use of complex conditional constructs     #
#------------------------------------------------------------------------------#
def p_conditional(p):
    # if x == 10:
    '''conditional : IF expression COLON suite conditional_extension'''
    p[0] = ast(p, "CONDITIONAL", 2, 4, 5)

def p_conditional_extension_empty(p):
    '''conditional_extension : empty'''
    p[0] = p[1]
    
def p_conditional_extension_elif(p):
    # elif x == 15:
    '''conditional_extension : ELIF expression COLON suite conditional_extension'''
    p[0] = ast(p, "CONDITIONAL_ELIF", 2, 4, 5)

def p_conditional_extension_else(p):
    # else:
    '''conditional_extension : ELSE COLON suite'''
    p[0] = ast(p, "CONDITIONAL_ELSE", 3)

#------------------------------------------------------------------------------#
# TRY_EXCEPT                                                                   #
# This family of rules allows of the use of exception handling                 #
#------------------------------------------------------------------------------#
def p_try_except(p):
    # try:
    '''try_except : TRY COLON suite exceptlist_nonempty empty empty
                  | TRY COLON suite exceptlist_nonempty except_else empty
                  | TRY COLON suite exceptlist_nonempty empty except_finally
                  | TRY COLON suite exceptlist_nonempty except_else except_finally
                  | TRY COLON suite empty empty except_finally'''
    p[0] = ast(p, "TRY_EXCEPT", 3, 4, 5, 6)

def p_except_simple(p):
    # except:
    '''except_simple : EXCEPT COLON suite'''
    p[0] = ast(p, "EXCEPT_SIMPLE", 3)

    
def p_except_alias(p):
    # except IndexError as e:
    '''except_alias : EXCEPT IDENTIFIER AS IDENTIFIER COLON suite exceptlist'''
    p[0] = ast(p, "EXCEPT_ALIAS", 2, 4, 6, 7)
    
def p_except_specific(p):
    # except IndexError:
    '''except_specific : EXCEPT IDENTIFIER COLON suite exceptlist'''
    p[0] = ast(p, "EXCEPT_SPECIFIC", 2, 4, 5)
    
def p_except_else(p):
    # else:
    '''except_else : ELSE COLON suite'''
    p[0] = ast(p, "EXCEPT_ELSE", 3)

    
def p_except_finally(p):
    # finally:
    '''except_finally : FINALLY COLON suite'''
    p[0] = ast(p, "EXCEPT_FINALLY", 3)

def p_exceptlist_nonempty(p):
    '''exceptlist_nonempty : except_simple
                           | except_alias
                           | except_specific'''
    p[0] = p[1]

def p_exceptlist(p):
    '''exceptlist : except_simple
                  | except_alias
                  | except_specific
                  | empty'''
    p[0] = p[1]


#------------------------------------------------------------------------------#
# ASSIGNMENT                                                                   #
# This rules accounts for the different syntaxes associated with reassigning   #
# values to variables                                                          #
#------------------------------------------------------------------------------#
def p_assignment(p):
    # list[1] = "a"
    # string[:2] = "ab"
    # x = z
    # x += 4 + y
    '''assignment : indexing assignment_operator expression
                  | slicing assignment_operator expression
                  | variable assignment_operator expression
                  | member assignment_operator expression'''

    p[0] = ast(p, "ASSIGNMENT", 1, 2, 3)


# Container for assignment operators    
def p_assignment_operator(p):
    '''assignment_operator : EQUALS
                           | PLUSEQU
                           | MINUSEQU
                           | TIMESEQU
                           | DIVEQU
                           | MODEQU
                           | BITANDEQU
                           | BITOREQU
                           | BITXOREQU
                           | LSHIFTEQU
                           | RSHIFTEQU
                           | POWEQU
                           | INTDIVEQU'''

    p[0] = p[1]


#------------------------------------------------------------------------------#
# INDEXING                                                                     #
# This rule allows for the indexing operator                                   #
#------------------------------------------------------------------------------#
def p_indexing(p):
    # list[1] 
    '''indexing : expression LBRACKET expression RBRACKET'''
    p[0] = ast(p, "INDEXING", 1, 3)
  

#------------------------------------------------------------------------------#
# SLICING                                                                      #
# These two rules allow for the slicing of iterables                           #
#------------------------------------------------------------------------------#
def p_slicing(p):
     # string[1:6:2], etc...
    '''slicing : expression LBRACKET expression COLON expression optslice RBRACKET 
               | expression LBRACKET empty COLON expression optslice RBRACKET 
               | expression LBRACKET expression COLON empty optslice RBRACKET 
               | expression LBRACKET empty COLON empty optslice RBRACKET  '''
    p[0] = ast(p, "SLICING", 1, 3, 5, 6)

def p_optslice_empty(p):
    '''optslice : empty empty
                | COLON empty
                | COLON expression'''
    p[0] = p[2]

#------------------------------------------------------------------------------#
# PROCEDURE CALL                                                               #
# This rule allows for the calling of procedures                               #
#------------------------------------------------------------------------------#
def p_procedure_call(p):
    # print("Hello World")
    '''procedure_call : expression LPAREN expressionlist RPAREN'''
    p[0] = ast(p, "PROCEDURE_CALL", 1, 3)

#------------------------------------------------------------------------------#
# RETURN                                                                       #
# This rule allows the use of both void and nonvoid returns                    #
#------------------------------------------------------------------------------#
def p_return(p):
    # return 
    # return x ** 2
    '''return : RETURN empty
              | RETURN expression'''
    p[0] = ast(p, "RETURN", 2)


def p_assert(p):
    '''assert : assertnomessage
               | assertmessage'''
    p[0] = p[1]

def p_assert_nomsg(p):
    # assert x == y
    '''assertnomessage : ASSERT expression'''
    # p[0] = ast("ASSERT_NOMSG", p[2])
    p[0] = ast(p, "ASSERT_NOMSG", 2)

def p_assert_msg(p):
    # assert x == y, "'x' is not equal to 'y'"
    '''assertmessage : ASSERT expression COMMA literal'''
    # p[0] = ast("ASSERT_MSG", p[2], p[3])
    p[0] = ast(p, "ASSERT_MSG", 2, 4)

def p_yield(p):
    '''yield : YIELD expression'''
    p[0] = ast(p, "YIELD", 2)

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
            | member_type
            | IDENTIFIER'''
    p[0] = ast(p, "TYPE", 1)
   
def p_member_type(p):
    '''member_type : IDENTIFIER DOT IDENTIFIER'''
    p[0] = ast(p, "MEMBER_TYPE", 1, 3)

def p_generator_type(p):
    '''generator_type : GENERATOR OF type'''
    p[0] = ast(p, "GENERATOR_TYPE", 3)

def p_function_type(p):
    # fn (int, int) -> int
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
                 | listbracket '''
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
    
def p_dictionary_type(p):
    # dict of [int|string]
    '''dictionary_type : DICT OF LBRACKET type BITOR type RBRACKET'''
    p[0] = ast(p, "DICTIONARY_TYPE", 4, 6)

#------------------------------------------------------------------------------#
# EXPRESSION                                                                   #
# Container rule for pieces of code that have a value                          #
#------------------------------------------------------------------------------#
def p_expression(p):
    '''expression : calculation
                  | function_call
                  | grouping
                  | literal
                  | indexing
                  | slicing
                  | ternary
                  | member
                  | identity
                  | membership 
                  | variable'''
    p[0] = p[1]
     
#------------------------------------------------------------------------------#
# CALCULATION                                                                  #
# Rules for use of binary and unary operators                                  #
#------------------------------------------------------------------------------#
def p_calculation_binaryoperator(p):
    '''calculation : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression PERCENT expression %prec MODULO
                   | expression INTDIV expression
                   | expression POW expression
                   | expression BITOR expression
                   | expression BITAND expression
                   | expression LSHIFT expression
                   | expression RSHIFT expression
                   | expression EQUALTO expression
                   | expression NEQUALTO expression
                   | expression LT expression
                   | expression LE expression
                   | expression GT expression
                   | expression GE expression
                   | expression REQUALTO expression
                   | expression BOOLOR expression
                   | expression BOOLAND expression
                   | expression OR expression
                   | expression AND expression
                   | expression CARET expression %prec BITXOR'''

    p[0] = ast(p, "CALCULATION_BINARYOPERATOR", 1, 2, 3)

    
def p_calculation_unaryoperator(p):
    '''expression : MINUS expression %prec UMINUS
                   | PLUS expression %prec UPLUS
                   | TILDE expression %prec BITINVERT
                   | EXMARK expression %prec BOOLNOT
                   | NOT expression %prec BOOLNOT '''
    p[0] = ast(p, "CALCULATION_UNARYOPERATOR", 1, 2)
    
#------------------------------------------------------------------------------#
# FUNCTION CALL                                                                #
# This rule, and its helpers, allow for the calling of a function              #
#------------------------------------------------------------------------------#
def p_function_call(p):
    # add(4, 5)
    '''function_call : expression LPAREN expressionlist RPAREN'''
    p[0] = ast(p, "FUNCTION_CALL", 1, 3)    

def p_expressionlist(p):
    '''expressionlist : nonempty_expressionlist
                      | empty'''
    p[0] = p[1]

def p_nonempty_expressionlist_single(p):
    '''nonempty_expressionlist : expression'''
    p[0] = ast(p, "EXPRESSIONLIST_SINGLE", 1)
    
def p_nonempty_expressionlist_multi(p):
    '''nonempty_expressionlist : nonempty_expressionlist COMMA nonempty_expressionlist'''
    p[0] = ast(p, "EXPRESSIONLIST_MULTI", 1, 3)
    
    
#------------------------------------------------------------------------------#
# GROUPING                                                                     #
# This rule is allows for parenthesization of expressions                      #
#------------------------------------------------------------------------------#
def p_grouping(p):
    # (4 + 5)
    '''grouping : LPAREN expression RPAREN'''
    p[0] = ast(p, "GROUPING", 2)
    
#------------------------------------------------------------------------------#
# LITERAL                                                                      #
# This family of rules allows for the expression of literal values             #
#------------------------------------------------------------------------------#
def p_literal_int(p):
    # 1 
    '''literal : INTLITERAL'''
    p[0] = ast(p, "LITERAL_INT", 1)
    
def p_literal_float(p):
    # 4.0
    '''literal : FLOATLITERAL'''
    p[0] = ast(p, "LITERAL_FLOAT", 1)
    
def p_literal_bool(p):
    # True
    # False
    '''literal : BOOLLITERAL'''
    p[0] = ast(p, "LITERAL_BOOL", 1)
    
def p_literal_string(p):
    # "Hello World"
    '''literal : STRINGLITERAL
               | DOCSTRING'''
    p[0] = ast(p, "LITERAL_STRING", 1)

def p_literal_none(p):
    #None
    '''literal : NONE'''
    p[0] = ast(p, "LITERAL_NONE", 1)

def p_literal_complex(p):
    '''literal : function_literal
               | procedure_literal
               | tuple_literal
               | list_literal
               | dictionary_literal
               | set_literal'''
    p[0] = p[1]
    
def p_function_literal(p):
    # lambda (x:int) -> int : (x * 2)
    '''function_literal : LAMBDA LPAREN argumentlist RPAREN ARROW type COLON LPAREN expression RPAREN'''
    p[0] = ast(p, "LITERAL_FUNCTION", 3, 6, 9)   

    
def p_tuple_literal(p):
    # (1,)
    # (1,2)
    '''tuple_literal : LPAREN tuplelist RPAREN''' 
    p[0] = ast(p, "LITERAL_TUPLE", 2)

def p_tuplelist(p):
    '''tuplelist : nonempty_tuple 
                 | empty'''
    p[0] = p[1]

def p_nonempty_tuple(p):
    '''nonempty_tuple : singletontuple
                      | crosstuple '''
    p[0] = p[1]

def p_singletontuple(p):
    '''singletontuple : nonempty_expressionlist COMMA'''
    p[0] = ast(p, "TUPLE_SINGLE", 1)

def p_crosstuple(p):
    '''crosstuple : nonempty_expressionlist'''
    p[0] = ast(p, "MULTI_TUPLE", 1)

def p_list_literal(p):
    # [], [1], [1,2]
    '''list_literal : LBRACKET expressionlist RBRACKET'''
    p[0] = ast(p, "LITERAL_LIST", 2)

def p_dictionary_literal(p):
    # { 1 : "a", 2 : "b" }
    '''dictionary_literal : LCURLY dictionarylist RCURLY'''
    p[0] = ast(p, "LITERAL_DICTIONARY", 2)
   
def p_dictionarylist(p):
    '''dictionarylist : nonempty_dictionarylist
                      | empty'''
    p[0] = p[1]
    
def p_nonempty_dictionarylist_single(p):
    '''nonempty_dictionarylist : expression COLON expression'''
    p[0] = ast(p, "DICTIONARYLIST_SINGLE", 1, 3)
    
def p_nonempty_dictionarylist_multi(p):
    '''nonempty_dictionarylist : nonempty_dictionarylist COMMA nonempty_dictionarylist'''
    p[0] = ast(p, "DICTIONARYLIST_MULTI", 1, 3)

# A set literal has to contain at least 1 element 
# Use makeset() to make an empty set
def p_set_literal(p):
    # {1} , {1,2}
    '''set_literal : LCURLY nonempty_expressionlist RCURLY'''
    p[0] = ast(p, "LITERAL_SET", 2)
    
#------------------------------------------------------------------------------#
# VARIABLE                                                                     #
# This rule simply allows for type checking to determine if an identifier is a #
# variable or a type                                                           #
#------------------------------------------------------------------------------#
def p_variable(p):
    '''variable : IDENTIFIER'''
    p[0] = ast(p, "VARIABLE", 1)

#------------------------------------------------------------------------------#
# TERNARY                                                                      #
# This rule allows for the use of the ternary operator                         #
#------------------------------------------------------------------------------#
def p_ternary(p):
    # x == y ? x * 2 : x * 3
    '''ternary : expression QMARK expression COLON expression %prec TERNARY'''
    p[0] = ast(p, "TERNARY", 1, 3, 5)


#------------------------------------------------------------------------------#
# MEMBER                                                                       #
# This rule allows for the use of the dot operator to access members or        #
# attributes and the 'in' and 'not in' key words to evaluate membership.       #
#------------------------------------------------------------------------------#
def p_member(p):
    # circle.center
    '''member : expression DOT IDENTIFIER'''
    p[0] = ast(p, "MEMBER", 1, 3)


#------------------------------------------------------------------------------#
# IDENTITY                                                                     #
# Allows for the use of the identity operators 'is' and 'is not'               #
#------------------------------------------------------------------------------#
def p_identity_is(p):
    # x is y
    ''' identity : expression IS expression'''
    p[0] = ast(p, 'IS_IDENTITY', 1, 3)

def p_identity_is_not(p):
    # x is not y
    '''identity : expression ISNOT expression'''
    p[0] = ast(p, 'IS_NOT_IDENTITY', 1, 3)


#------------------------------------------------------------------------------#
# MEMBERSHIP                                                                   #
# Allows for membership testing.                                               #
#------------------------------------------------------------------------------#
def p_membership_in(p):
    # 1 in [1,2,3]
    '''membership : expression IN expression'''
    p[0] = ast(p, 'IN_MEMBER', 1, 3)

def p_membership_notin(p):
    # 4 not in [1,2,3]
    '''membership : expression NOTIN expression'''
    p[0] = ast(p, 'NOTIN_MEMBER', 1, 3)

    
#----------------------------ERROR HANDLING------------------------------------#

#------------------------------------------------------------------------------#
# p_error(p:LexToken)                                                          #
#   Displays an error message when parse errors are encountered.               #
#                                                                              #
#   CSPy : SyntaxError                                                         #
#   Line NUM, Colum NUM                                                        #
#                                                                              #
#   code code error code                                                       #
#             ^^^^^                                                            #
#   If there is an error rule defined in the grammar (see definitions below),  #
#   the parser will attempt to resynchronize itself by finding the next        #
#   terminal that follows the error token in the rule and continue parsing     #
#   input from that point, allowing it to catch more than one syntax error     #
#   in a file. If the error is followed by a nonterminal, or fails             #
#   to encounter the next terminal, the parser will be unable to resynchronize #
#   itself and will either stop parsing or mistakenly identify good code as    #
#   as syntax errors.                                                          #
#------------------------------------------------------------------------------#
def p_error(p):
    # Invalid character - Lexer takes care of this error
    if not p: return

    print >> sys.stderr, "CSPy : Syntax Error"

    # Get the line from the source code
    source = p.lexer.lexdata.split('\n')
    lineno = p.lineno
    line =  source[lineno - 1]
 
    # Assume error occurred on previous line if current line is whitespace
    # Find previous nonwhitespace or noncomment line
    white_space = re.compile('^([ \t]+|[#].*)$')
    while (white_space.match(line) or line == '') and lineno != 1:
        lineno = lineno - 1
        line = source[lineno - 1]
    
    error_length = p.value if (p.type == 'DEDENT' or p.type == 'INDENT') \
        else len(p.value)
    
    # Find the column of the token in the source code
    if p.type == 'NL': col = len(line) + 1
    elif p.type == 'DEDENT' or p.type == 'INDENT': col = 1
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
 
    message = "Line " + str(lineno) + ", Column " +  str(col) + "\n\n" \
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

def p_declaration_error(p):
    '''declaration : IDENTIFIER COLON error EQUALS expression '''
    print >> sys.stderr, "Invalid type in declaration.\n"

#--Class Definitions-----------------------------------------------------------#

def p_class_definition_error(p):
    ''' class_definition : CLASS IDENTIFIER opt_extends error NL INDENT class_suite DEDENT
                         | CLASS IDENTIFIER opt_extends COLON NL INDENT error DEDENT'''
    print >> sys.stderr, "Class definition invalid syntax.\n"

#--Function and Procedure Definitions------------------------------------------#

def p_function_definition_error(p):
     '''function_definition : DEF error LPAREN argumentlist RPAREN ARROW type COLON suite
                            | DEF IDENTIFIER LPAREN argumentlist error ARROW type COLON suite
                            | DEF IDENTIFIER LPAREN argumentlist RPAREN ARROW error COLON suite'''
     print >> sys.stderr, "Function definition invalid syntax.\n"
    
def p_procedure_definition_error(p):
     '''procedure_definition : DEF error LPAREN argumentlist RPAREN COLON suite 
                             | DEF IDENTIFIER LPAREN argumentlist error COLON suite '''
     print >> sys.stderr, "Procedure definition invalid syntax.\n"

def p_argumentlist_single_error(p):
    '''nonempty_argumentlist : error COLON type'''
    print >> sys.stderr, "Invalid identifier.\n"

def p_defaultlist_single_error(p):
    '''nonempty_defaultlist : IDENTIFIER COLON error EQUALS expression'''
    print >> sys.stderr, "Invalid type in default list.\n"

#--LOOPS, CONDITIONALS, TRY-EXCEPT---------------------------------------------#

def p_while_error(p):
    '''while_loop : WHILE error COLON suite '''
    print >> sys.stderr, "Invalid boolean expression.\n"

def p_for_iter_error(p):
    '''for_loop : FOR error IN expression COLON suite
                | FOR IDENTIFIER IN error COLON suite
                | FOR error IN expression DOTDOT expression COLON suite
                | FOR IDENTIFIER IN error DOTDOT expression COLON suite
                | FOR IDENTIFIER IN expression DOTDOT error COLON suite'''
    print >> sys.stderr, "'for' loop invalid syntax.\n"

def p_conditional_error(p):
    '''conditional : IF error COLON suite conditional_extension'''
    print >> sys.stderr, "Invalid boolean expression.\n"
    
def p_conditional_extension_error(p):
    '''conditional_extension : ELIF error COLON suite conditional_extension'''
    print >> sys.stderr, "Invalid boolean expression.\n"

def p_except_alias_error(p):
    '''except_alias : EXCEPT error AS IDENTIFIER COLON suite exceptlist 
                    | EXCEPT IDENTIFIER AS error COLON suite exceptlist'''
    print >> sys.stderr, "Invalid indentifier.\n"

def p_except_specific_error(p):
    '''except_specific : EXCEPT error COLON suite exceptlist'''
    print >> sys.stderr, "Invalid identifier.\n"

#--INDEXING, SLICING-----------------------------------------------------------#

def p_indexing_error(p):
    '''indexing : expression LBRACKET error RBRACKET'''
    print >> sys.stderr, "Index invalid syntax.\n"

def p_slicing_error(p):
    '''slicing : expression LBRACKET error COLON expression optslice RBRACKET
               | expression LBRACKET expression COLON expression error RBRACKET'''
    print >> sys.stderr, "Slicing invalid syntax.\n"

#--PROCEDURE, FUNCTION CALL----------------------------------------------------#

def p_procedure_call_error(p):
    '''procedure_call : expression LPAREN error RPAREN'''
    print >> sys.stderr, "Procedure call invalid syntax.\n"

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

def p_tuple_type_error(p):
    '''tuple_type : TUPLE error LPAREN tuple_typelist RPAREN
                  | TUPLE OF LPAREN error RPAREN'''
    print >> sys.stderr, "Tuple type declaration invalid syntax.\n"

#--Lambda Expressions----------------------------------------------------------#
def p_functional_literal_error(p):
    '''function_literal : LAMBDA LPAREN error RPAREN ARROW type COLON LPAREN expression RPAREN
                        | LAMBDA LPAREN argumentlist RPAREN ARROW error COLON LPAREN expression RPAREN
                        | LAMBDA LPAREN argumentlist RPAREN ARROW type COLON LPAREN error RPAREN'''
    print >> sys.stderr, "Lambda expression invalid syntax.\n"

def p_procedure_literal_error(p):
    '''procedure_literal : LAMBDA LPAREN error RPAREN COLON LPAREN statement_simple RPAREN
                         | LAMBDA LPAREN argumentlist RPAREN error LPAREN statement_simple RPAREN
                         | LAMBDA LPAREN argumentlist RPAREN COLON LPAREN error RPAREN'''
    print >> sys.stderr, "Lambda expression invalid syntax.\n"

#--Tuple, List, Dictionary Literals--------------------------------------------#
def p_list_literal_error(p):
    '''list_literal : LBRACKET error RBRACKET'''
    print >> sys.stderr, "List element invalid syntax.\n"

def p_dictionary_literal_error(p):
    '''dictionary_literal : LCURLY error RCURLY'''
    print >> sys.stderr, "Dictionary entry invalid syntax.\n"
