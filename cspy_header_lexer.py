#------------------------------------------------------------------------------#
# cspy_header_lexer.py                                                         #
#                                                                              #
# Written by Paul Magnus '18, Ines Ayara '20, and Matthew R. Jenkins '20       #
# Summer 2017                                                                  #
#                                                                              #
# Contains all the tokens and corresponding token regular expressions for      #
# the header files for importing python programs into CSPy.                    #
#------------------------------------------------------------------------------#

import sys

states = [('indent', 'exclusive')]

reserved = {
    "as" : "AS",
    "class" : "CLASS",
    "def" : "DEF",
    "extends" : "EXTENDS",
    "fn" : "FN",
    "from" : "FROM",
    "pyimport" : "PYIMPORT",
    "of" : "OF",
    "proc" : "PROC",
    "list" : "LIST",
    "tuple" : "TUPLE",
    "dict" : "DICT",
    "set" : "SET",
    "frozenset" : "FROZENSET",
    "generator" : "GENERATOR",
    }

tokens = list(reserved.values()) + [
    # BASIC TOKENS
    "TIMES",        # *
    "LPAREN",       # (
    "RPAREN",       # )
    "COLON",        # :
    "COMMA",        # ,
    "QMARK",        # ?
    "LBRACKET",     # [
    "RBRACKET",     # ]
    "BITOR",        # |

    # COMPLEX TOKENS
    "ARROW",        # ->
    "COLONCOLON",   # ::

    # MISC
    "IDENTIFIER",
    "DOCSTRING",
    "NL",
    "INDENT",
    "DEDENT",
    ]

t_TIMES = r'\*'
t_RPAREN = r'\)'
t_COLON = r':'
t_QMARK = r'\?'
t_ARROW = r'\->'
t_COLONCOLON = r'::'
t_RBRACKET = r']'
t_BITOR = r'\|'
t_ignore_WS = r'[ \t]'

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    if t.value == 'True' or t.value == 'False':
        t.type = 'BOOLLITERAL'
    return t

def t_LPAREN(t):
    r'\(([ \t]*(\#.*)?)(\n[ \t]*(\#.*)?)*'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_LBRACKET(t):
    r'\[([ \t]*(\#.*)?)(\n[ \t]*(\#.*)?)*'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COMMA(t):
    r',([ \t]*(\#.*)?)(\n[ \t]*(\#.*?))*'
    t.lexer.lineno += t.value.count('\n')
    return t

"""....""" or '''...'''
def t_DOCSTRING(t):
    r'("""([^"]|\n)*""")|(\'\'\'([^\']|\n)*\'\'\')'
    t.lexer.lineno += t.value.count('\n')
    return t

# Break up lines using \
def t_CONTLINE(t):
    r'\\[\s\t]*\n[\s\t]*'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_pass_start(t):
    r'^([ \t]|\n|\#.*)+'
    t.lexer.lineno += t.value.count('\n')
    if (t.value[-1] == " " or t.value[-1] == "\t"):
        last_nl = t.value.rfind("\n")
        t.value = t.value[last_nl+1:]
        t.value = len(t.value)
        t.type = "INDENT"
        t.lexer.indentedline = t.lineno
        t.lexer.indentstack.append(t.value)
        return t

# Comment
def t_comment(t):
    r'(/\*((?!\*/)(.|\n))*\*/)\n?|(\#.*)'
    t.lexer.lineno += t.value.count('\n')
    pass

# Pass empty lines to keep code blocks from breaking up
def t_pass(t):
    r'\n[ \t]*(?=[\n\#])'
    t.lexer.lineno += t.value.count('\n')

def t_INITIAL_NL(t):
    r'\n[ \t]*(?![\n\#])'
    t.lexer.lineno += t.value.count('\n')
    t.lexer.push_state('indent')
    t.lexer.skip(-1 * len(t.value))
    t.value = t.value[:1]
    return t

def t_indent_INDENT(t):
    r'\n[ \t]*(?![\n\#])'
    t.value = t.value[1:]

    # Statements are in line with eachother; no indentation occuring
    if len(t.value) == t.lexer.indentstack[-1]:
        t.lexer.pop_state()

    # Dedent occurs when the indentation level is less than the previous
    # indent on the stack
    elif len(t.value) < t.lexer.indentstack[-1]:
        t.type = "DEDENT"
        t.lexer.skip(-1 * len(t.value) - 1)
        t.value = t.lexer.indentstack[-1]
        t.lexer.indentstack.pop()
        return t

    else:
        # Normal indent: return the indent token
        t.lexer.pop_state()
        prev_indent = t.lexer.indentstack[-1]
        t.value = len(t.value)
        t.lexer.indentedline = t.lineno
        t.lexer.indentstack.append(t.value)
        return t

def t_error(t):
    print >> sys.stderr, "CSPy : Header File SytaxError"

    # Get the line from the source text
    source = t.lexer.lexdata.split('\n')
    line = source[t.lineno - 1]

     # Find the column of the token in the source code
    last_nl = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_nl < 0:
        last_nl = -1
    next_nl = t.lexer.lexdata.find('\n', t.lexpos + len(t.value),\
                                   len(t.lexer.lexdata))
    if next_nl < 0:
        next_nl = len(t.lexer.lexdata)
    col = t.lexpos - last_nl 

    # Display line information
    message = "Line " + str(t.lineno) + ", Column " +  str(col) + "\n\n" \
              + line + "\n" + " " * (col - 1) + "^" 
    print >> sys.stderr, message
   
    # Display error message
    result = "Illegal character "
    if (ord(t.value[0]) >= 32 or ord(t.value[0]) <= 126):
        result += "'" + t.value[0] + "'"
    else:
        result += "#" + ord(t.value[0])
    print >> sys.stderr, result
   
    t.lexer.skip(len(t.value))

# this should never be called
def t_indent_error(t):
    print >> sys.stderr, "Lex indent error on Line" + str(t.lineno)