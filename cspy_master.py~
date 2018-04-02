#------------------------------------------------------------------------------#
# cspy_master.py                                                               #
#                                                                              #
# Original written by Alex Dennis '18 and Eric Collins '17                     #
# June 2015                                                                    #
#                                                                              #
# Revised and edited by Lyndsay LaBarge '17 and Maya Montgomery '18            #
# July 2016                                                                    #
#                                                                              #
# Revised and edited by Paul Magnus '18, Ines Ayara and Matthew R. Jenkins '20 #
# Summer 2017                                                                  #
#                                                                              #
# A master program which handles the entire compilation process for the        #
# language CSPy, a dialect of Python. Creates the lexer and parser using PLY,  #
# lexes, parses, generates environments, type checks, translates, and executes #
# the given .cspy file, also processing any .cspy files being imported.        #
#                                                                              #
# USAGE: python cspy_master.py filename.cspy                                   #
#------------------------------------------------------------------------------#

# PYTHON MODULES
import sys, re, getpass, os
import ply.lex as lex
import ply.yacc as yacc

# LOCAL FILES
from cspy_lexer import *
from cspy_parser import *
from cspy_genenv import generate_environments
from cspy_type_checker import det_type
from cspy_translate import translate
from cspy_runtime import *
from cspy_builtins import builtins, type_obj
from cspy_pyimport import pyimportgenerate

yacc.error_count = 3

#------------------------------------------------------------------------------#

def find_column(input, token):
    """Compute the column for a token, in the context of some input"""
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    return token.lexpos - last_cr


def get_line_numbers(p, n):
    return [p.lineno(i) for i in range(n)]

def usage():
    print >> sys.stderr, "Error: CSPy compiler may only be called with 1 " + \
        "argument.\n"+ \
        "Retry with .cspy file as sole argument."
    sys.exit(1)

def importgenerate(cspyfile, _imports=[]):

    _imports.append(cspyfile)

    # LEX AND PARSE THE FILE
    filename = cspyfile
    if not os.path.isfile(filename):
        print >> sys.stderr, cspyfile + " could not be found. Did you mean" +\
            " to use pyimport instead of import?"
        exit(1)

    cspy_file_match = re.match(r"(?P<path>.*)/[^/]+\.cspy", filename)
    if cspy_file_match:
        # path found - not being run in current directory
        cspy_file_path = cspy_file_match.group("path")
    else:
        cspy_file_path = ""

    cspyfile = open(cspyfile, 'rU').read() + "\n"
    
    lexer = lex.lex()
    lexer.indentwith = None
    lexer.indentedline = None
    lexer.indentstack = [0]    
    lexer.input(cspyfile)

    parser = yacc.yacc()
    lexer.parser = parser
    parsetree = parser.parse(tracking = True) 
    if parsetree:
        parsetree.set_column_num(cspyfile)
    else:
        print >> sys.stderr, 'Should something have been printed? cspy_master.py'
        remove_files()
        exit(1)


    # GET IMPORTED FILES
    imports = parsetree.flatten("IMPORTBLOCK_SINGLE")

    name = filename[:len(filename) - 5]

    tmp_path = "/tmp/" + getpass.getuser()

    try:
        os.stat(tmp_path)
    except:
        os.mkdir(tmp_path)

    # NO FILES IMPORTED
    if not imports:

        # SAVE FILE NAME
        F = open(tmp_path + "/__import_names.txt", "a")         # see documentation
        F.write(name + "\n")
        F.close()
        
        # PROCESS SELF
        generate_environments(parsetree, filename)            # add environments
        det_type(parsetree, file_name=filename)                # type check
        overloads = translate(parsetree, filename, cspy_file_path) # translate to Python

        return parsetree, _imports, overloads

    # FILES IMPORTED
    else:
        for statement in imports:
            
            # SAVE FILE NAME
            F = open(tmp_path + "/__import_names.txt", "a")     # see documentation
            F.write(name + "\n")
            F.close()

            # PROCESS IMPORTS
            statement = statement[0]
            importtype = statement.label

            # ADD IMPORTED CODE TO PARSE TREE

            # import simple : import module
            if importtype == "IMPORT_SIMPLE":
                importfile = statement[0] + ".cspy"
                importtree, _imports, import_overloads \
                    = importgenerate(path + importfile,
                                     _imports)
                importmodule = type_obj("import module",
                                        builtins["ImportModule"], 
                                    methods = importtree.env)
                import_overloads = {'global' : {},
                                    statement[0] : import_overloads}
                parsetree.initiate_var(statement[0], importmodule)

            # import alias : import module as id
            elif importtype == "IMPORT_ALIAS":
                importfile = statement[0] + ".cspy"
                importtree, _imports, import_overloads \
                    = importgenerate(path + importfile,
                                     _imports)
                alias =  statement[1]
                importmodule = type_obj("import module",
                                        builtins["ImportModule"], 
                                        methods = importtree.env)
                import_overloads = {'global' : {},
                                    alias : import_overloads}
                parsetree.initiate_var(alias, importmodule)

            # import bulk : from module import * 
            elif importtype == "IMPORT_BULK":
                importfile = statement[0] + ".cspy"
                importtree, _imports, import_overloads \
                    = importgenerate(path + importfile,
                                     _imports)
                for variable in importtree.env:
                    parsetree.initiate_var(variable, importtree.env[variable])

            # import discrete : from module import id1, id2, ...
            elif importtype == "IMPORT_DISCRETE":
                importfile = statement[0] + ".cspy"
                importtree, _imports, import_overloads \
                    = importgenerate(path + importfile,
                                     _imports)
                importids = statement.flatten("IMPORTLIST_SIMPLE")
                for identifier in importids:
                    name = identifier[0]
                    value = importtree.lookup_var(name)
                    parsetree.initiate_var(name, value)

                # copy over overloaded names from imports
                tmp = {'global' : {}}

                for name in import_overloads['global']:
                    # copy over the global functions and procedures
                    if import_overloads['global'][name] in importids:
                        tmp['global'][name] = import_overloads['global'][name]
                
                # copy over the imported classes
                for class_name in import_overloads:
                    if class_name in importids:
                        tmp[class_name] = import_overloads[class_name]
                        
                import_overloads = tmp

            #--------------------------------#
            # PYIMPORT - imports from python #
            #--------------------------------#

            # pyimport simple : pyimport module
            elif importtype == "PYIMPORT_SIMPLE":
                importfile = statement[0] + ".cspyh"
                importtree = pyimportgenerate(importfile,
                                              path)
                importmodule = type_obj("import module", 
                                        builtins["ImportModule"],
                                        methods = importtree.env)
                parsetree.initiate_py_var(statement[0], importmodule)
                import_overloads = {'global' : {}}

            # pyimport alias : pyimport module as id
            elif importtype == "PYIMPORT_ALIAS":
                importfile = statement[0] + ".cspyh"
                importtree = pyimportgenerate(importfile, 
                                              path)
                alias = statement[1]
                importmodule = type_obj("import module",
                                        builtins["ImportModule"],
                                        methods = importtree.env)
                parsetree.initiate_py_var(alias, importmodule)
                import_overloads = {'global' : {}}

            # pyimport bulk : from module pyimport *
            elif importtype == "PYIMPORT_BULK":
                importfile = statement[0] + ".cspyh"
                importtree = pyimportgenerate(importfile,
                                                         path)
                for variable in importtree.env:
                    parsetree.initiate_py_var(variable, importtree.env[variable])
                import_overloads = {'global' : {}}
            
            # pyimport discrete : from module pyimport id1, id2, ...
            elif importtype == "PYIMPORT_DISCRETE":
                importfile = statement[0] + ".cspyh"
                importtree = pyimportgenerate(importfile,
                                              path)
                importids = statement.flatten("IMPORTLIST_SIMPLE")
                for identifier in importids:
                    name = identifier[0]
                    value = importtree.lookup_var(name)
                    parsetree.initiate_py_var(name, value)

                import_overloads = {'global' : {}}

            else:
                # Should never reach this point
                print >> sys.stderr, "\nCompiler error with imports in " + \
                    "cspy_master.py.\n" + \
                    "No import type matched"
                sys.exit(1)
            
        # PROCESS SELF
        generate_environments(parsetree, filename)        # add environments
        det_type(parsetree, file_name=filename)                     # type check
        overloads = translate(parsetree, 
                              filename,
                              cspy_file_path,
                              import_overloads)          # translate to Python
        
        return parsetree, _imports, overloads


def main():

    # CHECK ARGS
    if len(sys.argv) != 2:
        usage()

    # CONFIRM VALID FILE
    filename = sys.argv[1]
    if (len(filename) < 6 or filename[len(filename) - 5:] != ".cspy"):
        print >> sys.stderr, "\nError: file must be a CSPy file and end with " +\
            "'.cspy'.\n" + \
            "File received: '" + filename + "'.\n"
        sys.exit(1)
    
    # GET PATH FOR MAIN .CSPY FILE
    find_path = re.compile('(?P<p>[\S]+/)[\S]+')  # saving the main file path
    found_path = find_path.search(filename)       # for locating imported files
    if found_path:                                  # (modules must be in same dir
        global path                                 #  as the main .cspy file)
        path = found_path.group("p")

    # PROCESS AND EXECUTE
    parsetree,imports, overloads = importgenerate(filename)
    run(filename, imports, path, overloads)


path = ""                                         # for importing files (see above)

if __name__ == "__main__":
    main()
