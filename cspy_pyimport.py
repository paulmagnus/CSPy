#------------------------------------------------------------------------------#
# cspy_pyimport.py                                                             #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, and Matthew R. Jenkins '20       #
# Summer 2017                                                                  #
#                                                                              #
# This file handles importing the declarations from a header file when the     #
# pyimport statement is used in a cspy file. Creates the lexer and parser      #
# using PLY and the grammar definitions given in cspy_header_lexer.py          #
# and cspy_header_parser.py. Once the declarations for classes, functions,     #
# and procedures are read, they are added to the top level environment of the  #
# CSPy parse tree.                                                             #
#                                                                              #
# .cspyh files are used to allow CSPy programs to import code written in       #
# Python by giving the type declarations for the Python code since Python does #
# not use the strongly-typed format that CSPy uses.                            #
#                                                                              #
# See the documentation file for the format of a .cspyh file                   #
#------------------------------------------------------------------------------#

# PYTHON MODULES
import os, getpass, re
import ply.lex as lex
import ply.yacc as yacc
import sys

# LOCAL FILES
from cspy_header_lexer import *
from cspy_header_parser import *
from cspy_header_genenv import generate_environments
from cspy_header_type import det_type
from cspy_builtins import builtins, type_obj
from cspy_runtime import remove_files

yacc.error_count = 3

#------------------------------------------------------------------------------#

def pyimportgenerate(hfile, path):
    
    # LEX AND PARSE THE FILE
    filename = hfile
    if not os.path.isfile(path + hfile):
        script_path = re.match(r'(?P<path>.*)/[^/]+', \
                                   os.path.realpath(__file__)).group('path')
        
        if os.path.isfile(script_path + "/cspy_headers/" + hfile):
            # found header in cspy_headers folder
            try:
                hfile = open(script_path + "/cspy_headers/" + hfile,
                             'rU').read() + "\n"
            except:
                print >> sys.stderr, "Header file '" + script_path + \
                    "/cspy_headers/" + hfile + "' could not be read."
                exit()
        else:
            print >> sys.stderr, "Header file '" + path + hfile + \
                "' could not be found."
            exit()
    else:
        try:
            hfile = open(path + hfile, 'rU').read() + "\n"
        except:
            print >> sys.stderr, "Header file '" + path + hfile + \
                "' could not be read."
            exit()

    lexer = lex.lex()
    lexer.indentwith = None
    lexer.indentedline = None
    lexer.indentstack = [0]
    lexer.input(hfile)

    parser = yacc.yacc(tabmodule="header_parsetab")
    lexer.parser = parser
    parsetree = parser.parse(tracking = True)

    if parsetree:
        parsetree.set_column_num(hfile)
    else:
        remove_files()
        exit(1)

    # GET IMPORTED FILES
    imports = parsetree.flatten("IMPORTBLOCK_SINGLE")
    
    name = filename[:len(filename) - 5]

    if len(filename) <= 5:
        print >> sys.stderr, "Compiler error in cspy_pyimport.py:\nTried " + \
            "to import a non-cspyh file."
        exit(1)

    pyfilename = filename[:-6] + ".py"

    File = None

    # NO FILES IMPORTED
    if not imports:

        # PROCESS SELF
        generate_environments(parsetree)         # add environments
        det_type(parsetree)                      # determine any remaining types
        
        return parsetree

    # FILES IMPORTED
    for statement in imports:

        # PROCESS IMPORTS
        statement = statement[0]
        importtype = statement.label

        # imports must be python files with cspyh headers
        importfile = statement[0] + ".cspyh"
        importtree = pyimportgenerate(importfile, path)

        # ADD IMPORTED CODE TO PARSE TREE
        
        # pyimport simple : pyimport module
        if importtype == "PYIMPORT_SIMPLE":
            importmodule = type_obj("import module", builtins["ImportModule"],
                                    methods = importtree.env)
            parsetree.initiate_var(statement[0], importmodule)

        # pyimport alias : pyimport module as id
        elif importtype == "PYIMPORT_ALIAS":
            alias = statement[1]
            importmodule = type_obj("import module", builtins["ImportModule"],
                                    methods = importtree.env)
            parsetree.initiate_var(alias, importmodule)
            
        # pyimport bulk : from module pyimport *
        elif importtype == "PYIMPORT_BULK":
            for  variable in importtree.env:
                parsetree.initate_var(variable, importtree.env[variable])

        # pyimport discrete : from module pyimport id1, id2, ...
        elif importtype == "PYIMPORT_DISCRETE":
            importids = statement.flatten("IMPORTLIST_SIMPLE")
            for identifier in importids:
                name = identifier[0]
                value = importtree.lookup(name)
                parsetree.initiate_var(name, value)

        else:
            # Should never reach this point
            print >> sys.stderr, "\nCompiler error with imports in " + \
                "cspy_pyimport.py.\nNo import type matched"

    # PROCESS SELF
    generate_environments(parsetree)             # add environments
    det_type(parsetree)                          # determine any remaining types
    return parsetree


path = ""                                   # for importing files (see above)