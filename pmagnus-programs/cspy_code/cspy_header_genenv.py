#------------------------------------------------------------------------------#
# cspy_header_genenv.py                                                        #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#                                                                              #
# Generates environments with variables in their scope for a CSPy header file. #
# The main function, generate_environments, relies on the                      #
# environment-generating functions defined below it (all names prefixed with   #
# a g_), each of which corresponds to an ast node such as a variable           #
# declaration block, a function definition, or a class definition, which       #
# involves identifiers.                                                        #
#------------------------------------------------------------------------------#

from cspy_data_struct import *
from cspy_builtins import *
from cspy_header_type import det_type

#------------------------------------------------------------------------------#
# generate_environments(node:ast)                                              #
#   POST: the "env" attribute of all nodes in the abstract syntax tree which   #
#         can hold an environment will be filled with the variable             #
#         associations for thier scope                                         #
#------------------------------------------------------------------------------#

def generate_environments(node):
    tree_pass(node, variables)

#------------------------------------------------------------------------------#
# tree_pass(node:ast, actions:dict of [string|proc])                           #
#   Recursively traverses the abstract syntax tree and generates               #
#   the environments for all nodes which can hold environments.                #
#------------------------------------------------------------------------------#

def tree_pass(node, actions):
    if not isinstance(node, ast):
        return

    if node.label in actions:
        actions[node.label](node)

    for child in node.children:
        tree_pass(child, actions)

#------------------------------------------------------------------------------#
#                       ENVIRONMENT GENERATING FUNCTIONS                       #
#                                                                              #
# The following functions define what action should be taken for each type     #
# of abstract syntax tree node. These have the following naming format:        #
# g_[a-z_]+                                                                    #
#                                                                              #
# Note: The name of the function is the lowercase version of the name of the   #
# type of node it acts upon.                                                   #
# Note: The first line of each function is a comment containing a list of the  #
# indices of the node "n" and what they contain (this information is defined   #
# in "parser_defs.py")                                                         #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# g_declaration(n:ast)                                                         #
#   Creates a new varialbe in the current scope of the given name and type.    #
#------------------------------------------------------------------------------#

def g_declaration(n):
    # 0: identifier; 1: type
    det_type(n[1])
    try:
        n.initiate_var(n[0], n[1].type)
    except DeclarationException:
        type_error("The variable '" + n[0] + "' has already been defined in " +
                   "the current scope.\nOnly functions and procedures can " +
                   "have multiple definitions.", n)

#------------------------------------------------------------------------------#
# g_function_definition(n:ast):                                                #
#   Creates a new variable in the current environment whose value is a         #
#   funciton type object with a given signature.                               #
#------------------------------------------------------------------------------#
def g_function_definition(n):
    # 0: identifier; 1: argument list; 2: return type
    det_type(n[1])
    det_type(n[2])
    sig = n[1].type
    sig.return_type = n[2].type

    try:
        n.parent.initiate_var(n[0],type_obj("fn", builtins["fn"], sig = sig))

    except SignatureException:
        # Function overloading - duplicate signature
        type_error("The function '" + n[0] + "' with the signature '" +
                   repr(sig) + "' has already been defined.", n[1], n[2])

    except DeclarationException:
        type_error("'" + n[0] + "' has already been declared in the current" + 
                   "scope, and is not a function or procedure. " +
                   "Only\nfunction and procedure definitions are allowed to " + 
                   " have more than one value.", n)

#------------------------------------------------------------------------------#
# g_procedure_definition(n:ast):                                               #
#   Creates a new variable in the current environment whose value is a         #
#   procedure type object with a given signature.                              #
#------------------------------------------------------------------------------#
def g_procedure_definition(n):
    # 0: identifier; 1: argument list
    det_type(n[1])
    sig = n[1].type

    try:
        n.parent.initiate_var(n[0],type_obj("proc",builtins["proc"], sig = sig))

    except SignatureException:
        # Function overloading - duplicate signature
        type_error("The procedure '" + n[0] + "' with the signature '" +
                   repr(sig) + "' has already been defined.", n[1])

    except DeclarationException:
        type_error("'" + n[0] + "' has already been declared in the current" + 
                   "scope, and is not a function or procedure.\n" +
                   "Only function and procedure definitions are allowed to " + 
                   " have more than one value.", n)

#------------------------------------------------------------------------------#
# g_class_definition(n:ast):                                                   #
#   Creates a new type in the global environment                               #
#------------------------------------------------------------------------------#

def g_class_definition(n):
    # 0: identifier; 1: super class; 2: classblock

    # Class extension
    if n[2].label == "EMPTY":
        sup = builtins["object"]
    else:
        det_type(n[1])
        sup = n[1].type

    # Temporarily initialize the class in the global environment
    # without any methods. This allows class methods in the class to
    # have local variables whose type is the class
    try:
        n.parent.initiate_var(n[0], type_obj(n[0], builtins["Type"], sup = sup))
    except DeclarationException:
        type_error("'" + n[0] + "' has already been declared in the current" + 
                   "scope, and is not a function or procedure.\n" +
                   "Only function and procedure definitions are allowed to " + 
                   " have more than one value.", n)

    # Get the class attributes
    det_type(n[2][1][0])
    attributes = n[2][1][0]
    if attributes.label == "EMPTY":
        # Empty variable declaration block - no class attributes
        attribute_nodes = []

    else:
        # Nonempty variable declaration block - has class attributes
        attribute_nodes = attributes.flatten("DECLARATION_SIMPLE") + \
            attributes.flatten("DECLARATION_INITIALIZE")

    # Add the attributes to the method dictionary
    methods = {}
    for a in attribute_nodes:
        methods[a[0]] = a[1].type

    # Get the class methods
    method_nodes = n[2].flatten("PROCEDURE_DEFINITION") + \
        n[2].flatten("FUNCTION_DEFINITION")

    # Add each method to the method dictionary
    for m in method_nodes:
        name = m[0]
        det_type(m[1])
        sig = m[1].type
        if m.label == "PROCEDURE_DEFINITION":
            # procedure overloading
            if name in methods.keys():
                if isinstance(methods[name], list):
                    # Add the new procedure signature to the class
                    methods[name].append(type_obj("proc", builtins["proc"], sig = sig))

                # First overload
                else:
                    methods[name] = [methods[name], type_obj("proc", builtins["proc"], sig = sig)]

            # Undeclared variable - add it to the class
            else:
                methods[name] = type_obj("proc", builtins["proc"], sig = sig)

        else:
            det_type(m[2])
            sig.return_type = m[2].type
            # function overloading
            if name in methods.keys():
                if (isinstance(methods[name], list)):
                    # Add the new function signature to the class
                    methods[name].append(type_obj("fn", builtins["fn"], sig = sig))

                # First overload
                else:
                    methods[name] = [methods[name], type_obj("fn", builtins["fn"], sig = sig)]
            # Undeclared variable - add it to the class
            else:
                methods[name] = type_obj("fn", builtins["fn"], sig = sig)

    # Locate the global environment and update the class method dictionary
    current = n
    while current.parent:
        current = current.parent

    current.env[n[0]].methods = methods

variables = {
    "DECLARATION_SIMPLE"     : g_declaration,
    "FUNCTION_DEFINITION"    : g_function_definition,
    "PROCEDURE_DEFINITION"   : g_procedure_definition,
    "CLASS_DEFINITION"       : g_class_definition,
    }