#------------------------------------------------------------------------------#
# cspy_translate.py                                                            #
#                                                                              #
# Original outline written by Eric Collins '17                                 #
# Summer 2015                                                                  #
#                                                                              #
# Revised and expanded by Maya Montgomery '18                                  #
# Summer 2016                                                                  #
#                                                                              #
# Revised and edited by Paul Magnus '18, Ines Ayara and Matthew R. Jenkins '20 #
# Summer 2017                                                                  #
#                                                                              #
# A translator for the language CSPy, a dialect of Python. Translates into     #
# native Python, creating a Python executable. Functions include a comment as  #
# the first line of the body that lists the children of the node received and  #
# handled by the function.                                                     #
#                                                                              #
# Translator also creates a linemap file for use during runtime error handling #
# which maps the Python executable lines to the original CSPy lines.           #
#                                                                              #
# USAGE: (ENTER THESE LINES INTO MASTER PROGRAM)                               #
#                                                                              #
#        from cspy_translate import translate                                  #
#        ... lexing, parsing, type checking here ...                           #
#        translate(myAbstractSyntaxTree, "filename.cspy")                      #
#                                                                              #
#------------------------------------------------------------------------------#
import sys, re, getpass, pickle, os
from cspy_data_struct import ast, holds_env, NotYetDeclaredException
from cspy_builtins import *
from cspy_runtime import remove_files


tmp_path = "/tmp/" + getpass.getuser() + "/"

#------------------------------------------------------------------------------#
# translate(parsetree:AST, filename:string)                                    #
# Translates checked code from parsetree to Python, outputs to file.           #
#------------------------------------------------------------------------------#
def translate(parsetree, filename, orig_path,
              import_overloads = {'global' : {}}):

    global path
    global overloads
    path = orig_path

    overloads = import_overloads

    # RETRIEVE FILE NAME
    find_path = re.compile('(?P<p>[\S]+)/(?P<n>[\S]+).cspy')
    found_path = find_path.search(filename)
    if found_path:
        filename = found_path.group("n") + ".py"
    else:
        filename = filename[:len(filename)-5] + ".py"

    # TRANSLATE
    try:
        the_file = open(tmp_path + filename, "w+")
        toPython(parsetree, the_file)            # translate parse tree
        the_file.close()
        export_map(filename)                     # write line map file
    except IOError:
        print >> sys.stderr, "Can't translate " + tmp_path + str(filename) + \
            " due to IOError."
        remove_files()
        sys.exit(1)

    return overloads

#------------------------------------------------------------------------------#
# The functions below translate the parsed CSPy file into Python code. Every   #
# node of the parsetree is accompanied with a label; the function toPython     #
# reads the labels and calls the appropriate function for each node.           #
#------------------------------------------------------------------------------#

# Delegates compilation to appropriate functions
def toPython(child, file, tabs=""):
    functions[child.label](child, file, tabs)


# Maps CSPy file line numbers to Python file line numbers
# (used for runtime error reporting)
def advance(child):
    global line_num
    line_num += 1
    lines[line_num] = child.lineNum

# Exports map of CSPy file line numbers to Python file line numbers
# (used for runtime error reporting)
def export_map(filename):

    # create map file name
    filename = filename[:len(filename)-3]      # get filename w/o .py
    filename = filename + "_linemap"
    try:
        the_file = open(tmp_path + filename, "wb")
    except IOError:
        print >> sys.stderr, "Can't compile " + str(filename) + \
            " due to IOError."

    # export the map

    # THIS METHOD USED FOR OTHER PATHS - see documentation for full explanation
    # the_file.write("_linemap = {")
    # for entry in lines:
    #     the_file.write("\t" + str(entry) + " : " + str(lines[entry]) + ",\n")
    # the_file.write("}\n")
    # the_file.write("for entry in _linemap:\n")
    # the_file.write("\tprint(str(entry) + \" \" + str(_linemap[entry]))")
    # the_file.close()

    # the_file.write("_linemap = {\n")
    # for entry in lines:
    #     the_file.write("\t" + str(entry) + " : " + str(lines[entry]) + ",\n")
    # the_file.write("}\n")
    
    pickle.dump(lines, the_file)
    the_file.close()


#------------------------------------------------------------------------------#
#                               FILE MAIN CONSTRUCTS                           #
#------------------------------------------------------------------------------#

def c_EMPTY(child, file, tabs):
    pass
    

def c_FILE(child, file, tabs):
    global path
    # 0: docstring; 1: import block; 2: declaration suite; 3: block
    if path != "":
        # replace ./ in path if it exists
        if re.match(r"^\./.+$", path):
            # first character is a .
            # replace with current working directory (cwd)
            path = os.getcwd() + path[1:]
        elif re.match(r"^[^/].+$", path):
            path = os.getcwd() + "/" + path

    file.write(tabs + "import sys\n")
    file.write(tabs + "sys.path.append(\"" + path + "\")\n")
    advance(child)
    advance(child)
    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)
    file.write(tabs + "import readline\n")       # see documentation for

    advance(child)                               # details on this
    toPython(child[2], file, tabs)
    toPython(child[3], file, tabs)

    # Not sure whether to add this in
    # It might allow me to avoid using os.system to run the program in cspy_runtime
    # file.write(tabs + "def _cspy_main():\n")
    # advance(child)
    # tabs = tabs + "\t"
    # toPython(child[3], file, tabs)


def c_DOCSTRING(child, file, tabs):
    # 0: optional docstring

    if type(child[0]) == str:                    # not empty
        doc = child[0].split("\n")
        for line in doc:                         # lexer defines docstrings
            file.write(tabs + line + "\n")       # as greedy with newlines;
            advance(child)                       # need to keep track of them


def c_DECLARATION_SUITE(child, file, tabs=""):
    # 0: variable block; 1: class block; 2: method block

    if in_class:                                 # handle class attributes
        make_init(child, file, tabs)             # within an __init__
    else:
        toPython(child[0], file, tabs)

    toPython(child[1], file, tabs)
    toPython(child[2], file, tabs)


def make_init(child, file, tabs=""):
    # 0: variable block

    global in_init
    in_init = True

    file.write(tabs + "def __init__(self, f, *params):\n")
    advance(child)

    # if superclass:
    #     file.write(tabs + "\t" + superclass + ".__init__(self)\n")
    #     advance(child)

    toPython(child[0], file, tabs + "\t")

    file.write(tabs + "\t" + "f(self, *params)\n")
    advance(child)

    in_init = False


#------------------------------------------------------------------------------#
#                                    IMPORT                                    #
#------------------------------------------------------------------------------#

def c_IMPORTBLOCK_SINGLE(child, file, tabs=""):
    # 0: import statement

    toPython(child[0], file, tabs)


def c_IMPORTBLOCK_MULTI(child, file, tabs=""):
    # 0: import block; 1: import block

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


def c_IMPORT_SIMPLE(child, file, tabs=""):
    # 0: module
    
    file.write("import " + child[0] + "\n")
    advance(child)


def c_IMPORT_BULK(child, file, tabs=""):
    # 0: module

    file.write("from " + child[0] + " import *\n")
    advance(child)


def c_IMPORT_ALIAS(child, file, tabs=""):
    # 0: module; 1: alias

    file.write("import " + child[0] + " as " + child[1] + "\n")
    advance(child)


def c_IMPORT_DISCRETE(child, file, tabs=""):
    # 0: module; 1: import list

    file.write("from " + child[0] + " import ")
    toPython(child[1], file, tabs)
    file.write("\n")
    advance(child)

def c_IMPORTLIST_SIMPLE(child, file, tabs=""):
    # 0: import identifier

    file.write(child[0])
  

def c_IMPORTLIST_MULTI(child, file, tabs=""):
    # 0: import list; 1: import list

    toPython(child[0], file, tabs)
    file.write(", ")
    toPython(child[1], file, tabs)


def c_IMPORTLIST_ALIAS(child, file, tabs=""):
    # 0: module; 1: alias

    file.write(child[0] + " as " + child[1])


#------------------------------------------------------------------------------#
#                                    BLOCKS                                    #
#------------------------------------------------------------------------------#

def c_BLOCK(child, file, tabs=""):
    # 0: variable block; 1: block

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


def c_BLOCK_WITH_ENVIRONMENT(child, file, tabs=""):
    # 0: variable block; 1: block

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


def c_SUITE_BLOCK(child, file, tabs=""):
    # 0: docstring; 1: block

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


def c_SUITE_INLINE(child, file, tabs=""):
    # 0: statement

    file.write(" ")                              # WHY A SPACE??
    toPython(child[0], file, tabs)


def c_VARIABLEBLOCK_MULTI(child, file, tabs=""):
    # 0: variable block; 1: variable block

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


def c_VARIABLEBLOCK_SINGLE(child, file, tabs=""):
    # 0: declaration

    file.write(tabs)
    toPython(child[0], file, tabs)
    file.write("\n")
    advance(child)


def c_CLASSBLOCK(child, file, tabs=""):
    # 0: class definition; 1: class block

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


def c_METHODBLOCK(child, file, tabs=""):
    # 0: subroutine definition; 1: method block

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


#------------------------------------------------------------------------------#
#                                    CLASSES                                   #
#------------------------------------------------------------------------------#

def c_CLASS_DEFINITION(child, file, tabs=""):
    # 0: identifier; 1: superclass; 2: suite

    global in_class
    global superclass
    global current_class
    global overloads
    in_class = True
    current_class = child[0]
    if current_class in overloads:
        print >> sys.stderr, "Error in 'cspy_translate.py':\n" + \
              "The class '" + current_class + "' has already been defined."
        remove_files()

    # new dictionary element
    overloads[current_class] = {}

    file.write(tabs + "class " + child[0])
    if child[1].label != "EMPTY":
        superclass = child[1][0]
        try:
            superclass = replace[superclass]
        except:
            pass
        file.write("(" + superclass + ")")
    file.write(":\n")
    advance(child)

    toPython(child[2], file, tabs+"\t")
    in_class = False
    current_class = ""
    superclass = None


def c_CLASS_SUITE(child, file, tabs=""):
    # 0: doc string; 1: declaration suite

    toPython(child[0], file, tabs)
    toPython(child[1], file, tabs)


def c_MEMBER(child, file, tabs=""):
    # 0: identifier; 1: attribute name

    # global needs_self

    toPython(child[0], file, tabs)

    if isinstance(child.type, list):          # overloaded function
        file.write(".")
        name = "_" + child[1]
        args = child.parent[1].flatten("EXPRESSIONLIST_SINGLE")
        for arg in args:
            name += "_" + arg[0].type.type_str

        file.write(name)

        return
        
    file.write("." + child[1])


def c_IN_MEMBER(child, file, tabs=""):
    # 0: expression; 1: expression

    toPython(child[0], file, tabs)
    file.write(" in ")
    toPython(child[1], file, tabs)


def c_NOTIN_MEMBER(child, file, tabs=""):
    # 0: expression; 1: expression

    toPython(child[0], file, tabs)
    file.write(" not in ")
    toPython(child[1], file, tabs)


#------------------------------------------------------------------------------#
#                             FUNCTIONS, OPERATIONS                            #
#------------------------------------------------------------------------------#

def c_FUNCTION_DEFINITION(child, file, tabs=""):
    # 0: identifier; 1: arg list; 2: return type; 3: suite

    global overloads

    if (type(child.lookup_var(child[0])) == list and
        child[0] not in builtins):                    # overloaded function
        name = overload_name(child, "def")

        if in_class:
            if name in overloads[current_class]:
                print >> sys.stderr, "Error in 'cspy_translate.py':\n" + \
                      "Function '" + name + "' was already defined as an " + \
                      "overloaded Python function."
                remove_files()

            overloads[current_class][name] = child[0]

        else:
            if name in overloads['global']:
                print >> sys.stderr, "Error in 'cspy_translate.py':\n" + \
                      "Function '" + name + "' was already defined as an " + \
                      "overloaded Python function."
                remove_files()
            
            overloads['global'][name] = child[0]

    else:
        name = child[0]

    file.write(tabs + "def " + name + "(")

    if in_class:
        file.write("self, ")
    toPython(child[1], file, tabs)
    file.write("):\n")
    advance(child)

    toPython(child[3], file, tabs+"\t")


def c_FUNCTION_CALL(child, file, tabs=""):
    # 0: identifier; 1: expression list

    # global needs_self

    var = child[0].flatten("VARIABLE")           # get func / member name

    if var == []:
        var = child[0][0][0]                     # literal function
    else:
        var = var[0][0]                          # get first var name

    if (type(child.lookup_var(var)) == list and
        var not in builtins):                    # overloaded function
        file.write(overload_name(child, "call"))
    else:
        toPython(child[0], file, tabs)

    file.write("(")
    # if needs_self:
    #     file.write("self,")
    #     needs_self = False
    toPython(child[1], file, tabs)
    file.write(")")


def c_CONSTRUCTOR_CALL(child, file, tabs=""):
    # 0: identifier; 1: expression list

    if child[0].label == "MEMBER":
        # x = alpha.A() => x = alpha.A(alpha.A.A,)
        var = child[0][0][0] + "." + child[0][1]
    else:
        var = child[0][0]

    file.write(var + "(" + var + ".")              # calls hidden Python __init__
    
    # CALL USER-DEFINED CONSTRUCTOR
    node = child
    while(node.label != "FILE"):
        node = node.parent
    if child[0].label == "MEMBER":
        var_methods = child[0].type
        if type(var_methods) == list:         # overloaded constructor
            name = "_" + child[0][1]          # prepenhd _
            args = child[1].flatten("EXPRESSIONLIST_SINGLE")
            for arg in args:                  # append arg types
                name += "_" + arg[0].type.type_str
            file.write(name)
        else:
            file.write(child[0][1])
    else:
        var_methods = node.env[var].methods
        if type(var_methods[var]) == list:     # overloaded constructor
            file.write(overload_name(child, "call"))
        else:
            toPython(child[0], file, tabs)
    file.write(",")
    toPython(child[1], file, tabs)
    file.write(")")

def c_SUPER_CONSTRUCTOR(child, file, tabs=""):
    # 0: member node; 1: expression list
    
    superclass = child[0][0][0]
    constructor = child[0][1]
    
    file.write(superclass + ".__init__(self, " + superclass + "." +
               constructor + ", ")
    toPython(child[1], file, tabs)
    file.write(")")

def c_PROCEDURE_DEFINITION(child, file, tabs=""):
    # 0: identifier; 1: arg list; 2: suite

    global overloads

    if (type(child.lookup_var(child[0])) == list and
        child[0] not in builtins):                    # overloaded function
        name = overload_name(child, "def")

        if in_class:
            if name in overloads[current_class]:
                print >> sys.stderr, "Error in 'cspy_translate.py':\n" + \
                      "Procedure '" + name + "' was already defined as an " + \
                      "overloaded Python procedure."
                remove_files()

            overloads[current_class][name] = child[0]

        else:
            if name in overloads['global']:
                print >> sys.stderr, "Error in 'cspy_translate.py':\n" + \
                      "Procedure '" + name + "' was already defined as an " + \
                      "overloaded Python procedure."
                remove_files()

            overloads['global'][name] = child[0]

    else:
        name = child[0]

    file.write(tabs + "def " + name + "(")

    if in_class:
        file.write("self, ")
    toPython(child[1], file, tabs)
    file.write("):\n")
    advance(child)

    toPython(child[2], file, tabs+"\t")


def c_PROCEDURE_CALL(child, file, tabs=""):
    # 0: variable node; 1: expression list

    # global needs_self

    var = child[0].flatten("VARIABLE")           # get proc / member name

    if var == []:
        var = child[0][0][0]                     # literal function
    else:
        var = var[0][0]                          # get first var name

    if (type(child.lookup_var(var)) == list and
        var not in builtins):                    # overloaded function
        file.write(overload_name(child, "call"))
    else:
        toPython(child[0], file, tabs)

    file.write("(")
    # if needs_self:
    #     file.write("self,")
    #     needs_self = False
    toPython(child[1], file, tabs)
    file.write(")")


def overload_name(child, which, params = None):
    # 0: identifier; 2: arg / expr list

    # PROC / FN CALL
    if (which == "call"):
        name = "_" + child[0][0]                     # prepend _

        args = child[1].flatten("EXPRESSIONLIST_SINGLE")
        for arg in args:                             # append arg types
            name += "_" + arg[0].type.type_str

    # PROC / FN DEFINITION
    if (which == "def"):
        name = "_" + child[0]                        # prepend _

        args = child[1].flatten("ARGUMENTLIST_SINGLE")
        for arg in args:                             # append arg types
            name += "_" + arg.type.type_str

    # PROC / FN ASSIGNMENT
    if (which == "assign"):
        name = "_" + child[0]                        # prepend _

        args = params
        for arg in args:                             # append arg types
            name += "_" + arg.type_str

    return name


def c_CALCULATION_BINARYOPERATOR(child, file, tabs=""):
    # 0: expression; 1: operator; 2: expression

    toPython(child[0], file, tabs)
    try:                                         # check for irregular binary
        op = replace[child[1]]                   # keywords (like 'and') 
    except KeyError:
        op = child[1]
    file.write(" " + op + " ")
    toPython(child[2], file, tabs)


def c_CALCULATION_UNARYOPERATOR(child, file, tabs=""):
    # 0: operator; 1: expression

    try:                                         # check for irregular unary
        op = replace[child[0]]                   # keywords (like 'not') 
    except KeyError:
        op = child[0]

    if op == "+":                                # make number positive by
        file.write("abs(")                       # using builtin abs()
        toPython(child[1], file, tabs)
        file.write(")")
    else:
        file.write(op)
        toPython(child[1], file, tabs)


def c_RETURN(child, file, tabs=""):
    file.write("return ")
    toPython(child[0], file, tabs)               # may be empty (void return)


def c_YIELD(child, file, tabs=""):
    file.write("yield ")
    toPython(child[0], file, tabs)


def c_CLASS_FUNCTION_CALL(child, file, tabs=""):

    var = child[0].flatten("CLASS_VARIABLE")           # get func / member name

    if var == []:
        var = child[0][0][0]                     # literal function
    else:
        var = var[0][0]                          # get first var name

    if (type(child.lookup_var(var)) == list and
        var not in builtins):                    # overloaded function
        file.write(overload_name(child, "call"))
    else:
        toPython(child[0], file, tabs)

    file.write("(")
    toPython(child[1], file, tabs)
    file.write(")")


def c_CLASS_PROCEDURE_CALL(child, file, tabs=""):

    var = child[0].flatten("CLASS_VARIABLE")           # get proc / member name

    if var == []:
        var = child[0][0][0]                     # literal function
    else:
        var = var[0][0]                          # get first var name

    if (type(child.lookup_var(var)) == list and
        var not in builtins):                    # overloaded function
        file.write(overload_name(child, "call"))
    else:
        toPython(child[0], file, tabs)

    file.write("(")
    toPython(child[1], file, tabs)
    file.write(")")


#------------------------------------------------------------------------------#
#                  PYTHON FUNCTIONS AND PROCEDURES                             #
#------------------------------------------------------------------------------#

def c_PYTHON_FUNCTION_CALL(child, file, tabs=""):
    # 0: identifier; 1: expression list
    
    # global needs_self

    var = child[0].flatten("VARIABLE")           # get func / member name

    if var == []:
        var = child[0][0][0]                     # literal function
    else:
        var = var[0][0]                          # get first var name

    toPython(child[0], file, tabs)

    file.write("(")
    # if needs_self:
    #     file.write("self,")
    #     needs_self = False
    toPython(child[1], file, tabs)
    file.write(")")


def c_PYTHON_CONSTRUCTOR_CALL(child, file, tabs=""):
    # 0: identifier; 1: expression list

    if child[0].label == "MEMBER":
        var = child[0][0][0] + "." + child[0][1]
    else:
        var = child[0][0]

    file.write(var + "(")
    toPython(child[1], file, tabs)
    file.write(")")


def c_PYTHON_SUPER_CONSTRUCTOR(child, file, tabs=""):
    # 0: identifier; 1: expression list

    superclass = child[0][0][0]
    constructor = child[0][1]
    
    file.write(superclass + ".__init__(self, ")
    toPython(child[1], file, tabs)
    file.write(")")


def c_PYTHON_PROCEDURE_CALL(child, file, tabs=""):
    # 0: identifier; 1: expression list

    # global needs_self

    var = child[0].flatten("VARIABLE")           # get proc / member name

    if var == []:
        var = child[0][0][0]                     # literal function
    else:
        var = var[0][0]                          # get first var name

    toPython(child[0], file, tabs)

    file.write("(")
    # if needs_self:
    #     file.write("self,")
    #     needs_self = False
    toPython(child[1], file, tabs)
    file.write(")")


#------------------------------------------------------------------------------#
#                                   VARIABLES                                  #
#------------------------------------------------------------------------------#

def c_IDENTIFIER(child, file, tabs=""): # THIS PROC MIGHT NOT BE NEEDED
    # 0: identifier

    if in_class:
        node = child
        while node.label != "CLASS_DEFINITION":
            node = node.parent
        if (child[0] in node.env):
            file.write("self.")

    file.write(child[0])


def c_IDENTIFIER_LIST(child, file, tabs=""):
    # 0: identifier list; 1: identifier list

    toPython(child[0], file, tabs)
    file.write(", ")
    toPython(child[1], file, tabs)


def c_VARIABLE(child, file, tabs=""):
    # 0: identifier

    var = child[0]

    _self = ""

    # CHECK FOR ATTRIBUTE
    if in_class:                             # check for attributes
        node = child                         # to see if need 'self.'
        local = False

        while (node.label != "CLASS_DEFINITION" and not local):
            if (node.label in holds_env and var in node.env):  
                local = True                 # var is local class var
            else:
                node = node.parent           # keep looking

        if (node.label == "CLASS_DEFINITION" and var in node.env):
            file.write("self.")              # var is class attribute
            _self = "self."

    # CHECK FOR FUNCTION
    assigned = False
    if assign_me != None:
        if (var not in builtins and         # overloaded function
            type(child.lookup_var(var)) == list):

            typ = child.lookup_var(assign_me)
            params = typ.sig.param_types
            file.write(overload_name(child, "assign", params))
            assigned = True

    # CHECK FOR IRREGULAR
    if not assigned:
        try:
            var = replace[var]                       # like str(), int()...
        except KeyError:
            pass
        file.write(var)

    global last_var                              # used for class constructors
    last_var = _self + var                       # and __init__ handling


def c_DECLARATION_SIMPLE(child, file, tabs=""):
    # 0: identifier; 1: type                     # child[1][0] = type str

    if in_init:                                  # class attributes are
        file.write("self.")                      # declared in an __init__

    file.write(child[0] + " = ")

    if child[1][0] in ("int", "float", "bool"):
        file.write("0")
    elif child[1][0] == "string":
        file.write("\"\"")
    elif child[1][0] == "file":
        file.write("None")

    elif type(child[1][0]) == ast:
        if child[1][0].label == "TUPLE_TYPE":
            file.write("()")
        elif child[1][0].label == "LIST_TYPE":
            file.write("[]")
        else:
            file.write("None")

    else:
        typ = child.lookup_var(child[1][0])
        # special case for init inside own class
        file.write("None")
        # if type(typ) == list or typ.type_str == "proc":
        #     file.write("None")
        # else:
        #     file.write(typ.type_str + "()")

    global last_var                              # used for class constructors
    last_var = child[0]                          # and __init__ handling


def c_DECLARATION_INITIALIZE(child, file, tabs=""):
    # 0: identifier; 1: type; 2: value

    if in_init:                                  # class attributes are
        file.write("self.")                      # declared in an __init__

    file.write(child[0] + " = ")
    global last_var                              # used for class constructors
    last_var = child[0]                          # and __init__ handling

    toPython(child[2], file, tabs)


def c_ASSIGNMENT(child, file, tabs=""):
    # 0: identifier; 1: operator; 2: value
    global assign_me

    toPython(child[0], file, tabs)
    file.write(" " + child[1] + " ")             # =, +=, *=, etc.

    v = child[0].flatten("VARIABLE")
    assign_me = v[0][0] if v != [] else None     # get variable node in case
    toPython(child[2], file, tabs)               # assigning overload func

    assign_me = None


def c_CLASS_VARIABLE(child, file, tabs=""):
    # 0: identifier

    var = child[0]

    # _self = ""

    # # CHECK FOR ATTRIBUTE
    # if in_class:                             # check for attributes
    #     node = child                         # to see if need 'self.'
    #     local = False

    #     while (node.label != "CLASS_DEFINITION" and not local):
    #         if (node.label in holds_env and var in node.env):  
    #             local = True                 # var is local class var
    #         else:
    #             node = node.parent           # keep looking

    #     if (node.label == "CLASS_DEFINITION" and var in node.env):
    #         file.write("self.")              # var is class attribute
    #         _self = "self."

    file.write("self.")

    # CHECK FOR FUNCTION
    assigned = False
    if assign_me != None:
        if (var not in builtins and         # overloaded function
            type(child.lookup_var(var)) == list):

            typ = child.lookup_var(assign_me)
            params = typ.sig.param_types
            file.write(overload_name(child, "assign", params))
            assigned = True

    # CHECK FOR IRREGULAR
    if not assigned:
        try:
            var = replace[var]                       # like str(), int()...
        except KeyError:
            pass
        file.write(var)

    global last_var                              # used for class constructors
    last_var = "self." + var                       # and __init__ handling


#------------------------------------------------------------------------------#
#                                     LOOPS                                    #
#------------------------------------------------------------------------------#

def c_WHILELOOP(child, file, tabs=""):
    # 0: bool expression; 1: suite

    file.write(tabs + "while (")
    toPython(child[0], file, tabs)
    file.write("):\n")
    advance(child)
    toPython(child[1], file, tabs+"\t")


def c_FORLOOP_ITER(child, file, tabs=""):
    '''for x:type in iterable'''                # includes range()
    # 0: identifier; 1: iterable; 2: suite

    file.write(tabs + "for " + child[0] + " in ")
    toPython(child[1], file, tabs)
    file.write(":\n")
    advance(child)
    toPython(child[2], file, tabs+"\t")
    
def c_FORLOOP_COUNT(child, file, tabs=""):
    '''for x:int in 0 .. 10'''                   # i.e. range(0,11)
    # 0: identifier; 1: start range; 2: stop range; 3: suite

    file.write(tabs + "for " + child[0] + " in range(")
    toPython(child[1], file, tabs)
    file.write(", ")
    toPython(child[2], file, tabs)
    file.write("+1):\n")                         # +1 bc range is exclusive
    advance(child)                               # but this should be inclusive
    toPython(child[3], file, tabs+"\t")


#------------------------------------------------------------------------------#
#                                 CONDITIONALS                                 #
#------------------------------------------------------------------------------#

def c_CONDITIONAL(child, file, tabs=""):
    # 0: bool expression; 1: suite; 2: additional clauses

    file.write(tabs + "if (")
    toPython(child[0], file, tabs)
    file.write("):\n")
    advance(child)
    toPython(child[1], file, tabs+"\t")
    toPython(child[2], file, tabs)               # optional additions


def c_CONDITIONAL_ELIF(child, file, tabs=""):
    # 0: bool expression; 1: suite; 2: additional clauses

    file.write(tabs + "elif (")
    toPython(child[0], file, tabs)
    file.write("):\n")
    advance(child)
    toPython(child[1], file, tabs+"\t")
    toPython(child[2], file, tabs)               # optional additions


def c_CONDITIONAL_ELSE(child, file, tabs=""):
    # 0: suite

    file.write(tabs + "else:\n")
    advance(child)
    toPython(child[0], file, tabs+"\t")          # indented body


def c_TERNARY(child, file, tabs=""):             # WILL NEED TO REWRITE
    # 0: bool expression; 1: expression; 2: expression

    toPython(child[1] , file, tabs)                # EXECUTE NON-VOID FUNCS
    file.write(" if ")                             # ALLOW ASSIGNMENT
    toPython(child[0], file, tabs)
    file.write(" else ")
    toPython(child[2], file, tabs)


#------------------------------------------------------------------------------#
#                                  STATEMENTS                                  #
#------------------------------------------------------------------------------#

def c_STATEMENT_SINGLE(child, file, tabs=""):
    # 0: statement

    file.write(tabs)
    try:                                         # check for irregular keywords
        s = replace[child[0]]                    # (like 'continue', 'break')
        file.write(s)
    except KeyError:
        if not isinstance(child[0], ast):
            file.write(child[0])                 # raise ___, delete ___
        else:
            toPython(child[0], file, tabs)
    file.write("\n")
    advance(child)


def c_STATEMENT_MULTI(child, file, tabs=""):
    # 0: statement list; 1: statement list

    toPython(child[0], file, tabs)
    file.write("\n")                             # new lines between statements
    advance(child)
    toPython(child[1], file, tabs)


def c_RAISE(child, file, tabs=""):
    # 0: identifier, 1: expression

    if isinstance(child[0], ast):
        file.write("raise ")
        toPython(child[0], file, tabs="")
    else:
        file.write("raise " + child[0])


def c_DELETE(child, file, tabs=""):
    # 0: expression

    file.write("del ")
    # file.write(tabs + "del ")
    toPython(child[0], file, tabs)


#------------------------------------------------------------------------------#
#                                LITERAL TYPES                                 #
#------------------------------------------------------------------------------#

def c_LITERAL_INT(child, file, tabs):
    file.write(child[0])


def c_LITERAL_FLOAT(child, file, tabs):
    file.write(child[0])


def c_LITERAL_STRING(child, file, tabs):
    string = child[0].split("\n")
    for x in range(len(string)-1):
        file.write(string[x] + "\n")
        advance(child)
    file.write(string[len(string)-1])


def c_LITERAL_BOOL(child, file, tabs):
    file.write(child[0].title())


def c_LITERAL_TUPLE(child, file, tabs=""):
    file.write("(")
    toPython(child[0], file, tabs)
    file.write(")")


def c_TUPLE_SINGLE(child, file, tabs =""):
    toPython(child[0],file, tabs)
    file.write(",")


def c_MULTI_TUPLE(child, file, tabs=""):
    toPython(child[0], file, tabs)


def c_LITERAL_LIST(child, file, tabs=""):
    file.write("[")
    toPython(child[0], file, tabs)
    file.write("]")


def c_LITERAL_DICTIONARY(child, file, tabs=""):
    file.write("{")
    toPython(child[0], file, tabs)
    file.write("}")


def c_LITERAL_SET(child, file, tabs=""):
    file.write("{")
    toPython(child[0], file, tabs)
    file.write("}")


def c_LITERAL_FUNCTION(child, file, tabs=""):
    file.write("lambda ")
    toPython(child[0], file, tabs)
    file.write(" : ")
    toPython(child[2], file, tabs)\


def c_LITERAL_NONE(child, file, tabs=""):
    file.write("None")


#------------------------------------------------------------------------------#
#                                 ARGUMENT LISTS                               #
#------------------------------------------------------------------------------#
    
def c_ARGUMENTLIST(child, file, tabs = ""):
    # 0: argument list; 1: default list

    toPython(child[0], file, tabs)
    if (child[1].label!="EMPTY"):
        file.write(", ")
        toPython(child[1], file, tabs)


def c_ARGUMENTLIST_SINGLE(child, file, tabs=""):
    # 0: argument

    file.write(child[0])

    
def c_ARGUMENTLIST_MULTI(child, file, tabs=""):
    # 0: argument list; 1: argument list

    toPython(child[0], file, tabs)
    file.write(", ")
    toPython(child[1], file, tabs)


def c_DEFAULTLIST_SINGLE(child, file, tabs=""):
    # 0: default

    file.write(child[0] + "=")
    toPython(child[2], file, tabs)


def c_DEFAULTLIST_MULTI(child, file, tabs=""):
    # 0: default list; 1: default list

    toPython(child[0], file, tabs)
    file.write(", ")
    toPython(child[1], file, tabs)


#------------------------------------------------------------------------------#
#                              MISC. LIST CONSTRUCTS                           #
#------------------------------------------------------------------------------#

def c_EXPRESSIONLIST_SINGLE(child, file, tabs=""):
    # 0: expression

    toPython(child[0], file, tabs)


def c_EXPRESSIONLIST_MULTI(child, file, tabs=""):
    # 0: expression list; 1: expression list

    toPython(child[0], file, tabs)
    file.write(", ")
    toPython(child[1], file, tabs)


def c_GENERICLIST_SINGLE(child, file, tabs=""):     # need these generic list
    pass                                            # functions defined so
                                                    # toPython doesn't error,
def c_GENERICLIST_MULTI(child, file, tabs=""):      # but Python doesn't use
    pass                                            # generic params, so no
                                                    # output for these

def c_DICTIONARYLIST_SINGLE(child, file, tabs=""):
    # 0: key; 1: value

    toPython(child[0], file, tabs)
    file.write(" : ")
    toPython(child[1], file, tabs)


def c_DICTIONARYLIST_MULTI(child, file, tabs=""):
    # 0: dictionary list; 1: dictionary list

    toPython(child[0], file, tabs)
    file.write(", ")
    toPython(child[1], file, tabs)


def c_GROUPING(child, file, tabs=""):
    # 0: expression

    file.write("(")
    toPython(child[0], file, tabs)
    file.write(")")


#------------------------------------------------------------------------------#
#                              INDEXING & SLICING                              #
#------------------------------------------------------------------------------#

def c_INDEXING(child, file, tabs=""):
    # 0: identifier; 1: expression
    
    toPython(child[0], file, tabs)
    file.write("[")
    toPython(child[1], file, tabs)
    file.write("]")


def c_SLICING(child, file, tabs=""):
    # 0: identifier; 1: expression; 2: expression; 3: expression

    toPython(child[0], file, tabs)
    file.write("[")
    toPython(child[1], file, tabs)
    file.write(":")
    toPython(child[2], file, tabs)
    file.write(":")
    toPython(child[3], file, tabs)
    file.write("]")


#------------------------------------------------------------------------------#
#                                   TRY EXCEPT                                 #
#------------------------------------------------------------------------------#

def c_TRY_EXCEPT(child, file, tabs=""):
    # 0: suite; 1-3: additional clauses

    file.write(tabs + "try:\n")
    advance(child)
    toPython(child[0], file, tabs+"\t")
    for i in range(1,4):                         # optional additions
        toPython(child[i], file, tabs)


def c_EXCEPT_SIMPLE(child, file, tabs=""):
    # 0: suite

    file.write(tabs + "except:\n")
    advance(child)
    toPython(child[0], file, tabs+"\t")


def c_EXCEPT_ALIAS(child, file, tabs=""):
    # 0: exception; 1: alias; 2: suite; 3: except list

    file.write(tabs + "except " + child[0] + " as " 
               + child[1] + ":\n")
    advance(child)
    toPython(child[2], file, tabs+"\t")
    toPython(child[3], file, tabs)


def c_EXCEPT_SPECIFIC(child, file, tabs=""):
    # 0: exception; 1: suite; 2: except list

    file.write(tabs + "except " + child[0] + ":\n")
    advance(child)
    toPython(child[1], file, tabs+"\t")
    toPython(child[2], file, tabs)


def c_EXCEPT_ELSE(child, file, tabs=""):
    # 0: suite

    file.write(tabs + "else:\n")
    advance(child)
    toPython(child[0], file, tabs+"\t")


def c_EXCEPT_FINALLY(child, file, tabs=""):
    # 0: suite

    file.write(tabs + "finally:\n")
    advance(child)
    toPython(child[0], file, tabs+"\t")


#-----------------------------------------------------------------------------#
#                                    ASSERT                                   #
#-----------------------------------------------------------------------------#

def c_ASSERT_NOMSG(child, file, tabs=""):
    # 0:  grouping
    file.write("assert ")
    toPython(child[0], file, tabs)

def c_ASSERT_MSG(child, file, tabs=""):
    # 0: LITERAL_BOOL, 1:  LITERAL_STRING
    file.write("assert ")
    toPython(child[0], file, tabs)
    file.write(", ")
    toPython(child[1], file, tabs)


#------------------------------------------------------------------------------#
#                                  IDENTITY                                    #
#------------------------------------------------------------------------------#

def c_IS_IDENTITY(child, file, tabs=""):
    # 0: LHS  # 1: RHS
    toPython(child[0], file, tabs)
    file.write(" is ")
    toPython(child[1], file, tabs)

def c_IS_NOT_IDENTITY(child, file, tabs=""):
    toPython(child[0], file, tabs)
    file.write(" is not ")
    toPython(child[1], file, tabs)

 
#------------------------------------------------------------------------------#
#                             COMPILER FUNCTIONALITY                           #
#------------------------------------------------------------------------------#

# Dictionary for toPython to use to delegate compilation
functions = {

    # FILE MAIN CONSTRUCTS
    "EMPTY"                         : c_EMPTY,
    "FILE"                          : c_FILE,
    "DOCSTRING"                     : c_DOCSTRING,
    "DECLARATION_SUITE"             : c_DECLARATION_SUITE,

    # IMPORT
    "IMPORTBLOCK_SINGLE"            : c_IMPORTBLOCK_SINGLE,
    "IMPORTBLOCK_MULTI"             : c_IMPORTBLOCK_MULTI,
    "IMPORT_SIMPLE"                 : c_IMPORT_SIMPLE,
    "IMPORT_BULK"                   : c_IMPORT_BULK,
    "IMPORT_ALIAS"                  : c_IMPORT_ALIAS,
    "IMPORT_DISCRETE"               : c_IMPORT_DISCRETE,
    "IMPORTLIST_SIMPLE"             : c_IMPORTLIST_SIMPLE,
    "IMPORTLIST_MULTI"              : c_IMPORTLIST_MULTI,
    "IMPORTLIST_ALIAS"              : c_IMPORTLIST_ALIAS,
    "PYIMPORT_SIMPLE"               : c_IMPORT_SIMPLE,
    "PYIMPORT_BULK"                 : c_IMPORT_BULK,
    "PYIMPORT_ALIAS"                : c_IMPORT_ALIAS,
    "PYIMPORT_DISCRETE"             : c_IMPORT_DISCRETE,

    # BLOCKS
    "BLOCK"                         : c_BLOCK,
    "BLOCK_WITH_ENVIRONMENT"        : c_BLOCK_WITH_ENVIRONMENT,
    "SUITE_BLOCK"                   : c_SUITE_BLOCK,
    "SUITE_INLINE"                  : c_SUITE_INLINE,
    "VARIABLEBLOCK_SINGLE"          : c_VARIABLEBLOCK_SINGLE,
    "VARIABLEBLOCK_MULTI"           : c_VARIABLEBLOCK_MULTI,
    "CLASSBLOCK"                    : c_CLASSBLOCK,
    "METHODBLOCK"                   : c_METHODBLOCK,

    # CLASSES
    "CLASS_DEFINITION"              : c_CLASS_DEFINITION,
    "CLASS_SUITE"                   : c_CLASS_SUITE,
    "MEMBER"                        : c_MEMBER,
    "IN_MEMBER"                     : c_IN_MEMBER,
    "NOTIN_MEMBER"                  : c_NOTIN_MEMBER,

    # FUNCTIONS, OPERATIONS
    "FUNCTION_DEFINITION"           : c_FUNCTION_DEFINITION,
    "FUNCTION_CALL"                 : c_FUNCTION_CALL,
    "PROCEDURE_DEFINITION"          : c_PROCEDURE_DEFINITION,
    "CONSTRUCTOR_CALL"              : c_CONSTRUCTOR_CALL,
    "SUPER_CONSTRUCTOR"             : c_SUPER_CONSTRUCTOR,
    "PROCEDURE_CALL"                : c_PROCEDURE_CALL,
    "CALCULATION_BINARYOPERATOR"    : c_CALCULATION_BINARYOPERATOR,
    "CALCULATION_UNARYOPERATOR"     : c_CALCULATION_UNARYOPERATOR,
    "RETURN"                        : c_RETURN,
    "YIELD"                         : c_YIELD,
    "CLASS_FUNCTION_CALL"           : c_CLASS_FUNCTION_CALL,
    "CLASS_PROCEDURE_CALL"          : c_CLASS_PROCEDURE_CALL,

    # PYTHON FUNCTIONS AND PROCEDURES
    "PYTHON_FUNCTION_CALL"          : c_PYTHON_FUNCTION_CALL,
    "PYTHON_CONSTRUCTOR_CALL"       : c_PYTHON_CONSTRUCTOR_CALL,
    "PYTHON_SUPER_CONSTRUCTOR"      : c_PYTHON_SUPER_CONSTRUCTOR,
    "PYTHON_PROCEDURE_CALL"         : c_PYTHON_PROCEDURE_CALL,

    # VARIABLES
    "IDENTIFIER"                    : c_IDENTIFIER,
    "IDENTIFIER_LIST"               : c_IDENTIFIER_LIST,
    "VARIABLE"                      : c_VARIABLE,
    "DECLARATION_SIMPLE"            : c_DECLARATION_SIMPLE,
    "DECLARATION_INITIALIZE"        : c_DECLARATION_INITIALIZE,
    "ASSIGNMENT"                    : c_ASSIGNMENT,
    "CLASS_VARIABLE"                : c_CLASS_VARIABLE,

    # LOOPS
    "WHILELOOP"                     : c_WHILELOOP,
    "FORLOOP_ITER"                  : c_FORLOOP_ITER,     # list or range
    "FORLOOP_COUNT"                 : c_FORLOOP_COUNT,    # dot dot

    # CONDITIONALS
    "CONDITIONAL"                   : c_CONDITIONAL,
    "CONDITIONAL_ELIF"              : c_CONDITIONAL_ELIF,
    "CONDITIONAL_ELSE"              : c_CONDITIONAL_ELSE,
    "TERNARY"                       : c_TERNARY,

    # STATEMENTS
    "STATEMENT_SINGLE"              : c_STATEMENT_SINGLE,
    "STATEMENT_MULTI"               : c_STATEMENT_MULTI,
    "RAISE"                         : c_RAISE,
    "DELETE"                        : c_DELETE,

    # LITERAL TYPES
    "LITERAL_INT"                   : c_LITERAL_INT,
    "LITERAL_FLOAT"                 : c_LITERAL_FLOAT,
    "LITERAL_STRING"                : c_LITERAL_STRING,
    "LITERAL_BOOL"                  : c_LITERAL_BOOL,
    "LITERAL_TUPLE"                 : c_LITERAL_TUPLE,
    "MULTI_TUPLE"                   : c_MULTI_TUPLE, 
    "TUPLE_SINGLE"                  : c_TUPLE_SINGLE, 
    "LITERAL_LIST"                  : c_LITERAL_LIST, 
    "LITERAL_DICTIONARY"            : c_LITERAL_DICTIONARY,
    "LITERAL_SET"                   : c_LITERAL_SET,
    "LITERAL_FUNCTION"              : c_LITERAL_FUNCTION,
    "LITERAL_NONE"                  : c_LITERAL_NONE,

    # ARGUMENT LISTS
    "ARGUMENTLIST"                  : c_ARGUMENTLIST,
    "ARGUMENTLIST_SINGLE"           : c_ARGUMENTLIST_SINGLE,
    "ARGUMENTLIST_MULTI"            : c_ARGUMENTLIST_MULTI,
    "DEFAULTLIST_SINGLE"            : c_DEFAULTLIST_SINGLE,
    "DEFAULTLIST_MULTI"             : c_DEFAULTLIST_MULTI,

    # MISC. LIST CONSTRUCTS
    "EXPRESSIONLIST_SINGLE"         : c_EXPRESSIONLIST_SINGLE,
    "EXPRESSIONLIST_MULTI"          : c_EXPRESSIONLIST_MULTI,
    "GENERICLIST_SINGLE"            : c_GENERICLIST_SINGLE,
    "GENERICLIST_MULTI"             : c_GENERICLIST_MULTI,
    "DICTIONARYLIST_SINGLE"         : c_DICTIONARYLIST_SINGLE,
    "DICTIONARYLIST_MULTI"          : c_DICTIONARYLIST_MULTI,
    "GROUPING"                      : c_GROUPING,

    # INDEXING & SLICING
    "INDEXING"                      : c_INDEXING,
    "SLICING"                       : c_SLICING,

    # TRY EXCEPT
    "TRY_EXCEPT"                    : c_TRY_EXCEPT,
    "EXCEPT_SIMPLE"                 : c_EXCEPT_SIMPLE,
    "EXCEPT_ALIAS"                  : c_EXCEPT_ALIAS,
    "EXCEPT_SPECIFIC"               : c_EXCEPT_SPECIFIC,
    "EXCEPT_ELSE"                   : c_EXCEPT_ELSE,
    "EXCEPT_FINALLY"                : c_EXCEPT_FINALLY,

    # ASSERT
    "ASSERT_NOMSG"                  : c_ASSERT_NOMSG,
    "ASSERT_MSG"                    : c_ASSERT_MSG,

    # IDENTITY
    "IS_IDENTITY"                   : c_IS_IDENTITY,
    "IS_NOT_IDENTITY"               : c_IS_NOT_IDENTITY,
    } 


# Irregular keywords to insert
replace = {
    # KEYWORDS
    "continue" : "continue", # these are just here so c_STATEMENT_SIMPLE does
    "break"    : "break",    # not error (as they are irregular statements)
    "pass"     : "pass",

    # OPERATORS
    "&&"       : "and",
    "||"       : "or",
    "!"        : "not ",     # space needed here: other unary ops don't use
    "not"      : "not ",     # ditto

    # BUILTIN INTERFACES
    "tobool"   : "bool",     # these builtin interfaces were renamed for CSPy
    "toint"    : "int",      # to make the purpose (type conversion) clearer
    "tofloat"  : "float",    # and to avoid serious issues with type-checking
    "tostring" : "str",      # (since the names are same as the type names)
    "totuple"  : "tuple",
    "todict"   : "dict",
    "tolist"   : "list",
    "frzset"   : "frozenset",
    "makeset"  : "set",

    # types
    "string"   : "str",

    # MISC.
    "input"    : "raw_input",  # raw_input always reads in a string
    }                          # input would require quotes


# Dictionary to map CSPy file line numbers to Python file line numbers
# (used for runtime error reporting)
lines = {
    # python line #   :  CSPy line #
    }


#------------------------------------------------------------------------------#
# Because of the nature of this translator and the ast nodes, sometimes a      #
# function requires information that is not held within its received node.     #
# These specific situations are handled with the global variables below. See   #
# documentation for a more detailed explanation (particularly for a few more   #
# complicated situations).                                                     #
#------------------------------------------------------------------------------#
in_class  = False    # currently writing a class definition?
current_class = ""   # name of the current class
in_init   = False    # currently writing an init function?
superclass = None    # class definition superclass - for writing __init__

line_num  = 0        # current Python file line number

last_var = ""        # most recent variable - used for class constructors
                     # see documentation for more details

assign_me = None     # most recent variable being assigned a value
                     # see documentation for more details

needs_self = False   # currently writing a class inheritance method
                     # eg. Parent.write(self) rather than Parent.write()

path = ""

overload = {
    'global' : {}
    }