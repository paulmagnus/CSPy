#------------------------------------------------------------------------------#
# cspy_genenv.py                                                               #
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
# Generates environments with variables in their scope for a CSPy program. The #
# main function, generate_environments, relies on the environment-generating   #
# functions defined below it (all names prefixed with a g_), each of which     #
# corresponds to an ast node such as a variable declaration block, a function  #
# definition, or a class definition, which involves identifiers.               #
#------------------------------------------------------------------------------#
from cspy_data_struct import *
from cspy_type_checker import det_type, type_error
from cspy_builtins import *

#------------------------------------------------------------------------------#
# generate_environments(node:ast)                                              #
#   POST: the "env" attribute of all nodes in the abstract syntax tree which   #
#         can hold an environment will be filled with the variable             #
#         associations for their scope                                         #
#------------------------------------------------------------------------------#
def generate_environments(node, filename):
    global file_name
    file_name = filename
    tree_pass(node, variables)

#------------------------------------------------------------------------------#
# tree_pass(node:ast, actions:dict of [string|proc])                           #
#   Recursively traverses the abstract syntax tree and generates               #
#   the environments for all nodes which can hold environments.                #
#------------------------------------------------------------------------------#
def tree_pass(node, actions):
    if (not isinstance(node, ast)):
        return

    if (node.label in actions):
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
#   Creates a new variable in the current scope of the given name              #
#   and type.                                                                  #
#------------------------------------------------------------------------------#
def g_declaration(n):
    # 0: identifier; 1: type
    det_type(n[1], file_name)
    try:
        n.initiate_var(n[0], n[1].type)
    except DeclarationException:
        type_error("The variable '" + n[0] +"' has already been defined in " +
                   "the current scope.\nOnly functions and procedures can " +
                   "have multiple definitions.", file_name, n)

#------------------------------------------------------------------------------#
# g_argumentlist(n:ast)                                                        #
#   Creates a new variable of the given name and type inside of                #
#   the subroutine definition in which it is contained.                        #
#------------------------------------------------------------------------------#
def g_argumentlist(n):
    # 0: identifier; 1: type
    det_type(n[1], file_name)
    identifier = n[0]
    t = n[1].type
 
    # Locate the function or procedure node
    while (n.label != "FUNCTION_DEFINITION" and \
               n.label != "PROCEDURE_DEFINITION" and \
               n.label != "LITERAL_FUNCTION" and \
               n.label != "LITERAL_PROCEDURE"):
        n = n.parent

    
    # Function or procedure literal - lambda expression 
    if n.label == "LITERAL_FUNCTION" or n.label == "LITERAL_PROCEDURE":
        try:
            n.initiate_var(identifier, t)
        except DeclarationException:
            type_error("'" + n[0] + "' has already been declared in the " +
                       "current scope, and is not a function or procedure.\n" +
                   "Only function and procedure definitions are allowed to " + 
                   " have more than one value.", file_name, n)

    else:
        # Function or procedure defintion
        # Child node with an environment = n[3] if function, n[2] if procedure
        n = n[3] if (len(n.children) == 4) else n[2] 
        if (n.label == "SUITE_BLOCK"):
            try:
                n[1].initiate_var(identifier, t)
            except DeclarationException:
                type_error("'" + n[0] + "' has already been declared in the "
                           " current scope, and is not a function or " +
                           "procedure.\nOnly function and procedure " + 
                           " definitions are allowed to have more than one " + 
                           "value.", file_name, n)
        if (n.label == "SUITE_INLINE"):
            try:
                n.initiate_var(identifier, t)
            except DeclarationException:
                type_error("'" + n[0] + "' has already been declared in the "
                           " current scope, and is not a function or " +
                           "procedure.\nOnly function and procedure " + 
                           " definitions are allowed to have more than one " + 
                           "value.", file_name, n)


#------------------------------------------------------------------------------#
# g_function_definition(n:ast):                                                #
#   Creates a new variable in the current environment whose value is a         #
#   funciton type object with a given signature.                               #
#------------------------------------------------------------------------------#
def g_function_definition(n):
    # 0: identifier; 1: argument list; 2: return type; 3: suite
    det_type(n[1], file_name)
    det_type(n[2], file_name)
    sig = n[1].type
    sig.return_type = n[2].type

    try:
        n.parent.initiate_var(n[0],type_obj("fn", builtins["fn"], sig = sig))

    except SignatureException:
        # Function overloading - duplicate signature
        type_error("The function '" + n[0] + "' with the signature '" +
                   repr(sig) + "' has already been defined.", file_name, n[1], n[2])

    except DeclarationException:
        type_error("'" + n[0] + "' has already been declared in the current" + 
                   "scope, and is not a function or procedure. " +
                   "Only\nfunction and procedure definitions are allowed to " + 
                   " have more than one value.", file_name, n)
    
        

#------------------------------------------------------------------------------#
# g_procedure_definition(n:ast):                                               #
#   Creates a new variable in the current environment whose value is a         #
#   procedure type object with a given signature.                              #
#------------------------------------------------------------------------------#
def g_procedure_definition(n):
    # 0: identifier; 1: argument list; 2: suite
    det_type(n[1], file_name)
    sig = n[1].type

    try:
        n.parent.initiate_var(n[0],type_obj("proc",builtins["proc"], sig = sig))

    except SignatureException:
        # Function overloading - duplicate signature
        type_error("The procedure '" + n[0] + "' with the signature '" +
                   repr(sig) + "' has already been defined.", file_name, n[1])

    except DeclarationException:
        type_error("'" + n[0] + "' has already been declared in the current" + 
                   "scope, and is not a function or procedure.\n" +
                   "Only function and procedure definitions are allowed to " + 
                   " have more than one value.", file_name, n)

#------------------------------------------------------------------------------#
# g_class_definition(n:ast):                                                   #
#   Creates a new type in the global environment.                              #
#------------------------------------------------------------------------------#
def g_class_definition(n):
    # 0: identifier; 1: super class; 2: suite

    # Class extension
    if (n[1].label == "EMPTY"):
        sup = builtins["object"]
        n[1].label = "TYPE"
        n[1].children.append("object")
    else:
        det_type(n[1], file_name)
        sup = n[1].type

    # Temporarily initialize the class in the global environment
    # without any methods.  This allows methods in the class to 
    # have local variables whose type is the class
    try:
        n.parent.initiate_var(n[0], type_obj(n[0], builtins["type"], sup = sup))

    except DeclarationException:
        type_error("'" + n[0] + "' has already been declared in the current" + 
                   "scope, and is not a function or procedure.\n" +
                   "Only function and procedure definitions are allowed to " + 
                   " have more than one value.", file_name, n)


    # Get the class attributes  
    det_type(n[2][1][0], file_name)
    attributes = n[2][1][0] 
    if (attributes.label == "EMPTY"): 
        # Empty variable declaration block - no class attributes
        attribute_nodes = []

    else:
        # Nonempty variable declartion block - has class attributes
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
        det_type(m[1], file_name)
        sig = m[1].type
        if m.label == "PROCEDURE_DEFINITION":
            # procedure overloading
            if name in methods.keys():
                if (isinstance(methods[name], list)):
                    # Add the new procedure signature to the class
                    methods[name].append(type_obj("proc", builtins["proc"], sig = sig))

                # First overload
                else:
                    methods[name] = [methods[name], type_obj("proc", builtins["proc"], sig = sig)]
            # Undeclared variable - add it to the class
            else:
                methods[name] = type_obj("proc", builtins["proc"], sig = sig)
        else:
            det_type(m[2], file_name)
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


#------------------------------------------------------------------------------#
# g_forloop_iter(n:ast)                                                        #
#   Generates the environemtn for an iterative for loop containing the         #
#   variable whose name was given in the iterative for loop and whose          #
#   type corresponds to the type of the elements of the iterable.              #
#   NOTE: Tuples are multi-typed. How do you know what type the iterator       #
#         should be? Possible AnyType                                          #
#------------------------------------------------------------------------------#
def g_forloop_iter(n): 
    # 0: identifier; 1: list; 2: suite
    det_type(n[1], file_name)
    iterable = n[1].type

    # Determine the type of the iterative variable based on the container 
    # it's iterating over
    if basetype(iterable) in (builtins["StringType"], builtins["FileType"]):
        id_type = builtins["string"]

    elif basetype(iterable) in containertypes:
          id_type = iterable.elem_type[0]
  
    else:
         # recovering from a type error
         # a type error will be thrown during type checking
         id_type = iterable


    # Add the iterative variable to the loop's environment 
    if (n[2].label == "SUITE_BLOCK"):
         # 0: docstring; 1: block
         n[2][1].initiate_var(n[0], id_type)
 
    if (n[2].label == "SUITE_INLINE"):
         # 0: simple statement
         n[2].initiate_var(n[0], id_type)


#------------------------------------------------------------------------------#
# g_forloop_count(n:ast)                                                       #
#   Generates the environment for a counting for loop. Creates a variable      #
#   inside of the loop whose name is name given and whose type is an integer.  #
#------------------------------------------------------------------------------#
def g_forloop_count(n):
    # 0: identifier; 1: start range; 2: end range; 3: suite
    # The actual types of n[1] and n[2] don't matter right now
    # If they are wrong, a type error will be thrown during type checking

    if (n[3].label == "SUITE_BLOCK"):
        # 0: docstring; 1: block
        n[3][1].initiate_var(n[0], builtins["int"])

    if (n[3].label == "SUITE_INLINE"):
        # 0: simple statement
        n[3].initiate_var(n[0], builtins["int"])


#------------------------------------------------------------------------------#
# g_except_alias(n:ast)                                                        #
#   Creates a variable with the given name and exception type in the scope     #
#   of the except block.                                                       #
#------------------------------------------------------------------------------#
def g_except_alias(n):
    # 0: identifier; 1: alias; 2: suite; 3: extension
    try:
        exception = n.lookup_var(n[0])
    except NotYetDeclaredException:
        pass
    else:
        n.initiate_var(n[1], exception)

     

variables = {
    "DECLARATION_SIMPLE"     : g_declaration,
    "DECLARATION_INITIALIZE" : g_declaration,
    "ARGUMENTLIST_SINGLE"    : g_argumentlist,
    "DEFAULTLIST_SINGLE"     : g_argumentlist,
    "FUNCTION_DEFINITION"    : g_function_definition, 
    "PROCEDURE_DEFINITION"   : g_procedure_definition,
    "CLASS_DEFINITION"       : g_class_definition,
    "FORLOOP_ITER"           : g_forloop_iter,
    "FORLOOP_COUNT"          : g_forloop_count,
    "EXCEPT_ALIAS"           : g_except_alias
}

file_name = ""