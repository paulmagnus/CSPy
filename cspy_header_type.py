#------------------------------------------------------------------------------#
# cspy_header_type.py                                                          #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#                                                                              #
# Based on cspy_type_checker.py, this file contains functions for determining  #
# the type of complex structures in the CSPy header files.                     #
#------------------------------------------------------------------------------#

# PYTHON MODULES
import sys

# LOCAL IMPORTS
from cspy_data_struct import *
from cspy_builtins import *
from cspy_runtime import remove_files

#------------------------------------------------------------------------------#
# det_type(astnode)                                                            #
#   Recursively traverses the abstract synatx tree of a CSPy header file to    #
#   determine the type of each node.                                           #
#------------------------------------------------------------------------------#

def det_type(astnode):
    if not isinstance(astnode, ast):
        return

    for child in astnode.children:
        det_type(child)

    if astnode.label in checks:
        checks[astnode.label](astnode)

#------------------------------------------------------------------------------#
# type_error(message:string, *nodes:ast)                                       #
#  Displays a type error using the following format:                           #
#                                                                              #
# There is a Type Error                                                        #
# Line NUMBER1, Column NUMBER1: TYPE1                                          #
# LINEOFCODE1                                                                  #
#       ^^^^                                                                   #
# Line NUMBER2, Column NUMBER2: TYPE2                                          #
# LINEOFCODE2                                                                  #
#       ^^^^                                                                   #
# ...                                                                          #
# Line NUMBERn, Column NUMBERn: TYPEn                                          #
# LINEOFCODEn                                                                  #
#       ^^^^                                                                   #
# MESSAGE                                                                      #
#                                                                              #
# For each node in "*nodes", its line number, column number, type, the line it #
# is on, and an underline of the code representing that node are printed out.  #
# Then the given error message is printed out.                                 #
#------------------------------------------------------------------------------#
def type_error(message, *nodes):
    result = "\nCSPy : Header Type Error\n"
    for node in nodes:

        column = node.column
        endColumn = node.endColumn
        line_list = node.line.split("\n")

        name = str(node.type) if node.type else ""
        result += ("Line " + str(node.lineNum) + ", Column " + str(node.column) 
                   + ": " + name + "\n")

        for i in range(len(line_list)):
            indent_index = 0
            while (indent_index < len(line_list[i]) and 
                   (line_list[i][indent_index] == " " or 
                    line_list[i][indent_index] == "\t")):
                indent_index += 1

            if (indent_index >= len(line_list[i]) or 
                line_list[i][indent_index] == "#"):
                column -= len(line_list[i]) + 1      
                endColumn -= len(line_list[i]) + 1
                continue

            lstart = max(indent_index + 1, column)
            lend = min(len(line_list[i]), endColumn)
            result += line_list[i] + "\n"
            result += " " * (lstart - 1)
            result += "^" * (lend - lstart + 1)
            result += " " * (len(line_list[i]) - lend)
            result += "\n"
            column -= len(line_list[i]) + 1
            endColumn -= len(line_list[i]) + 1

    result += message + "\n"
    print >> sys.stderr, result
    remove_files()
    sys.exit(1)

#------------------------------------------------------------------------------#
# global_env(n:ast) -> ast                                                     #
#    Returns the node of an abstract syntax tree containing the global         #
#    environment by traversing the tree from n to the root node.               #
#------------------------------------------------------------------------------#

def global_env(n):
    current = n
    while current.parent:
        current = current.parent
    return current

#------------------------------------------------------------------------------#
#                      TYPE-DETERMINING FUNCTIONS                              #
#                                                                              #
# The following functions define what action should be taken for each type of  #
# abstract syntax tree node. These functions follow a naming convention of     #
# s_[a-z_]+ where the name of the function is the lowercase verion of the name #
# of the type of node it acts upon.                                            #
#                                                                              #
# The first line of each function is a comment containing a list of the        #
# indeces of the node "n" and what they contain (this information is defined   #
# in "cspy_header_parser.py").                                                 #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                                  TYPES                                       #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_type(n:ast)                                                                #
#------------------------------------------------------------------------------#

def s_type(n):
    # 0: type

    if isinstance(n[0], str):
        globalnode = global_env(n)
        globalenv = globalnode.env

        try:
            # Lookup the type identifier
            typ = n.lookup_var(n[0])

        except NotYetDeclaredException:
            # Identifier undeclared
            type_error("'" + n[0] + "'is not a declared type.", n)

        else:
            # Identifier is not a type
            if not is_type(typ):
                
                # Prevents user types (classes) from receiving the type
                # of their constructors (procedure type) inside of a class
                # definitions
                if n[0] in globalenv and is_type(globalnode.lookup_var(n[0])):
                    n.type = globalnode.lookup_var(n[0])

                else:
                    type_error("'" + n[0] + "'is declared, but it is not a " +
                               "type.", n)

            else:
                n.type = typ

    else:
        # Take the type of its child node
        n.type = n[0].type

#------------------------------------------------------------------------------#
# s_typelist(n)                                                                #
#   Creates a signature object from a list of types for the parameters of a    #
#   function type literal or a procedure type literal.                         #
#------------------------------------------------------------------------------#

def s_typelist(n):
    # 0: type list; 1: default type list
    type_list = [t.type for t in n[0].flatten("TYPELIST_SINGLE")]
    default_list = [d.type for d in n[1].flatten("DEFAULT_TYPELIST_SINGLE")]
    n.type = signature(params = type_list, defaults = default_list)

#------------------------------------------------------------------------------#
# s_typelist_single(n)                                                         #
#   Sets the type of a single typelist node to the type of its child.          #
#------------------------------------------------------------------------------#

def s_typelist_single(n):
    # 0: type
    n.type = n[0].type

#------------------------------------------------------------------------------#
# s_default_typelist_single(n)                                                 #
#   Sets the type of a single default typelist entry node to the type of its   #
#   child.                                                                     #
#------------------------------------------------------------------------------#

def s_default_typelist_single(n):
    # 0: type
    n.type = n[0].type

#------------------------------------------------------------------------------#
# s_dictionary_type(n:ast)                                                     #
#   Sets the type of a dictionary to a dictionary type object.                 #
#------------------------------------------------------------------------------#

def s_dictionary_type(n):
    # 0: key type; 1: value type
    n.type = init_dict([n[0].type, n[1].type])


#------------------------------------------------------------------------------#
# s_tuple_type(n:ast)                                                          #
#   Sets the type of a tuple to a tuple type object.                           #
#------------------------------------------------------------------------------#

def s_tuple_type(n):
    # 0: type list
    type_list = n[0].flatten('TUPLE_TYPELIST_SINGLE')
    tuple_types = [t.type for t in type_list]
    n.type = init_tuple(tuple_types)

#------------------------------------------------------------------------------#
# s_set_type(n:ast)                                                            #
#   Sets the type of a set to a set type object.                               #
#------------------------------------------------------------------------------#

def s_set_type(n):
    n.type = init_set(n[0].type)

#------------------------------------------------------------------------------#
# s_frozenset_type(n:ast)                                                      #
#   Sets the type of a frozenset to a frozenset type object.                   #
#------------------------------------------------------------------------------#

def s_frozenset_type(n):
    n.type = init_frzset(n[0].type)

#------------------------------------------------------------------------------#
# s_tuple_typelist_single(n)                                                   #
#   Sets the type of a single tuple type list entry node to the type of its    #
#   child.                                                                     #
#------------------------------------------------------------------------------#

def s_tuple_typelist_single(n):
    # 0: type
    n.type = n[0].type
  
#------------------------------------------------------------------------------#
# s_list_type(n:ast)                                                           #
#   Sets the type of a list to a list type object.                             #
#------------------------------------------------------------------------------#

def s_list_type(n):
    # 0: type
    n.type = init_list([n[0].type])

#------------------------------------------------------------------------------#
# s_generator_type(n:ast)                                                      #
#   Sets the type of a generator to a generator type object                    #
#------------------------------------------------------------------------------#

def s_generator_type(n):
    # 0: type
    n.type = init_generator([n[0].type])

#------------------------------------------------------------------------------#
#                                 FUNCTIONS                                    #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_function_type(n)                                                           #
#  Sets the type of a function type literal (eg fn (int) -> int) to a 'fn'     #
#  type object with the appropriate signature.                                 #
#------------------------------------------------------------------------------#

def s_function_type(n):
    # 0: parameters; 1: return
    sig = n[0].type
    sig.return_type = n[1].type
    n.type = type_obj("fn", builtins["fn"], sig = sig)

#------------------------------------------------------------------------------#
# s_procedure_type(n)                                                          #
#   Sets the type of a procedure type literal (eg. proc (string)) to a new     #
#   'proc' type object.                                                        #
#------------------------------------------------------------------------------#

def s_procedure_type(n):
    # 0: parameters
    n.type = type_obj("proc", builtins["proc"], sig = n[0].type)

#------------------------------------------------------------------------------#
#                                 ARGUMENTS                                    #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_argumentlist(n:ast)                                                        #
#   Sets the type of an argument list node to a signature object               #
#   whose parameter and default types are set accordingly.                     #
#------------------------------------------------------------------------------#

def s_argumentlist(n):
    # 0: normal arguments; 1: default arguments  
    nondefaults = [t.type for t in n[0].flatten("ARGUMENTLIST_SINGLE")]
    defaults = [d.type for d in n[1].flatten("DEFAULTLIST_SINGLE")]
    n.type = signature(params = nondefaults, defaults = defaults)

#------------------------------------------------------------------------------#
# s_argumentlist_single(n:ast)                                                 #
#   Assigns the type of an single argument to the type of its indentifier.     #
#------------------------------------------------------------------------------#

def s_argumentlist_single(n):
    # 0: identifier; 1: type
    n.type = n[1].type

#------------------------------------------------------------------------------#
# s_defaultlist_single(n:ast)                                                  #
#   Assigns the type of the single default argument to its declared type       #
#------------------------------------------------------------------------------#
def s_defaultlist_single(n):
    # 0: identifier; 1: type
    n.type = n[1].type


checks = {
    # Functions, Operations
    "FUNCTION_TYPE"              : s_function_type,
    "PROCEDURE_TYPE"             : s_procedure_type,
    
    # Types
    "TYPE"                       : s_type,
    "TYPELIST"                   : s_typelist,
    "TYPELIST_SINGLE"            : s_typelist_single,
    "DEFAULT_TYPELIST_SINGLE"    : s_default_typelist_single,
    "DICTIONARY_TYPE"            : s_dictionary_type,
    "TUPLE_TYPE"                 : s_tuple_type,
    "TUPLE_TYPELIST_SINGLE"      : s_tuple_typelist_single,
    "LIST_TYPE"                  : s_list_type,
    "SET_TYPE"                   : s_set_type,
    "FROZENSET_TYPE"             : s_frozenset_type,
    "GENERATOR_TYPE"             : s_generator_type,
    
    # Arguments
    "ARGUMENTLIST"               : s_argumentlist,
    "ARGUMENTLIST_SINGLE"        : s_argumentlist_single,
    "DEFAULTLIST_SINGLE"         : s_defaultlist_single,
    }