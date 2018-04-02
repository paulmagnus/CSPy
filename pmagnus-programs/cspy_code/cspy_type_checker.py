#------------------------------------------------------------------------------#
# cspy_type_checker.py                                                         #
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
# Contains type checking functions for the semantic analysis of a CSPy program.#
#------------------------------------------------------------------------------#
from cspy_data_struct import *
from cspy_builtins import *
from cspy_runtime import remove_files
import sys

#------------------------------------------------------------------------------#
# det_type(astnode)                                                            #
#   Recursively traverses the abstract syntax tree of a CSPy program to        #
#   determinethe type of each node and call the necessary type-checking        #
#   functions.                                                                 #
#------------------------------------------------------------------------------#
def det_type(astnode, file_name):

    global filename
    filename = file_name
    if (not isinstance(astnode, ast)):
        return

    subtree_returns = []
    for child in astnode.children:
        subtree_returns.append(det_type(child, file_name))

    if (astnode.label in checks):
        checks[astnode.label](astnode)

    if astnode.label == "FUNCTION_DEFINITION":
        if not subtree_returns[3]:
            function_return_error(astnode.line, astnode.lineNum,
                                  astnode.children[2].type)

    if (astnode.label in returns):
        return returns[astnode.label](subtree_returns)
    else:
        return False

#------------------------------------------------------------------------------#
# function_return_error(function:string, lineNum:int, function_type:type_obj)  #
#  Displays a function return error when a function does not return a promised #
#  type or fails to return anything when it has a return type.                 #
#------------------------------------------------------------------------------#

def function_return_error(function, lineNum, function_type):
    print >> sys.stderr, "\nCSPy : FunctionTypeError\n"
    print >> sys.stderr, "Line: " + str(lineNum)
    print >> sys.stderr, function
    print >> sys.stderr, "Function must return something of type " + \
        str(function_type) + " in all cases."
    remove_files()
    sys.exit(1)


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
def type_error(message, file_name, *nodes):
    if file_name == "":
        file_name = filename

    result = "\nCSPy : Type Error\n"
    result += "File: " + file_name + "\n"
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
#    environment by traversing the root from n to the root node.               #
#------------------------------------------------------------------------------#
def global_env(n):
    current = n
    while current.parent:
        current = current.parent
    return current


#------------------------------------------------------------------------------#
#                          TYPE-CHECKING FUNCTIONS                             #
#                                                                              #
# The following functions define what action should be taken for each type     #
# of abstract syntax tree node. These functions have a naming format s_[a-z_]+ #
# where the name of the function is the lowercase version of the name of the   #
# type of node it acts upon.   (ex: s_calculation_unaryoperator)               #
#                                                                              #
# The first line of each function is a comment containing a list of the        #
# indices of the node "n" and what they contain (this information is defined   #
# in "cspy_parser.py").                                                        #
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
#                                 VARIABLES                                    #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_variable(n)                                                                #
#  Looks up the type of a variable within its scope. If the variable is        #
#  undeclared, an error occurs. Else, the type of the node is set to the type  #
#  of the variable.                                                            #
#------------------------------------------------------------------------------#
def s_variable(n):
    # 0: identifier
    try:
        typ = n.lookup_var(n[0])

        if n.is_class_var(n[0]):
            n.label = "CLASS_VARIABLE"

    except NotYetDeclaredException:
        type_error("Undeclared variable '" + (n[0]) +"'.", "", n)

    else:
        n.type = typ
        return False

#------------------------------------------------------------------------------#
# s_declaration_initialize(n)                                                  #
#   Checks if the value a variable is initialized to has the same type as      #
#   the variable's declared type.                                              #
#------------------------------------------------------------------------------#
def s_declaration_initialize(n):
    # 0: identifier; 1: type; 2: expression
    if (not n[1].type or not n[2].type):
        # type error handled by s_type
        return                          
    
    if (n[1].type != n[2].type):
        type_error("The value assigned to '" + n[0] + "' must have type '" + 
                   repr(n[1].type) + "', not type '" + repr(n[2].type) + "'.",
                   "", n[1], n[2])


#------------------------------------------------------------------------------#
# s_assignment(n)                                                              #
#   Checks two kinds of assignment - normal (using '=') and augmented          #
#   assignment (eg '+='). For normal assignment, checks the the                #
#   variable on the LHS has the same type as the expression being assigned to  #
#   it on the RHS.                                                             #
#                                                                              #
#   For augmented assignment, checks that the type of the variable and the     #
#   expression on the lhs both have methods corresponding to the binary        #
#   operator being used in the augmented assignment and that their             #
#   signatures match.                                                          #
#------------------------------------------------------------------------------#
def s_assignment(n):
    # 0: variable; 1: assignment operator; 2: expression

    if n[2].label == "LITERAL_NONE":
        if n[0].type.type_str in builtins:
            type_error("The value assigned to the variable '" + n[0][0] 
                       + "' cannot be set to None.", "",
                       n[0], n[2])



    # Variable is undeclared or the expression had a type error
    if (not n[2].type or not n[0].type):
        return

    # Normal assignment 
    if (n[1] == "="):

        # Binding a variable to an overloaded function  
        if isinstance(n[2].type, list) and n[2].label == "VARIABLE":
            valid = filter(lambda f: f == n[0].type, n[2].type)
            if not valid:
                type_error("The overloaded function '" + n[2][0] + 
                           "' is not defined with the type signature " +
                           "", repr(n[0].type) + ".", n[0], n[2])
 
        # Binding the wrong type to a variable
        elif (n[0].type != n[2].type):
            type_error("The value assigned to the variable '" + n[0][0] 
                       + "' must have type '"+ str(n[0].type) + "'.", "",
                       n[0], n[2])


    # Immutable types do not support augmented assignment
    elif basetype(n[0].type) in (builtins["TupleType"], 
                                 builtins["FrozenSetType"]):
        type_error("'" + repr(n[0].type) + "' is immutable and does not" +
                   " support augmented assignment.", "", n[0])


    # Augmented assignment
    else:
        orig = n[1] 
        n[1] = orig[:len(orig) - 1] # binary operator
        binaryop(n)
        n[1] = orig


#------------------------------------------------------------------------------#
# s_member(n)                                                                  #
#   Attempts to look up member on object type and sets the type of the node    #
#   to the type of the member (which is an attribute or method) if the member  #
#   exists for the object type.                                                #
#     eg) l.append(1) will look up the 'append' method for the type of l (list)#
#------------------------------------------------------------------------------#
def s_member(n):
    # 0: object; 1: attribute terminal   
    typ = n[0].type    # class
    attr = n[1]        # name of attribute

    if typ.type == builtins["proc"].type or \
            typ.type == builtins["fn"].type:
        # typ has been given the type of the class constructor instead
        # of the class
        top = global_env(n)

        try:
            typ = top.lookup_var(n[0][0])
        except NotYetDefinedException:
            type_error("'" + repr(typ)+ "' object has no '" + attr + 
                    "' attribute defined.", "", n[0])
    
    member = typ.lookup_method(attr)
    if member:
        # Overloaded method
        if len(member) > 1:
            n.type = member

        # Normal attribute or non-overloaded method
        else:
            n.type = member[0]
    else:
         type_error("'" + repr(typ)+ "' object has no '" + attr + 
                    "' attribute defined.", "", n[0])


#------------------------------------------------------------------------------#
# s_membership                                                                 #
#  Checks that the container supports membership testing.                      #
#------------------------------------------------------------------------------#
def s_membership(n):
    # 0 : object 1: container
    member = n[0].type
    container = n[1].type

    # eg. 4 in 4 is illegal
    if basetype(container) not in sequencetypes:
        type_error("Type '" + repr(container) + "' does not support " +
                   "membership testing.", "", n[1])

    # eg. 1.0 in [1,2,3]
    elif (container is not builtins["string"]) and \
         (member not in container.elem_type):
        type_error("Membership testing for '" + repr(member) + 
                   "' in '" + repr(container) + "'.", "", n[0], n[1])

    # eg. 4 in "1 2 3 4" illegal
    elif (basetype(container) is builtins["StringType"]) and (basetype(member) is not builtins["StringType"]):
        type_error("Membership testing for '" + repr(member) + 
                   "' in '" + repr(container) + "'.", "", n[0], n[1])
        

    else:
        n.type = builtins["bool"]

#------------------------------------------------------------------------------#
# s_identity                                                                   #
#   Checks that the two objects being compared have the same type.             #
#------------------------------------------------------------------------------#
def s_identity(n):
    if n[1].label == "LITERAL_NONE":
        if n[0].type.type_str in builtins:
            type_error("The value assigned to the variable '" + n[0][0] 
                       + "' cannot be set to None.", "",
                       n[0], n[1])
        else:
            n.type = builtins["bool"]
            return

    # 0: lhs  1: rhs
    if n[0].type != n[1].type:
        type_error("Identity testing for '" + repr(n[1].type) + "' type" + 
                   " with '" + repr(n[0].type) + "' type.", "", n[0], n[1])
    else:
        n.type = builtins["bool"]


#------------------------------------------------------------------------------#
#                                    TYPES                                     #
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
# s_type(n:ast)                                                                #
#   Assigns the type of a type literal.                                        #
#------------------------------------------------------------------------------#
def s_type(n):
    # 0: type

    if(isinstance(n[0], str)):
        globalnode = global_env(n)
        globalenv = globalnode.env

        try:
            # Lookup the type identifier
            typ = n.lookup_var(n[0])

        except NotYetDeclaredException:
            # Identifier undeclared
            type_error("'" + n[0] + "' is not a declared type.", "", n)

        else:
            # Identifier is not a type
            if not is_type(typ):

                # Prevents user types (classes) from receivng the type 
                # of their constructors (procedure type) inside of a class
                # definitions
                if n[0] in globalenv and is_type(globalnode.lookup_var(n[0])):
                    n.type = globalnode.lookup_var(n[0])

                else:
                    type_error("'" + n[0] + "' is declared, but it is not a " +
                               "type.", "", n)
            else:
                n.type = typ
    else:
        # Take the type of its child node
        n.type = n[0].type


#------------------------------------------------------------------------------#
# s_typelist(n)                                                                #
#   Creates a signature object from  a list of types for the parameters of     #
#   a funciton type literal or a procedure type literal.                       #
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
    n.type = init_set([n[0].type])



#------------------------------------------------------------------------------#
# s_frozenset_type(n:ast)                                                      #
#   Sets the type of a frozenset to a frozenset type object.                   #
#------------------------------------------------------------------------------#
def s_frozenset_type(n):
    n.type = init_frzset([n[0].type])



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
#   Sets the type of a generator type object                                   #
#------------------------------------------------------------------------------#
def s_generator_type(n):
    # 0: type
    n.type = init_generator([n[0].type])



#------------------------------------------------------------------------------#
# s_member_type(n:ast)                                                         #
#   Sets the type of a member type object.                                     #
#------------------------------------------------------------------------------#
def s_member_type(n):
    # 0: IDENTIFIER # 1: IDENTIFIER
    try:
        # Lookup the type identifier
        module = n.lookup_var(n[0])
    except NotYetDeclaredException:
        # Identifier undeclared
        type_error("'" + n[0] + "' is not declared.", "", n)

    attr = n[1]       # type

    if attr in module.methods:
        member = module.methods[attr]
        if isinstance(member, list):
            # Overloaded method - not a type
            type_error("'" + n[0] + "." + 
                       attr + "' is a function or procedure, not a type.",
                       "", n)
        else:
            if is_type(member):
                n.type = member
            else:
                type_error("'" + n[0] + "." +attr + "' is not a type.", "", n)
    else:
        type_error("'" + n[0] + "' object has no '" + attr +
                   "' attribute defined.", "", n)

#------------------------------------------------------------------------------#
#                               LITERAL TYPES                                  #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_literal_int(n:ast)                                                         #
#   Assigns 'int' type to an int literal.                                      #
#------------------------------------------------------------------------------#
def s_literal_int(n):
    # 0: terminal
    n.type = builtins["int"]



#------------------------------------------------------------------------------#
# s_literal_float(n:ast)                                                       #
#   Assigns 'float' type to a float literal.                                   #
#------------------------------------------------------------------------------#
def s_literal_float(n):
    # 0: terminal
    n.type = builtins["float"]



#------------------------------------------------------------------------------#
# s_literal_bool(n:ast)                                                        #
#   Assigns 'bool' type to a bool literal.                                     #
#------------------------------------------------------------------------------#
def s_literal_bool(n):
    # 0: terminal
    n.type = builtins["bool"]



#------------------------------------------------------------------------------#
# s_literal_string(n:ast)                                                      #
#   Assigns 'string' type to a string literal.                                 #
#------------------------------------------------------------------------------#
def s_literal_string(n):
    # 0: terminal
    n.type = builtins["string"]



#------------------------------------------------------------------------------#
# s_literal_list(n:ast)                                                        #
#   Assigns 'list' type to a list literal.                                     #
#------------------------------------------------------------------------------#
def s_literal_list(n):
    # 0: expression list
    elements = n[0].flatten("EXPRESSIONLIST_SINGLE")

    # empty list
    if not elements:
        n.type = init_list([])
     
    # nonempty list
    else:
        listtype = elements[0].type
        bad_elements = filter(lambda e: listtype != e.type, elements)

        # Heterogenous list
        if bad_elements:
            bad_types = [e.type for e in bad_elements]
            type_error("List of '" + repr(listtype) + "' type contains '" + 
                   listTostr(bad_types) + "' type. \nAll elements " + 
                   "of a list must be the same type.", "",
                   * bad_elements)
        else:
            # Homogeneous list
            n.type = init_list([listtype])



                   
#------------------------------------------------------------------------------#
# s_literal_tuple(n:ast)                                                       #
#   Assigns 'tuple' type to a tuple literal.                                   #
#------------------------------------------------------------------------------#
def s_literal_tuple(n):
    # 0: terminal
    single = n[0].flatten("TUPLE_SINGLE")
    multi = n[0].flatten("EXPRESSIONLIST_SINGLE")
    elements = single if single else multi

    # empty tuple
    if not elements:
        n.type = init_tuple([])

    # non-empty tuple
    else:
        tuple_types = [e[0].type for e in elements]
        n.type = init_tuple(tuple_types)




#------------------------------------------------------------------------------#
# s_literal_set(n:ast)                                                         #
#   Assigns 'set' type to a set literal.                                       #
#------------------------------------------------------------------------------#
def s_literal_set(n):
    # 0: expression list

    # literal sets cannot be nonempty -> { } is a dictionary literal
    members = n[0].flatten("EXPRESSIONLIST_SINGLE")
    settype = members[0].type

    bad_members = filter(lambda m: settype != m.type, members)
    
    # heterogenous set
    if bad_members:
        bad_types = [m.type for m in bad_members]
        type_error("Set of '" + repr(settype) + "' type contains '" + 
                   listTostr(bad_types) + "' type. \nAll members " + 
                   "of a set must be the same type.", "",
                   * bad_members)

    else:
        # homogeneous set
        n.type = init_set(settype)    



#------------------------------------------------------------------------------#
# s_literal_dictionary(n:ast)                                                  #
#   Assigns 'dictionary' type to a dictionary literal.                         #
#------------------------------------------------------------------------------#
def s_literal_dictionary(n):
    # 0: dictionary list
    dict_entries = n[0].flatten("DICTIONARYLIST_SINGLE") # 0: key; 1: value

    # empty dictionary
    if not dict_entries:
        n.type = init_dict([])

    else:
        # nonempty dictionary
        keys = [e[0] for e in dict_entries]
        values = [e[1] for e in dict_entries]
        key_types = [k.type for k in keys]
        values_types = [v.type for v in values]

        
        keys_homogeneous = not(False in [key_types[0] == kt \
                                         for kt in key_types])
        values_homogeneous = not(False in [values_types[0] == vt \
                                           for vt in values_types])

       # homogeneous dictionary
        if (keys_homogeneous and values_homogeneous):
            n.type = init_dict([key_types[0], values_types[0]])
 
       # type error for nonhomogenous dictionary
        else:
            if not keys_homogeneous:
                bad_keys = filter(lambda k: not key_types[0] == k.type, keys)
                bad_types = [k.type for k in bad_keys]
                error = "Dictionary with key type '" + repr(key_types[0]) + \
                    "' contains key(s) of" + listTostr(bad_types) + \
                    " type.\nThe keys in a dictionary must be the same type."
                type_error(error, "", * bad_keys)

            if not values_homogeneous:
                    bad_values = filter(lambda v: not values_types[0] == v.type,
                                        values)
                    bad_types = [v.type for v in bad_values]
                    type_error("Dictionary with value type '" 
                               + repr(values_types[0]) + 
                               "' contains value(s) of" + listTostr(bad_types) +
                               " type.\nThe values in a dictionary must be " +
                               "the same type.", "", * bad_values)




#------------------------------------------------------------------------------#
# s_literal_function(n)                                                        #
#   Checks the types of a function literal (i.e. lambda expression).           #
#   Ensures the return type of the function matches the type of the body.      #
#   Sets the type of the literal function node to a 'fn' type object           #
#   with the approriate function signature.                                    #
#------------------------------------------------------------------------------#
def s_literal_function(n):
    # 0: arguments; 1: return type; 2: expression

    # Lambda return type does not match the type of its body
    if (n[2].type != n[1].type):
        type_error("The anonymous function with return type '" + 
                   repr(n[1].type) + "' contains a body with type '" + 
                   repr(n[2].type) + "'.\nThe body of an anonymous function" +
                   " must have the specified return type.", "",
                   n[1], n[2])

    # Function signature
    sig = n[0].type
    sig.return_type = n[1].type
    n.type = type_obj("fn", builtins["fn"], sig = sig)





#------------------------------------------------------------------------------#
#                                 FUNCTIONS                                    #
#------------------------------------------------------------------------------#



#------------------------------------------------------------------------------#
# signatureMatch(sigs:list of type_obj, callparams: list of type_obj, t:string)#
#                -> tuple of type_obj * type_obj                               #
#   A helper function for s_procedure call and s_function call.                #
#   Creates a call signature from the parameter types and finds the type_obj   #
#   in sigs whose signature matches the call signature.                        #
#   returns -> (call signature, match if found)                                #
#------------------------------------------------------------------------------#
def signatureMatch(sigs, callparams, t):
    call_sig = type_obj(t, builtins[t], 
                        sig = signature(params = callparams))

    match = filter(lambda s : callmatch(s, call_sig), sigs)

    if match == []:
        # check for superclass matching
        for i in range(len(callparams)):
            if callparams[i].super:
                sup_callparams = []
                for j in range(len(callparams)):
                    if j != i:
                        sup_callparams.append(callparams[j])
                    else:
                        sup_callparams.append(callparams[j].super)
                rec_call_sig, rec_match = signatureMatch(sigs,
                                                         sup_callparams,
                                                         t)
                if rec_match:
                    # match found, return match
                    return rec_call_sig, rec_match
        
        return call_sig, None

    else:
        return call_sig, match[0]




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
# s_function_definition(n)                                                     #
#   Checks that the type of all the return statements in a function defintion  #
#   match the function return type as specified in the function declaration.   #
#------------------------------------------------------------------------------#
def s_function_definition(n):
    # 0: identifier; 1: argument list; 2: return type; 3: suite
    returns = n.flatten("RETURN")

    # missing return statment
    if not returns:
        yields = n.flatten("YIELD")
        if not yields:
            type_error("The function definition of '" + n[0] + "', whose return " +
                       "type is '" +  repr(n[2].type) + "', must contain a " + 
                       "return statement.", "", n)

    # empty return statement
    empty_returns = filter(lambda r: r.type == None, returns)
    if empty_returns:
        type_error("The function definition of '" + n[0] + "', whose return " +
                   "type is '" +  repr(n[2].type) + "', contains empty " + 
                   "return statement(s).", "", * empty_returns)
        
    
    # return statement whose type does not match the function return type
    bad_returns = filter(lambda r: r.type != n[2].type, returns)
    if bad_returns:
        wrong_types = [r.type for r in bad_returns]
        type_error("The function definition of '" + n[0] + "', whose return " +
                   "type is '" +  repr(n[2].type) + "', contains return "
                   "statement(s) of type" + listTostr(wrong_types) + ".", "",
                   n[2], * bad_returns)




#------------------------------------------------------------------------------#
# s_function_call(n)                                                           #
#   Determines the signature of a function call from its parameters and        #
#   looks up the value of the function indentifier. If the function            #
#   indentifier has multiple values (i.e function overloading),                #
#   the function with the matching type signature to the call signature        #
#   is found. The type of the function call node is set to the return          #
#   type of the function.                                                      #
#------------------------------------------------------------------------------#
def s_function_call(n):

    # 0: function; 1: parameters
    try:
        # class method eg) mylist.append(1), name = append
        name = n[0][1]
    except IndexError:
        # normal function 
        name = n[0][0]
    
    fn = n[0].type
    call_params = [t.type for t in n[1].flatten("EXPRESSIONLIST_SINGLE")]

    # Undeclared function - error handled by s_variable
    if not fn:
        return
  
    # built-in function (signature depends on parameters eg. map, filter)
    if callable(fn):
        fn, error = fn(call_params)
        if not fn:
            n[0].type = None
            type_error(error, "", n[0])
        else:
            n[0].type = fn

    fn = fn if isinstance(fn, list) else [fn]
    uncallable = filter(lambda f: not is_callable(f), fn)

    if uncallable:
        # constructor is a special type - not a function or a procedure
        print fn
        print basetype(fn[0])
        if usertype(fn[0]):
            # Check if it is a python constructor call
            if n.is_python(name):
                n.label = "PYTHON_CONSTRUCTOR_CALL" # necessary for translator
                n[0].type = fn[0].lookup_method(name)
                n.type = fn[0]
                s_procedure_call(n)
                return

            n.label = "CONSTRUCTOR_CALL" # necessary for translator
            n[0].type = fn[0].lookup_method(name)
            n.type = fn[0]
            s_procedure_call(n)
            return
           
        elif is_exception(fn[0]):
            n.label = "PYTHON_CONSTRUCTOR_CALL"
            n[0].type = fn[0].lookup_method(name)
            n.type = fn[0]
            s_procedure_call(n)
            return
        else:
            type_error("'" + name + 
                           "' is not a function and cannot be called.", "", n[0])
    else:
        callsig, match = signatureMatch(fn, call_params,  "fn")
        n[1].type = callsig

        if not match:
            type_error("The function '" + name + 
                       "' with the type signature '" + 
                       repr(callsig.sig) + "' is not defined.", "",
                       n[0], n[1]) 

        elif match.type != builtins["fn"]:
            type_error("'" + name + 
                       "' is a procedure and does not return a value.", "",
                       n[0])

        else:
            if n.is_python(name):
                n.label = "PYTHON_FUNCTION_CALL"
            elif n.is_class_var(name):
                n.label = "CLASS_FUNCTION_CALL"
            n.type = match.sig.return_type



#------------------------------------------------------------------------------#
# s_return(n)                                                                  #
#   Sets the type of return statement node the type of its child (the value    #
#   being returned).                                                           #
#------------------------------------------------------------------------------#
def s_return(n):
    # 0: expression
    n.type = n[0].type



#------------------------------------------------------------------------------#
# s_yield(n)                                                                   #
#   Sets the type of return statement node to a generator of its child (the    #
#   value being returned)                                                      #
#------------------------------------------------------------------------------#
def s_yield(n):
    #0: expression
    n.type = init_generator([n[0].type])



#------------------------------------------------------------------------------#
# s_procedure_type(n)                                                          #
#   Sets the type of a procedure type literal (eg. proc (string)) to a new     #
#   'proc' type object.                                                        #
#------------------------------------------------------------------------------#
def s_procedure_type(n):
    # 0: parameters
    n.type = type_obj("proc", builtins["proc"], sig = n[0].type)




#------------------------------------------------------------------------------#
# s_procedure_definition(n)                                                    #
#   Checks to make sure that all of the return statements in a procedure       #
#   are empty.                                                                 #
#------------------------------------------------------------------------------#
def s_procedure_definition(n):
    # 0: identifier; 1: argument list; 2: suite
    rets = n.flatten("RETURN")

    # all return statements must be empty
    nonempty = filter(lambda r : r.type != None, rets)
    if nonempty:
         type_error("Non-empty return statement(s). A procedure cannot return a"
                    + " value.", "", * nonempty)




#------------------------------------------------------------------------------#
# s_procedure_call(n)                                                          #
#   Determines the procedure type signature of a procedure call based on the   #
#   types of its argument list.  If the procedure identifier has multiple      #
#   procedures associated with it (i.e function overloading), the procedure    #
#   whose signature matches the call signature is found. Type error            #
#   if it cannot find a procedure whose name is identifier with the matching   #
#   type signature of the procedure call.                                      #
#------------------------------------------------------------------------------#
def s_procedure_call(n):
    # 0: procedure; 1: parameters

    try:
        # procedure is a class method
        name = n[0][1]
    except IndexError:
        # normal procedure call
        name = n[0][0]

    proc = n[0].type
    params = [t.type for t in n[1].flatten("EXPRESSIONLIST_SINGLE")]

    # Undeclared function - error handled by s_variable
    if not proc:
        return
  
    # builtin in procedure
    if callable(proc):
        proc, error = proc(params)
        if not proc:
            n[0].type = None
            type_error(error, "", n[0])

        else:
            n[0].type = proc

    proc = proc if isinstance(proc, list) else [proc]
    uncallable = filter(lambda p: not is_callable(p), proc)

    if uncallable:
        type_error("'" + name + 
                           "' is not a procedure and cannot be called.", "", n[0])
    else:

        callsig, match = signatureMatch(proc, params,  "proc")
        n[1].type = callsig
        if not match:
            type_error("The procedure '" + name + 
                       "' with the type signature '" + 
                       repr(callsig.sig) + "' is not defined.", "",
                       n[0], n[1]) 
        else:
            if match.type != builtins["proc"] and n.label != "CONSTRUCTOR_CALL":
                type_error("The return value of a function call must be used" + 
                           " in an assignment or other operation.", "", n[0])

            # check if the procedure is from a python import
            if n.is_python(name):
                n.label = "PYTHON_PROCEDURE_CALL"

            if n.is_class_var(name):
                n.label = "CLASS_PROCEDURE_CALL"

            # check if procedure is a super constructor
            # check if procedure is a member
            if n[0].label != "MEMBER":
                return

            # check if member and method have the same name
            if n[0][0][0] != n[0][1]:
                return

            # find class definition if there is one
            node = n
            while node.label != "FILE" and node.label != "CLASS_DEFINITION":
                node = node.parent
            if node.label == "FILE":
                return
            
            # check if class has a superclass
            if node[1].label == "EMPTY":
                return

            sup = node[1].type

            while sup.type_str != n[0][1] and sup.super:
                sup = sup.super

            if sup.type_str == n[0][1]:
                n.label = "SUPER_CONSTRUCTOR"

            if n.is_python(name) or name in builtins:
                n.label = "PYTHON_SUPER_CONSTRUCTOR"


#------------------------------------------------------------------------------#
#                                   OPERATORS                                  #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# binaryop(n:ast)                                                              #
#   Helper function for s_calculation_binary and s_assignment (augmented       #
#   assignment).                                                               #
#   Checks to see if the left hand side of the operator has the binary         #
#   operator defined and that the right hand side matches its signature.       #
#   Checks to see if the right hand side of the operator has the binary        #
#   operator defined and that the left hand side matches its signature.        #
#   Type error occurs if either the LHS or the RHS does not have the           #
#   binary operator defined, the operators do not have the right signature,    #
#   or if the binary operator is not defined for both the LHS and the RHS.     #
#------------------------------------------------------------------------------#
def binaryop(n):
    # 0: left-hand side; 1: operator; 2: right-hand side
    op = n[1]           # operator
    lhs = n[0].type     # type of left-hand side
    rhs = n[2].type     # type of right-hand side

    name = op
    try:
        name = binary_overload[op]
    except KeyError:
        pass


    # Check to see if the type of the LHS and RHS have the binary 
    # operator defined
    Loperator = lhs.lookup_method(name)
    Roperator = rhs.lookup_method(name)
    callsig, Lmatch = signatureMatch(Loperator, [rhs], "fn")
    callsig, Rmatch = signatureMatch(Roperator, [lhs], "fn")
      
    if Loperator:
        if not Lmatch:
            type_error("The binary operator '" + op + "' is defined for the " +
                       "left-hand side (" + repr(lhs) + "), but it does not " + 
                       "have a signature matching the right-hand side ("
                       + repr(rhs) + ")." , "", n[0], n[2])

        
    if Roperator:
        if not Rmatch:
           type_error("The binary operator '" + op + "' is defined for the " +
                      "right-hand side (" + repr(rhs) + "), but it does not " +
                      "have a signature matching the left-hand side ("
                       + repr(lhs) + ")." , "", n[0], n[2])
           
           
            

    # Operator is defined for neither the RHS nor the LHS 
    if not Loperator or not Roperator:
        type_error("The binary operator \"" + op + "\" is not defined " +
                    "for type '" + repr(lhs) + "' and type '" + 
                   repr(rhs) + "'.", "", n[0], n[2])
        
    else: 
        # Operator is defined for both the LHS and RHS and have the correct
        # signatures
        
        # Tuple binary operators - *, + : have to determine the return type
        # from the element types in the tuple(s)
        #   eg. tuple of (int * string) + tuple of (int) = 
        #       tuple of (int * string * int)
        bases = [basetype(lhs), basetype(rhs)]

        if (builtins["TupleType"] in bases) and (n[1] == "+" or n[1] == "*"):
            n.type = tuplebinary(n[1], n[0], n[2])
        else:
            n.type = Lmatch.sig.return_type
        

#------------------------------------------------------------------------------#
# tuple_binary(op:string, lhs:ast, rhs:ast) -> type_obj                        #
#   Returns the type resulting from a tuple binary operation (+ or *).         #
#------------------------------------------------------------------------------#
def tuplebinary(op, lhs, rhs):
    if op == "+":
        return tuple_add(lhs, rhs)
    else:
        return tuple_mult(lhs, rhs)



#------------------------------------------------------------------------------#
# tuple_mult(lhs:ast, rhs:ast) -> type_obj                                     #
#   Returns the type resulting from the binary operation * where one operand   #
#   is a tuple and the other is an int.                                        #
#------------------------------------------------------------------------------#
def tuple_mult(lhs, rhs):
    if lhs.type == builtins["int"]:
        try:
            multiplier = int(lhs[0])
        except ValueError:
            type_error("Tuple multiplier must be integer literal.", "", lhs)
            
        tup = rhs.type
    else:
        try:
            multiplier = int(rhs[0])
        except ValueError:
            type_error("Tuple multiplier must be integer literal.", "", rhs)

        tup = lhs.type

    newtype = tup.elem_type * multiplier
    return init_tuple(newtype)



#------------------------------------------------------------------------------#
# tuple_add(lhs:ast, rhs:ast) -> type_obj                                      #
#   Returns the type resulting from the binary operation + where both          #
#   opearands are tuples.                                                      #
#------------------------------------------------------------------------------#
def tuple_add(lhs, rhs):
    types = lhs.type.elem_type + rhs.type.elem_type
    return init_tuple(types)
    


#------------------------------------------------------------------------------#
# s_calculation_binaryoperator(n)                                              #
#   Checks to see if the left hand side of the operator has the binary         #
#   operator defined and that the right hand side matches its signature.       #
#   Checks to see if the right hand side of the operator has the binary        #
#   operator defined and that the left hand side matches its signature.        #
#   Type error occurs if either the LHS or the RHS does not have the           #
#   binary operator defined, the operators do not have the right signature,    #
#   or if the binary operator is not defined for both the LHS and the RHS.     #
#------------------------------------------------------------------------------#
def s_calculation_binaryoperator(n):
    if n[2].label == "LITERAL_NONE" and (n[1] == "==" or n[1] == "!="):
        if n[0].type.type_str in builtins:
            type_error("The value assigned to the variable '" + n[0][0] 
                       + "' cannot be None.", "",
                       n[0], n[2])
        else:
            # a == None
            n.type = builtins["bool"]

    if n[0].label == "LITERAL_NONE" and (n[1] == "==" or n[1] == "!="):
        type_error("None should appear after the operator '" + n[1] + "'.", "",
                   n[0], n[2])

    # type error on either the lhs or rhs 
    if not n[0].type or not n[2].type:
        return

    else:
        binaryop(n)
    

#------------------------------------------------------------------------------#
# s_calculation_unaryoperator(n)                                               #
#   Checks the type of the operand to see if the type has the unary operator   #
#   defined.  Type errors if the unary operator is undefined for the operand   #
#   or if it is defined, but is not a function.                                #
#------------------------------------------------------------------------------#
def s_calculation_unaryoperator(n):
    # 0: operator; 1: parameter
    op = n[0]           # operator
    rhs = n[1].type     # type of right-hand side
    name = unary_overload[op]

    operator = rhs.lookup_method(name)

    # Unary opertaor is not defined for the type
    if not operator:
        type_error("The unary operator \'" + op + "' is not " +
                   "defined for this type.", "", n[1])

    else:
        operator = operator[0]
        # Operator is defined but is not a function 
        if (not is_callable(operator)):
              type_error("The unary operator '" + op + "\' is not" +
                       " defined for this type, but it is not a function.", "",
                         n[1])
        else:
            # Operator is defined for this type
            n.type = operator.sig.return_type


#------------------------------------------------------------------------------#
#                                CONDITIONALS                                  #
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
# s_conditional(n)                                                             #
#   Checks to see if the condition of an if/elif statement is a boolean        #
#   expression.                                                                #
#   NOTE: Python's truth testing system allows other types to be               #
#   used in conditionals. Possible modification in the future.                 #
#------------------------------------------------------------------------------#
def s_conditional(n):
    # 0: condition; 1: suite; 2: extension
    if(n[0].type != builtins["bool"]):
        type_error("The condition of an if statement must be a boolean.", 
                   "", n[0])

    
#------------------------------------------------------------------------------#
# s_ternary(n)                                                                 #
#   Checks to see if the condition of the ternary operator is a boolean        #
#   expression. Makes sure that the if-then expression has the same type       #
#   of the else expression. Assigns the type of the ternary node to a          #
#   type object whose type is the type of the two resultant expressions.       #
#------------------------------------------------------------------------------#
def s_ternary(n):
    # 0: condition; 1: expression; 2: expression
    if(n[0].type != builtins["bool"]):
        type_error("The condition of the ternary operator must be a " +
                   "boolean expression.", "", n[0])
        return

    if(n[1].type != n[2].type):
        type_error("The second and third operands of the ternary operator " +
                   "must have the same type.", "", n[1], n[2])
        return

    n.type = n[1].type


#------------------------------------------------------------------------------#
#                                   LOOPS                                      #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_whileloop(n)                                                               #
#   Checks to see if the condtion of a while loop is a boolean expression.     #
#   NOTE: Python's truth testing system allows for multiple types to be used   #
#         in truth testing. Possible modification in the future.               #
#------------------------------------------------------------------------------#
def s_whileloop(n):
    # 0: condition; 1: suite
    if (n[0].type != builtins["bool"]):
        type_error("The condition of a while loop must be a boolean" + 
                   " expression.", "", n[0])


#------------------------------------------------------------------------------#
# s_forloop_iter(n)                                                            #
#   Type errors if the object in the for loop is not iterable.                 #
#   NOTE: Will need to be modified in the future to account for user defined   #
#         types who support iteration.
#------------------------------------------------------------------------------#
def s_forloop_iter(n):
    # 0: identifier; 1: type; 2: iterable 3; suite 
    if (basetype(n[1].type) not in iterabletypes):
        type_error("Type '" + repr(n[1].type) + "' is not iterable.", "", n[2])
   


#------------------------------------------------------------------------------#
# s_forloop_count(n)                                                           #
#   Makes sure that the type of the start and stop values are integers.        #
#------------------------------------------------------------------------------#
def s_forloop_count(n):
    # 0: identifier; 1: start range; 2: stop range; 3: suite
    if (n[1].type != builtins["int"]) or (n[2].type != builtins["int"]):
        type_error("The starting and ending values for the range of a counting"+
                   " for loop must both be integers.", "", n[1], n[2])    

#------------------------------------------------------------------------------#
#                                  TRY EXCEPT                                  #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_except_specific(n)                                                         #
#  For 'except ValueError', checks to make sure ValueError is defined and is   #
#  an exception type.                                                          #
#------------------------------------------------------------------------------#
def s_except_specific(n):
    # 0: exception; 1: suite; 2: except list
   try:
       exception = n.lookup_var(n[0])

   except NotYetDeclaredException:
       type_error("Undeclared exception type '" + n[0] + "'.", "", n)

   else:
       if not is_exception(exception):
            type_error("'" + n[0] + "' is not an exception.", "", n)


#------------------------------------------------------------------------------#
# s_except_alias(n)                                                            #
#   For 'except ValueError as v', checks to make sure ValueError is defined    #
#   and is an exception type.                                                  #
#------------------------------------------------------------------------------#
def s_except_alias(n):
    # 0: exception; 1: alias; 2: suite; 3: except list
    try:
        exception = n.lookup_var(n[0])

    except NotYetDeclaredException:
        type_error("Undeclared exception type '" + n[0] + "'.", "", n)

    else:
        if not is_exception(exception):
             type_error("'" + n[0] + "' is not an exception.", "", n)

def s_raise(n):
    # 0: exception

    if isinstance(n[0], ast):
        if n[0].label == "EMPTY":
            return

        # 0: constructor call
        exception_class = n[0].type
        if not is_exception(exception_class):
            type_error("'" + n[0] + "' is not an exception.", "", n)
        return

    try:
        exception = n.lookup_var(n[0])
    
    except NotYetDeclaredException:
        type_error("Undeclared exception type '" + n[0] + "'.", "", n)
    
    else:
        # if basetype(exception) != builtins["ExceptionType"]:
        if not is_exception(exception):
            type_error("'" + n[0] + "' is not an exception.", "", n)
        

#------------------------------------------------------------------------------#
#                              INDEXING & SLICING                              #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# s_indexing(n)                                                                #
#   Looks up the '__getitem__' method for the container being indexed. If the  #
#   method is undefined, a type error occurrs. Else, the type of index is      #
#   checked against the signature of the '__getitem__' method to ensure        #
#   the index is the right type (eg. is an integer).                           #
#   Sets the type of the indexing node to the return type of the indexing      #
#   function.                                                                  #
#   NOTE: For tuples, which can contain multiple types, the type of the        #
#         indexing node is not set to the return type of the indexing function #
#         (the return type is a generic 'object'). Instead, the proper return  #
#         type is determined from the type of the tuple by indexing its        #
#         element type list.                                                   #
#------------------------------------------------------------------------------#
def s_indexing(n):
    # 0: container; 1: index
    container = n[0].type
    index = n[1].type
    
    fn = container.lookup_method("__getitem__") 
    if not fn:
        # Undefined index operator for the container
        type_error("The indexing operator is not defined for '" + 
                   repr(container) + "' type.", "", n[0])
   
    else:
        fn = fn[0]
        index_type = fn.sig.param_types[0]

        #  Index operator is defined - check if the index is the correct type
        if index_type != index:
            
            # Lists, tuples, string indices must all by integers
            if basetype(container) in (builtins["ListType"], 
                                       builtins["TupleType"],
                                       builtins["StringType"]):
                type_error(container.type_str.title() + " indices must be " + 
                           "integers, not type '" + repr(index) + "'.", "",
                           n[0], n[1])

            # Dictionary key must have the corret key type
            elif basetype(container) is builtins["DictType"]:
                type_error("The key for '" + repr(container) + "' must have " +
                           "type '" + repr(container.elem_type[0]) + "', not " +
                           "type '" + repr(index) + "'.", "", n[0], n[1])

            # User defined class you can index
            else:
                type_error("The indexing operator is defined for '" + 
                           repr(container.type) + "type, but its indices must" +
                           "have type '" + repr(index_type) + "', not '" +
                           repr(index) + "' type.", "", n[0], n[1])

        # Indexing tuples - return the type of the element at index 
        elif container.type is builtins["tuple"]:
            try:
                tuple_index = int(n[1][0])
            except ValueError:
                type_error("'tuple' type index must be an integer literal, " + 
                           "not an identifier.", "", n[1])
                

            try:
              n.type = container.elem_type[tuple_index]  
            except IndexError:
                # index out of range
                type_error("'" + repr(container) + "' index out of range.", "",
                           n[1])

        else:
            # Return type of the indexing operator
            n.type = fn.sig.return_type

#------------------------------------------------------------------------------#
# s_slicing(n)                                                                 #
#   First, determines the signature of the slicing operation based off which   #
#   slicing arguments are present - start, stop, and step. Then, looks up the  #
#   slice method (__getslice__) for the container type.  Type errors if the    #
#   method is not defined. If the method is defined, checks to see if the      #
#   slicing indices have proper signature (eg. are integers).  Type errors     #
#   if they are not. If the method is defined and the indices have the         #
#   correct signature, the type of slicing node is set to the return type      #
#   of the slicing method.                                                     #
#   NOTE: As with indexing, for tuples which can contain multiple types,       #
#         the return type of the slicing method is a generic 'object' type.    #
#         The proper return type of the slicing method is determined by        #
#         by slicing the tuple's list of element types.                        #
#------------------------------------------------------------------------------#
def s_slicing(n):
    # 0: container; 1: start index; 2: end index; 3: step
    container = n[0].type    # container type
    sss = [n[1], n[2], n[3]] # start, stop, step


    fn = container.lookup_method("__getslice__")
    # Container type does not support slicing
    if not fn:
        type_error("The slicing operation is not defined for '" + 
                   repr(container) + "' type.", "", n[0])

    else:
        # Determine the types of the slicing operands if they exist
        sss = filter(lambda s : s.label != "EMPTY", sss)
        sss_types = map(lambda t: t.type, sss)
        # Container type supports slicing
        call_sig, match = signatureMatch(fn, sss_types, "fn")

        # Slicing operands/indices are the wrong type
        if not match:
            index_type = fn[0].sig.default_types[0]
            bad_indices = filter(lambda t: t.type != index_type, sss)
            bad_types = [s.type for s in bad_indices]

            type_error("Slice indices for type '" + repr(container) + 
                           "' must be '" + repr(index_type) + 
                       "' type, not" + listTostr(bad_types) + " type.", 
                       "",
                       * bad_indices)

        # Container is a tuple
        elif container.type is builtins["tuple"]:
            n.type = tuple_splice(n[0], n[1], n[2], n[3]) 

        # Container supports slicing and operands/indices have the right type
        else:
            n.type = match.sig.return_type
            


#------------------------------------------------------------------------------#
# def tuple_splice(t:type_obj, start:ast, stop:ast, step:ast) -> type_obj      #
#   Helper function for s_slicing for tuple slicing. Returns a new tuple       #
#   type_obj whose element types correspond to the sliced tuple.               #
#------------------------------------------------------------------------------#
def tuple_splice(t, start, stop, step):
    sss = []
    for s in [start, stop, step]:
        if s.label == "EMPTY":
            sss.append(None)
        else:
            try:
                sss.append(int(s[0]))
            except ValueError:
                type_error("'tuple' type indices must be integer literals, " + 
                           "not indentifiers.", "", s[0])
                return None
                
   
    try:
        result_type = t.type.elem_type[sss[0]:sss[1]:sss[2]]

    # Slicing operation out of range
    except IndexError:
        type_error("'" + repr(t) + "' index out of range.", "", t)
        return None

    else:
        return type_obj("tuple", builtins["tuple"], elem_type = result_type)

#------------------------------------------------------------------------------#
#                             MISC. LIST CONSTRUCTS                            #
#------------------------------------------------------------------------------#
            
#------------------------------------------------------------------------------#
# s_expressionlist_single(n:ast)                                               #
#   Sets the type of a single expression list to the type of its child.        #
#------------------------------------------------------------------------------#
def s_expressionlist_single(n):
    # 0: expression
    n.type = n[0].type


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
#   Checks if the type of a parameter's default value matches the delared      #
#   type of its identifier. Assigns the type of the single default argument    #
#   to its declared type.                                                      #
#------------------------------------------------------------------------------#
def s_defaultlist_single(n):
    # 0: identifier; 1: type; 2: expression
    if n[1].type != n[2].type:
        type_error("The default value assigned to '" + n[0] + "' must have " + 
                   "type '" + repr(n[1].type) + "', not type '" + 
                   repr(n[2].type) + "'.",  "", n[1], n[2])
    else:
        n.type = n[1].type


#------------------------------------------------------------------------------#
# s_grouping(n)                                                                #
#   Sets the type of a grouping node to the type of its child (i.e. the        #
#   expression inside of the grouping.                                         #
#------------------------------------------------------------------------------#
def s_grouping(n):
    # 0: expression
    n.type = n[0].type
    
       
checks = { 
    # Functions, Operations
    "FUNCTION_DEFINITION"        : s_function_definition,
    "FUNCTION_TYPE"              : s_function_type,
    "FUNCTION_CALL"              : s_function_call,
    "PROCEDURE_DEFINITION"       : s_procedure_definition,
    "PROCEDURE_TYPE"             : s_procedure_type,
    "PROCEDURE_CALL"             : s_procedure_call,
    "CALCULATION_BINARYOPERATOR" : s_calculation_binaryoperator,
    "CALCULATION_UNARYOPERATOR"  : s_calculation_unaryoperator,
    "RETURN"                     : s_return,
    "YIELD"                      : s_yield,
    
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
    "MEMBER_TYPE"                : s_member_type,
 
    # Conditionals
    "CONDITIONAL"                : s_conditional,
    "CONDITIONAL_ELIF"           : s_conditional,
    "TERNARY"                    : s_ternary,
    
    # Loops
    "WHILELOOP"                  : s_whileloop,
    "FORLOOP_ITER"               : s_forloop_iter,
    "FORLOOP_COUNT"              : s_forloop_count,

    # Literals
    "LITERAL_INT"                : s_literal_int,
    "LITERAL_FLOAT"              : s_literal_float,
    "LITERAL_BOOL"               : s_literal_bool,
    "LITERAL_STRING"             : s_literal_string,
    "LITERAL_LIST"               : s_literal_list,
    "LITERAL_TUPLE"              : s_literal_tuple,
    "LITERAL_DICTIONARY"         : s_literal_dictionary,
    "LITERAL_FUNCTION"           : s_literal_function,
    "LITERAL_SET"                : s_literal_set,

    # Variables and Declarations
    "DECLARATION_INITIALIZE"     : s_declaration_initialize,
    "ASSIGNMENT"                 : s_assignment,
    "VARIABLE"                   : s_variable,
    "MEMBER"                     : s_member, 

    # Membership testing
    "IN_MEMBER"                  : s_membership, 
    "NOTIN_MEMBER"               : s_membership,

    # Identity testing
    "IS_IDENTITY"                : s_identity, 
    "IS_NOT_IDENTITY"            : s_identity, 

     # Indexing and Slicing
    "INDEXING"                   : s_indexing,
    "SLICING"                    : s_slicing,  

    # List Constructs
    "ARGUMENTLIST"               : s_argumentlist,
    "ARGUMENTLIST_SINGLE"        : s_argumentlist_single,
    "DEFAULTLIST_SINGLE"         : s_defaultlist_single,
    "EXPRESSIONLIST_SINGLE"      : s_expressionlist_single,
    "GROUPING"                   : s_grouping,

     # Try Except
    "EXCEPT_SPECIFIC"            : s_except_specific,
    "EXCEPT_ALIAS"               : s_except_alias, 
    "RAISE"                      : s_raise

}

def r_return(lst):
    return True

def r_yield(lst):
    return True

def r_raise(lst):
    return True

def r_or(lst):
    return any(lst)

def r_try_except(lst):
    assert(len(lst) == 4)

    # try : lst[0]
    # except : lst[1]
    # else : lst[2]
    # finally : lst[3]
    return lst[3] or (lst[1] and (lst[0] or lst[2]))

def r_conditional(lst):
    if len(lst) != 3:
        return False
    return lst[1] and lst[2]

returns = {
    # Return
    "RETURN"                     : r_return,
    "YIELD"                      : r_yield,
    "RAISE"                      : r_raise,

    # OR
    "SUITE_BLOCK"                : r_or,
    "SUITE_INLINE"               : r_or,
    "BLOCK_WITH_ENVIRONMENT"     : r_or,
    "BLOCK"                      : r_or,
    "STATEMENT_MULTI"            : r_or,
    "STATEMENT_SINGLE"           : r_or,
    "CONDITIONAL_ELSE"           : r_or,
    "EXCEPT_SIMPLE"              : r_or,
    "EXCEPT_ALIAS"               : r_or,
    "EXCEPT_SPECIFIC"            : r_or,
    "EXCEPT_ELSE"                : r_or,
    "EXCEPT_FINALLY"             : r_or,

    # CONDITIONAL
    "CONDITIONAL"                : r_conditional,
    "CONDITIONAL_ELIF"           : r_conditional,
    
    # TRY_EXCEPT special case
    "TRY_EXCEPT"                 : r_try_except,
}

filename = ""