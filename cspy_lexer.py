#------------------------------------------------------------------------------#
# cspy_lexer.py                                                                #
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
# Contains all the tokens and corresponding token regular expressions for      #
# the language CSPy.                                                           #
#------------------------------------------------------------------------------#

import sys

states = [('indent','exclusive')]

reserved = {
    "None":"NONE",
    "and":"AND",
    "as":"AS",
    "assert":"ASSERT",
    "break":"BREAK",
    "class":"CLASS",
    "continue":"CONTINUE",
    "def":"DEF",
    "del":"DEL",
    "elif":"ELIF",
    "else":"ELSE",
    "except":"EXCEPT",
    "extends":"EXTENDS",
    "finally":"FINALLY",
    "fn":"FN",
    "for":"FOR",
    "from":"FROM",
    "if":"IF",
    "import":"IMPORT",
    "pyimport" : "PYIMPORT",
    "in":"IN",
    "is":"IS",
    "lambda":"LAMBDA",
    "not":"NOT",
    "of":"OF",
    "or":"OR",
    "pass":"PASS",
    "proc":"PROC",
    "raise":"RAISE",
    "return":"RETURN",
    "try":"TRY",
    "while":"WHILE",
    "yield":"YIELD",

    # BUILT-IN NAMES
    "list":"LIST",
    "tuple":"TUPLE",
    "dict":"DICT",
    "set" : "SET",
    "frozenset" : "FROZENSET", 
    "generator" : "GENERATOR",
}

tokens = list(reserved.values()) + [    
    # BASIC TOKENS
    "TILDE",        # ~ Invert Bits
    "EXMARK",       # ! 
    "PERCENT",      # %
    "CARET",        # ^ Bitwise xor
    "BITAND",       # &
    "TIMES",        # *
    "LPAREN",       # (
    "RPAREN",       # )
    "MINUS",        # -
    "PLUS",         # +
    "EQUALS",       # =
    "LCURLY",       # {
    "RCURLY",       # }
    "LBRACKET",     # [
    "RBRACKET",     # ]
    "BITOR",        # | Bitwise or
    "DIVIDE",       # /
    "COLON",        # :
    "SEMICOLON",    # ;
    "COMMA",        # ,
    "LT",           # <
    "GT",           # >
    "DOT",          # .
    "QMARK",        # ?

    # COMPLEX TOKENS
    "DOTDOT",       # ..
    "INTDIV",       # //
    "POW",          # **
    "LSHIFT",       # <<
    "RSHIFT",       # >>
    "GE",           # >=
    "LE",           # <=
    "EQUALTO",      # ==
    "NEQUALTO",     # !=
    "REQUALTO",     # ~=
    "ARROW",        # ->
    "PLUSEQU",      # +=
    "TIMESEQU",     # *=
    "DIVEQU",       # /=
    "MINUSEQU",     # -=
    "MODEQU",       # %=
    "BITANDEQU",    # &=
    "BITOREQU",     # |=
    "BITXOREQU",    # ^=
    "LSHIFTEQU",    # <<=
    "RSHIFTEQU",    # >>=
    "POWEQU",       # **=
    "INTDIVEQU",    # //=
    "BOOLOR",       # ||
    "BOOLAND",      # &&
    "COLONCOLON",   # ::

    # MISC
    "IDENTIFIER",
    "INTLITERAL",
    "FLOATLITERAL",
    "BOOLLITERAL",
    "STRINGLITERAL",
    "DOCSTRING",
    "NL",
    "INDENT",
    "DEDENT",
    "ISNOT",
    "NOTIN"
]


t_TILDE = r'~'
t_EXMARK = r'!'
t_PERCENT = r'%'
t_CARET = r'\^'
t_BITAND = r'&'
t_TIMES = r'\*'
t_RPAREN = r'\)'
t_MINUS = r'\-'
t_PLUS = r'\+'
t_EQUALS = r'='
t_RCURLY = r'}'
t_RBRACKET = r']'
t_BITOR = r'\|'
t_DIVIDE = r'/'
t_COLON = r':'
t_SEMICOLON = r';'
t_LT = r'<'
t_GT = r'>'
t_DOT = r'\.'
t_QMARK = r'\?'
t_DOTDOT = r'\.\.'
t_INTDIV = r'//'
t_POW = r'\*\*'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_GE = r'>='
t_LE = r'<='
t_EQUALTO = r'=='
t_NEQUALTO = r'!='
t_REQUALTO = r'~='
t_ARROW = r'\->'
t_PLUSEQU = r'\+='
t_TIMESEQU = r'\*='
t_DIVEQU = r'/='
t_MINUSEQU = r'\-='
t_MODEQU = r'%='
t_BITANDEQU = r'&='
t_BITOREQU = r'\|='
t_BITXOREQU = r'\^='
t_LSHIFTEQU = r'<<='
t_RSHIFTEQU = r'>>='
t_POWEQU = r'\*\*='
t_INTDIVEQU = r'//='
t_BOOLOR = r'\|\|'
t_BOOLAND = r'&&'
t_COLONCOLON = r'::'
t_STRINGLITERAL = r'(\"(\\.|[^"\n])*\")|(\'(\\.|[^\'\n])*\')'
t_FLOATLITERAL = r'[0-9]*\.[0-9]+'
t_INTLITERAL = r'[0-9]+'
t_ignore_WS =  r'[ \t]'


def t_ISNOT(t):
    r'is[ ]+not'
    return t

def t_NOTIN(t):
    r'not[ ]+in'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    if t.value == 'True' or t.value == 'False':
        t.type = 'BOOLLITERAL'
    return t

def t_LPAREN(t):
    r'\(([ \t]*(\#.*)?)(\n[ \t]*(\#.*)?)*(?!\Z)'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_LCURLY(t):
    r'{([ \t]*(\#.*)?)(\n[ \t]*(\#.*)?)*(?!\Z)'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_LBRACKET(t):
    r'\[([ \t]*(\#.*)?)(\n[ \t]*(\#.*)?)*(?!\Z)'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_COMMA(t):
    r',([ \t]*(\#.*)?)(\n[ \t]*(\#.*)?)*'
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
    if(t.value[-1] == " " or t.value[-1] == "\t"):
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
    print >> sys.stderr, "CSPy : SyntaxError"

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
    print >> sys.stderr, "Lex indent error on Line " + str(t.lineno)