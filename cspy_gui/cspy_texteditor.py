#------------------------------------------------------------------------------#
# cspy_texteditor.py                                                           #
#                                                                              #
# This file contains a single class Text_editor which is an extension on the   #
# standard tkinter text.                                                       #
#                                                                              #
# Written by Ines Ayara '20, Paul Magnus '18, Matthew R. Jenkins '20           #
# Summer 2017                                                                  #
#------------------------------------------------------------------------------#

# A Stack class
from stack import *

# TKINTER MODULES
from Tkinter import *
from ttk import*
from tkFileDialog import *
from tkMessageBox import *
from tkFont import *

# PHYTHON MODULES
import keyword
import re
import os
import threading
from string import ascii_letters, digits, punctuation, join
from split import *

# LOCAL FILES
from cspy_searchbox import *
from cspy_statusbar import *
from cspy_notebook import *
from cspy_line_numbers import *
import solarized


# KEYWORDS
type_kw = ['None', 'list', 'dict', 'set', 'string', 'bool', 'tuple',
           'float', 'frozenset', 'int', 'fn', 'proc', 'of', 'file', 'generator']

other_kw = ['extends', 'True', 'False', 'self']

type_conv = ['tostring', 'tofloat', 'repr', 'toint', 'round', 'tolist',
             'toset', 'tofrozenset']

spec_chars = ['==', '+=', '-=', '*=', '%', '>=', '<=', '=', '->', '>', '<', 
              ':', '*', '+', '-', '/']

# THEMES
DARK = solarized.BASE03
LIGHT = solarized.BASE3

#------------------------------------------------------------------------------#
# class Text_editor                                                            #
#    Attributes:                                                               #
#        - root       : Tk()                                                   #
#        - frame      : Frame Tkinet widget                                    #
#        - notebook   : Notebook ttk widget                                    #
#        - statusbar  : Customized Tkinter label to display current line/col   #
#        - fontsize   : Font size (Adjustable)                                 #
#        - background : Background color (Dark/Light)                          #
#                                                                              #
#    Methods:                                                                  #
#        - change_theme                  : Switch between Dark/Light theme     #
#        - get_font_size                 : Return the font size                #
#        - call back                     : Statusbar update/ Paren match       #
#        - config_tags/remove_tags       : Mainly for syntax highlighting      #
#        - key_release                   : Key release bindingc(Syn. Highlight #
#        - key_control_a                 : Select all                          #
#        - key_control_l                 : Extend selection to line            #
#        - key_control_d                 : Extend selection to word            #
#        - key_return                    : Auto-indent on the return key       #
#        - key_tab                       : Replace tab with 4 spaces           #
#------------------------------------------------------------------------------#


class Text_editor(Text):
    """ This is where you write code """

    tags = {'kw': solarized.GREEN,
            'type_kw': solarized.MAGENTA,
            'other_kw': solarized.CYAN,
            'type_conv': solarized.RED,
            'spec_chars': solarized.YELLOW,
            'import_kw': solarized.ORANGE,
            'line_comment': solarized.BASE0,
            'block_comment': solarized.BASE0,
            'docstring': solarized.CYAN,
            'declaration_block': solarized.GREEN,
            'string': solarized.CYAN,
            'function': solarized.BLUE,
            'class': solarized.BLUE}

    def __init__(self, root, frame, notebook, statusbar):
        Text.__init__(self, frame, width=600, height=400)
        self.focus()

        """
        This code is for detecting every movement of the cursor and
        updating its position (Line/ Col)
        """
        private_callback = self.register(self._callback)
        self.tk.eval("""
           proc widget_proxy {actual_widget callback args} {
              # this prevents recursion if the widget is called during callback 
              set flag ::dont_recurse(actual_widget)

              # call the real tk widget with the real args
              set result [uplevel [linsert $args 0 $actual_widget]]

              # call the callback and ignore errors, but only do so
              #on inserts, deletes, and changes in the mark. Otherwise
              #we'll call the callback way too often.
              if {! [info exists $flag]} {
                 if {([lindex $args 0] in {insert replace delete}) ||
                     ([lrange $args 0 2] == {mark set insert})} {
                    #the flag makes sure that whatever happens in the 
                    #callback doesn't cause the callbacks to be called again.
                    set $flag 1
                    catch {$callback $result {*}$args } callback_result
                    unset -nocomplain $flag
                 }
              }

              # return the result from the real widget command
              return $result
           }
           """)
        self.tk.eval("""
           rename {widget} _{widget}
           interp alias {{}} ::{widget} {{}} widget_proxy _{widget} {callback}
         """.format(widget=str(self), callback=private_callback))

        self.filename = "Untitled"
        self.root = root
        self.frame = frame
        self.notebook = notebook
        self.statusbar = statusbar
        self.fontsize = 13
        self.background = DARK
        self.foreground = "white"
        self.insertbg = "white"

        self.config(background=self.background,
                    foreground=self.foreground,
                    font=("Monospace", self.fontsize),
                    tabs=36,
                    insertbackground=self.insertbg,
                    bd=0,
                    highlightthickness=0,
                    relief='ridge')

        self.config(height=700, width=700, undo=True)
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation

        self.bind('<KeyRelease>', self.key_release)    #Syn. highlight
        self.bind('<Control-a>', self.key_control_a)   #Select all
        self.bind('<Control-l>', self.key_control_l)   #Extend selection to line
        self.bind('<Control-d>', self.key_control_d)   #Extend selection to word
        self.bind('<Return>', self.key_return)         #Auto indent
        self.bind('<Tab>', self.key_tab)               #Replace tab w/ spaces

    #---------------------------------------------------------------------#
    # get_theme() -> string                                               #
    #   Returns the color theme                                           #
    #---------------------------------------------------------------------#
    def get_theme(self):
        return self.background

    #---------------------------------------------------------------------#
    # set_theme(bg : string, fg : string, insertbg : string)              # 
    #   - Changes the background color to bg                              #
    #   - Changes the foreground color to fg                              #
    #   - Changes the insertbackground (cursor) color to insertbg         # 
    #   Themes are:                                                       #
    #   solarized.BASE03                                                  #
    #   solarized.BASE3                                                   #
    #---------------------------------------------------------------------#
    def set_theme(self, bg, fg, insertbg):
        self.background = bg
        self.foreground = fg
        self.insertbg = insertbg
        self.config(background=self.background,
                    foreground=self.foreground,
                    insertbackground=self.insertbg)

    #---------------------------------------------------------------------#
    # get_filename() -> string                                            #
    #   Returns the name of the file                                      #
    #---------------------------------------------------------------------#
    def get_filename(self):
        return self.filename

    #---------------------------------------------------------------------#
    # set_filename(filename : string)                                     # 
    #    Changes the name of the file to filename                         # 
    #---------------------------------------------------------------------#
    def set_filename(self, filename):
        self.filename = filename

    def _callback(self, result, *args):
        self.callback(result, *args)

    #---------------------------------------------------------------------#
    # - Updates the line/col on the status bar                            #
    # - Updates the line number on the left side of the text widget       #
    # - Highlights matching parens                                        #
    #---------------------------------------------------------------------#
    def callback(self, result, *args):
        #Updating the position of the cursor
        index = self.index("insert")

        #for all chars that are > 79/line, highlight extra in red 
        cline = self.index(INSERT).split('.')[0]
        lastcol = 0
        char = self.get('%s.%d' % (cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d' % (cline, lastcol))
        
        last_char = '%s.%d' % (cline, lastcol)
        first_char = '%s.%d' % (cline, 79)
        self.tag_remove("too_long", '%s.%d' % (cline, 0),
                        '%s.%d' % (cline, 0) + " lineend")
        if lastcol > 79:
            self.tag_add("too_long", first_char, last_char)

        #Updating line and column on the status bar
        self.statusbar.lineCol(*index.split('.'))

        #Updating line numbers on the left side
        self.frame.linenumbers.redraw()

        #----------------------------------------------------------------#
        # As the cursor moves, this part takes care of highligting       #
        # matching parentheses using a stack.                            #
        #----------------------------------------------------------------#
        self.tag_remove("paren_match", "1.0", END)
        ccline = int(self.index("insert").split('.')[0])
        ccol = int(self.index("insert").split('.')[1]) - 1
        char = self.get('%s.%d' % (ccline, ccol))

        # If the cursor in right after an opening paren
        if (char == "(" or char == "[" or char == "{"):
            stack_index = stack()
            stack_char = stack()
            start = self.index("insert")
            while self.index(start) != self.index(END):

                line = int(self.index(start).split('.')[0])
                col = int(self.index(start).split('.')[1]) - 1

                if (self.get('%s.%d' % (line, col)) == "(" or
                   self.get('%s.%d' % (line, col)) == "[" or
                   self.get('%s.%d' % (line, col)) == "{"):

                    stack_index.push(start + "-1c")
                    stack_char.push(self.get('%s.%d' % (line, col)))

                elif (self.get('%s.%d' % (line, col)) == ")" and
                      stack_char.empty() is False):

                    if stack_char.size == 1 and stack_char.top() == "(":

                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start + "-1c",
                                     start)
                        start = END

                    elif stack_char.top() == "(":
                        stack_index.pop()
                        stack_char.pop()

                elif (self.get('%s.%d' % (line, col)) == "}" and
                      stack_char.empty() is False):

                    if stack_char.size == 1 and stack_char.top() == "{":

                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start + "-1c",
                                     start)
                        start = END

                    elif stack_char.top() == "{":
                        stack_index.pop()
                        stack_char.pop()

                elif (self.get('%s.%d' % (line, col)) == "]" and
                      stack_char.empty() is False):

                    if stack_char.size == 1 and stack_char.top() == "[":

                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start + "-1c",
                                     start)
                        start = END

                    elif stack_char.top() == "[":

                        stack_index.pop()
                        stack_char.pop()

                #CASE OF PAREN INSIDE STRING exp: print("hi(")
                elif (self.get('%s.%d' % (line, col)) == '"' or
                      self.get('%s.%d' % (line, col)) == "'"):

                    if self.get('%s.%d' % (line, col)) == '"':
                        pos = self.search('"', start, stopindex=END)

                    else:
                        pos = self.search("'", start, stopindex=END)
                    
                    if not pos:
                        break
                    
                    start = str(pos) + "+1c"

                start = start + "+1c"

        # If the cursor is on a closing paren
        if (char == ")" or char == "]" or char == "}"):

            stack_index = stack()   #Stack for the indexes of parens
            stack_char = stack()    #Stack for for parens
            start = self.index("insert")

            while self.index(start) != self.index("1.0"):

                line = int(self.index(start).split('.')[0])
                col = int(self.index(start).split('.')[1]) - 1
                if (self.get('%s.%d' % (line, col)) == ")" or
                   self.get('%s.%d' % (line, col)) == "]" or
                   self.get('%s.%d' % (line, col)) == "}"):

                    stack_index.push(start + "-1c")
                    stack_char.push(self.get('%s.%d' % (line, col)))

                elif (self.get('%s.%d' % (line, col)) == "(" and
                      stack_char.empty() is False):

                    if stack_char.size == 1 and stack_char.top() == ")":
                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start + "-1c",
                                     start)
                        start = "1.0"

                    elif stack_char.top() == ")":
                        stack_index.pop()
                        stack_char.pop()

                elif (self.get('%s.%d' % (line, col)) == "{" and
                      stack_char.empty() is False):
                    if stack_char.size == 1 and stack_char.top() == "}":

                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start + "-1c",
                                     start)
                        start = "1.0"

                    elif stack_char.top() == "}":
                        stack_index.pop()
                        stack_char.pop()

                elif (self.get('%s.%d' % (line, col)) == "[" and
                      stack_char.empty() is False):
                    
                    if stack_char.size == 1 and stack_char.top() == "]":
                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start + "-1c",
                                     start)
                        start = "1.0"
                    
                    elif stack_char.top() == "]":
                        stack_index.pop()
                        stack_char.pop()
                
                #CASE OF PAREN INSIDE STRING exp: print("hi(")
                elif (self.get('%s.%d' % (line, col)) == '"' or
                      self.get('%s.%d' % (line, col)) == "'"):

                    if self.get('%s.%d' % (line, col)) == '"':
                        start = start + "-1c"
                        line = int(self.index(start).split('.')[0])
                        col = int(self.index(start).split('.')[1]) - 1
                        while (self.get('%s.%d' % (line, col)) != '"' and
                               self.index(start) != self.index("1.0")):
                            start = start + "-1c"
                            line = int(self.index(start).split('.')[0])
                            col = int(self.index(start).split('.')[1]) - 1
                    else:
                        start = start + "-1c"
                        line = int(self.index(start).split('.')[0])
                        col = int(self.index(start).split('.')[1]) - 1
                        while (self.get('%s.%d' % (line, col)) != "'" and
                               self.index(start) != self.index("1.0")):
                            start = start + "-1c"
                            line = int(self.index(start).split('.')[0])
                            col = int(self.index(start).split('.')[1]) - 1
                            
                start = start + "-1c"
            
    def config_tags(self):
        for tag, val in self.tags.items():
            self.tag_config(tag, foreground=val,
                            font=("Monospace", self.fontsize))

        self.tag_config('too_long', foreground=solarized.RED)
        self.tag_config('paren_match', background=solarized.BASE1)
        self.tag_lower('declaration_block')
        self.tag_lower('spec_chars')
        self.tag_raise('type_kw')
        self.tag_raise('string', 'line_comment')
        self.tag_raise('string', 'type_kw')
        self.tag_raise('line_comment', 'type_kw')
        self.tag_raise('block_comment', 'line_comment')
        self.tag_raise('docstring', 'block_comment')
        self.tag_raise('too_long', 'docstring')
            
    def remove_tags(self, start, end):
        for tag in self.tags.keys():
            self.tag_remove(tag, start, end)

    #---------------------------------------------------------------------#
    #                  Syntax Highlighting on key release                 #
    #---------------------------------------------------------------------#
    def key_release(self, key):
        cline = self.index(INSERT).split('.')[0]
        lastcol = 0
        char = self.get('%s.%d' % (cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d' % (cline, lastcol))

        buffer = self.get('%s.%d' % (cline, 0),
                          '%s.%d' % (cline, lastcol))
        tokenized = re.split("[^A-Za-z0-9_=><:*+-/]", buffer)

        self.remove_tags('%s.%d' % (cline, 0),
                         '%s.%d' % (cline, lastcol))
        
        start, end = 0, 0
        for s in tokenized:
            lst = split_string(s, [":", ",", "."])
            for token in lst:
                end = start + len(token)
                if token == "import" or token == "pyimport":
                    self.tag_add('import_kw', '%s.%d' % (cline, start), 
                                 '%s.%d' % (cline, end))
                
                elif token in keyword.kwlist:
                    self.tag_add('kw', '%s.%d' % (cline, start), 
                                 '%s.%d' % (cline, end))
            
                elif token in type_kw:
                    self.tag_add('type_kw', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))

                elif token in other_kw:
                    self.tag_add('other_kw', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))

                elif token in type_conv:
                    self.tag_add('type_conv', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))
            
                elif token in spec_chars:
                    self.tag_add('spec_chars', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))
    
                start += len(token)
            start += 1

        #LINE COMMENT
        comment_start = buffer.find('#')
        if comment_start != -1:
            self.tag_add('line_comment', '%s.%d' % (cline, comment_start),
                         '%s.%d' % (str(int(cline) + 1), 0))
        self.tag_remove('docstring', 1.0, END)
        self.tag_remove('block_comment', 1.0, END)
        self.tag_remove('declaration_block', 1.0, END)
        self.tag_remove('string', 1.0, END)

        #BLOCK COMMENT
        start = "1.0"
        while True:
            start = self.search(r"\/\*",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if self.get(start, start + "+2c") == "/*":
                end = self.search(r"\*\/",
                                  start + "+2c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = self.search(r'\*\/',
                                  start + "+2c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            self.tag_add('block_comment', start, end + "+2c")

            start = end + "+2c"

        #DOCSTRING
        start = "1.0"
        while True:
            start = self.search(r"(''')|(\"\"\")",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if self.get(start, start + "+3c") == "'''":
                end = self.search(r"'''",
                                  start + "+3c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = self.search(r'"""',
                                  start + "+3c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            self.tag_add('docstring', start, end + "+3c")

            start = end + "+3c"

        #VAR DECLARATION
        start = "1.0"
        while True:
            start = self.search(r"::",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break

            end = self.search(r"::",
                              start + "+2c",
                              stopindex=END,
                              regexp=True)

            if not end:
                end = END
            
            self.tag_add('declaration_block',
                         start,
                         end + "+2c")

            start = end + "+2c"

        #FUNCTION
        start = "1.0"
        while True:
            start = self.search(r"def ",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            end = self.search(r'\(',
                              start + "+4c",
                              stopindex=END,
                              regexp=True)
            if not end:
                end = END
                
            self.tag_add('function',
                         start + "+4c",
                         end)

            start = end + "+1c"

        #CLASS
        start = "1.0"
        while True:
            start = self.search(r"class ",
                                start,
                                stopindex=END,
                                regexp=True)
            
            if not start:
                break
            
            end = self.search(r"(:)|(\()",
                              start + "+6c",
                              stopindex=END,
                              regexp=True)
            if not end:
                end = END
            
            self.tag_add('class',
                         start + "+6c",
                         end)

            start = end + "+1c"

        #STRING
        start = "1.0"
        while True:
            start = self.search(r"(')|(\")",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if self.get(start, start + "+1c") == "'":
                end = self.search(r"'",
                                  start + "+1c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = self.search(r'"',
                                  start + "+1c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            self.tag_add('string', start, end + "+1c")

            start = end + "+1c"

    #--------------------------------------------------------------------------#
    #  Auto-indentation for ":", "," inside parens, closing parens, and key    #
    # words : return, yield, raise.                                            #
    #--------------------------------------------------------------------------#
    def key_return(self, key):
        """ Auto indentation when the return button is pressed """ 
        cline = int(self.index(INSERT).split('.')[0])
        lastcol = 0
        char = self.get('%s.%d' % (cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d' % (cline, lastcol))  

        text = self.get('%s.%d' % (cline, 0), self.index(INSERT))      
        line = cline + 1

        if len(text) > 1:

            #CASE OF ":"      
            if text[-1] == ":" and text[-2] != ":" and\
                    text[-2] != ")" and text[-2] != "]" and text[-2] != "}": 

                self.insert(INSERT, "\n")
                indent = re.search(r"^(?P<indent>[ ]*)", text).group("indent")
                self.insert('%s.%d' % (line, 0), indent + "    ")
                return "break"

            #CASE OF ): or ]: or }: 
            if text[-1] == ":" and (text[-2] == ")" or\
               text[-2] == "]" or text[-2] == "}"):

                curr_index = self.index(INSERT)
                self.insert(INSERT, "\n")
                indent = 0
                start = "1.0"
                open_stack = stack()
                close_stack = stack()
                while start != curr_index:

                    if self.get(start) == "(" or\
                            self.get(start) == "[" or\
                            self.get(start) == "{":
                        open_stack.push(start)

                    elif self.get(start) == ")" or\
                            self.get(start) == "]" or\
                            self.get(start) == "}":
                            close_stack.push(start)

                    start = self.index(start + "+1c")
                    
                if not open_stack.empty():
                    paren_line = int(open_stack.top().split('.')[0])
                    indent_col = 0
                    c = self.get('%s.%d' % (paren_line, indent_col))
                    while c == " ":
                        indent += 1
                        indent_col += 1
                        c = self.get('%s.%d' % (paren_line, indent_col))

                if self.get(self.index(INSERT)) == " ":
                    indent -= 1
                self.insert('%s.%d' % (line, 0), indent * " " + "    ")
                return "break"
        
            # CASE OF "," INSIDE SINGLE/MULTIPLE PAREN/BRACKETS/BRACES
            elif text[-1] == "," or text[-2] == ", ":
            
                curr_index = self.index(INSERT)
                self.insert(INSERT, "\n")
                indent = len(re.search(r"^(?P<indent>[ ]*)",
                             text).group("indent"))
                start = "1.0"
                open_stack = stack()
                close_stack = stack()
                while start != curr_index:

                    if self.get(start) == "(" or\
                            self.get(start) == "[" or\
                            self.get(start) == "{":
                        open_stack.push(start)

                    elif self.get(start) == ")" or\
                            self.get(start) == "]" or\
                            self.get(start) == "}":
                            close_stack.push(start)

                    if not open_stack.empty() and not close_stack.empty():

                        if (self.get(open_stack.top()) == "(" and\
                                self.get
                            (self.index(close_stack.top())) == ")") or\
                                (self.get
                                 (self.index(open_stack.top())) == "[" and\
                                     self.get
                                 (self.index(close_stack.top())) == "]") or\
                                     (self.get
                                      (self.index(open_stack.top())) == "{" and\
                                          self.get
                                      (self.index(close_stack.top())) == "}"):
                            open_stack.pop()
                            close_stack.pop()

                    start = self.index(start + "+1c")
                    
                    if not open_stack.empty():
                        indent = int(open_stack.top().split('.')[1]) + 1
            
                if self.get(self.index(INSERT)) == " ":
                    indent -= 1
                self.insert('%s.%d' % (line, 0), indent * " ")
                return "break"
            
            #CASE OF ), ], }
            elif text[-1] == ")" or text[-1] == "]" or text[-1] == "}":
           
                curr_index = self.index(INSERT)
                self.insert(INSERT, "\n")
                indent = 0
                start = "1.0"
                open_stack = stack()
                close_stack = stack()
                while start != curr_index:
                    if self.get(start) == "(" or\
                            self.get(start) == "[" or\
                            self.get(start) == "{":
                        open_stack.push(start)

                    elif self.get(start) == ")" or\
                            self.get(start) == "]" or\
                            self.get(start) == "}":
                            close_stack.push(start)

                    start = self.index(start + "+1c")
               
                if not open_stack.empty():
                    paren_line = int(open_stack.top().split('.')[0])
                    indent_col = 0
                    c = self.get('%s.%d' % (paren_line, indent_col))
                    while c == " ":
                        indent += 1
                        indent_col += 1
                        c = self.get('%s.%d' % (paren_line, indent_col))
                if self.get(self.index(INSERT)) == "":
                    indent -= 1
                self.insert('%s.%d' % (line, 0), indent * " ")
                return "break"

            #CASE OF RETURN/YIELD/RAISE
            start = '%s.%d' % (cline, 0)
            end = self.index(INSERT)
            return_index = self.search("return",
                                       start,
                                       stopindex=end)
            yield_index = self.search("yield",
                                      start,
                                      stopindex=end)
            raise_index = self.search("raise",
                                      start,
                                      stopindex=end)
            if return_index or yield_index or raise_index:
                if return_index:
                    indent = int(return_index.split('.')[1])
                elif yield_index:
                    indent = int(yield_index.split('.')[1])
                else:
                    indent = int(raise_index.split('.')[1])

                if indent > 0:
                    indent -= 4
                    
                self.insert(INSERT, "\n")
                self.insert('%s.%d' % (line, 0), indent * " ")
                return "break"
                                      
            #OTHER
            else:
                self.insert(INSERT, "\n")
                indent = re.search(r"^(?P<indent>[ ]*)", text).group("indent")
                if indent:
                    if self.get(self.index(INSERT)) == "":
                        indent = indent[:-1]
                    self.insert('%s.%d' % (line, 0), indent)
                return "break"

    #--------------------------------------------------------------------------#
    #                      Replace a tab with 4 spaces                         #
    #--------------------------------------------------------------------------#
    def key_tab(self, key):
        self.insert(INSERT, " " * 4)
        return "break"
    #--------------------------------------------------------------------------#
    #                          Select all (shortcut)                           #
    #--------------------------------------------------------------------------#
    def key_control_a(self, event):
        self.tag_remove(SEL, "1.0", END)
        self.tag_add(SEL, "1.0", END)
        self.mark_set(INSERT, END)
        self.see(INSERT)
        return 'break'
    #--------------------------------------------------------------------------#
    #                           Save (shortcut)                                #
    #--------------------------------------------------------------------------#
    def save(self,):
        if self.filename == "Untitled":
            self.save_as()
            return
        
        statusbar = self.notebook.get_current_statusbar()

        t = self.get("0.0", END)
        try:
            file = open(self.filename, 'w')
            file.write(t)
            file.close()
            statusbar.set_text()
            self.root.after(3000, statusbar.reset_text)
        except IOError:
            showerror(title="Save Error",
                      message="Unable to save file " + self.filename)
    #--------------------------------------------------------------------------#
    #                          Save as (shortcut)                              #
    #--------------------------------------------------------------------------#
    def save_as(self):
        try:
            file = asksaveasfile(mode='w', defaultextension='.cspy')
        except IOError:
            showerror(title="SaveError",
                      message="Unable to save file...")
            return
        if file is None:
            return
        self.filename = file.name

        self.notebook.tab(self.notebook.select(), text=self.filename)
        statusbar = self.notebook.get_current_statusbar()
        t = self.get("0.0", END)

        try:
            file.write(t.rstrip())
            statusbar.set_text()
            self.root.after(3000, statusbar.reset_text)
        except IOError:
            showerror(title="Save error",
                      message="Unable to save file " + self.filename)
    #--------------------------------------------------------------------------#
    #                 Extend selection to the rest of the line                 #
    #--------------------------------------------------------------------------#
    def key_control_l(self, key):
        """ Select the rest of the line """
        cline = self.index(INSERT).split('.')[0]
        lastcol = 0
        char = self.get('%s.%d' % (cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d' % (cline, lastcol))
        self.tag_remove(SEL, INSERT, '%s.%d' % (cline, lastcol))
        self.tag_add(SEL, INSERT, '%s.%d' % (cline, lastcol))
        self.mark_set(INSERT, '%s.%d' % (cline, lastcol))
        self.see(INSERT)
        return 'break'
    #--------------------------------------------------------------------------#
    #                  Extend selection to the rest of the word                #
    #--------------------------------------------------------------------------#
    def key_control_d(self, key):
        """ Select the rest of the word """
        cline = self.index(INSERT).split('.')[0]
        lastcol = 0
        char = self.get('%s.%d' % (cline, lastcol))
        while char != " ":
            lastcol += 1
            char = self.get('%s.%d' % (cline, lastcol))
        self.tag_remove(SEL, INSERT, '%s.%d' % (cline, lastcol))
        self.tag_add(SEL, INSERT, '%s.%d' % (cline, lastcol))
        self.mark_set(INSERT, '%s.%d' % (cline, lastcol))
        self.see(INSERT)
        return 'break'
    #--------------------------------------------------------------------------#
    # get_fontsize() -> int                                                    #
    #   returns the font size of the current text widget                       #
    #--------------------------------------------------------------------------#
    def get_fontsize(self):
        return self.fontsize

    #--------------------------------------------------------------------------#
    # This is a separate syntax highlighting function called when a pre-       #
    # existing file is opened in the text editor.                              #
    #                                                                          #
    # Parameters:                                                              #
    #     - A text widget (Current one)                                        #
    #     - A current line index                                               #
    #--------------------------------------------------------------------------#
    def syn_highlight(text, cline):
        lastcol = 0
        char = text.get('%s.%d' % (cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = text.get('%s.%d' % (cline, lastcol))
    
        buffer = text.get('%s.%d' % (cline, 0),
                          '%s.%d' % (cline, lastcol))
        tokenized = re.split("[^A-Za-z0-9_=><:*+-/]", buffer)
    
        text.remove_tags('%s.%d' % (cline, 0),
                         '%s.%d' % (cline, lastcol))
        start, end = 0, 0
        
        # import/keywords/types/type conversion/special chars
        for s in tokenized:
            lst = split_string(s, [":", ",", "."])

            for token in lst:
                end = start + len(token)
                if token == "import" or token == "pyimport":
                    text.tag_add('import_kw', '%s.%d' % (cline, start), 
                                 '%s.%d' % (cline, end))
                
                elif token in keyword.kwlist:
                    text.tag_add('kw', '%s.%d' % (cline, start), 
                                 '%s.%d' % (cline, end))
            
                elif token in type_kw:
                    text.tag_add('type_kw', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))

                elif token in other_kw:
                    text.tag_add('other_kw', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))

                elif token in type_conv:
                    text.tag_add('type_conv', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))
            
                elif token in spec_chars:
                    text.tag_add('spec_chars', '%s.%d' % (cline, start),
                                 '%s.%d' % (cline, end))
    
                start += len(token)
            start += 1

        #LINE COMMENT
        comment_start = buffer.find('#')
        if comment_start != -1:
            text.tag_add('line_comment', '%s.%d' % (cline, comment_start),
                         '%s.%d' % (str(int(cline) + 1), 0))
        text.tag_remove('docstring', 1.0, END)
        text.tag_remove('block_comment', 1.0, END)
        text.tag_remove('declaration_block', 1.0, END)
        text.tag_remove('string', 1.0, END)

        #BLOCK COMMENT
        start = "1.0"
        while True:
            start = text.search(r"\/\*",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if text.get(start, start + "+2c") == "/*":
                end = text.search(r"\*\/",
                                  start + "+2c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = text.search(r'\*\/',
                                  start + "+2c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            text.tag_add('block_comment', start, end + "+2c")

            start = end + "+2c"

        #DOCSTRING
        start = "1.0"
        while True:
            start = text.search(r"(''')|(\"\"\")",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
        
            if text.get(start, start + "+3c") == "'''":
                end = text.search(r"'''",
                                  start + "+3c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = text.search(r'"""',
                                  start + "+3c",
                                  stopindex=END,
                                  regexp=True)
            
            if not end:
                end = END
            text.tag_add('docstring', start, end + "+3c")
            
            start = end + "+3c"

        #VAR DECLARATION
        start = "1.0"
        while True:
            start = text.search(r"::",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break

            end = text.search(r"::",
                              start + "+2c",
                              stopindex=END,
                              regexp=True)

            if not end:
                end = END
            
            text.tag_add('declaration_block',
                         start,
                         end + "+2c")

            start = end + "+2c"

        #FUNCTION
        start = "1.0"
        while True:
            start = text.search(r"def ",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            end = text.search(r'\(',
                              start + "+4c",
                              stopindex=END,
                              regexp=True)
            if not end:
                end = END
                
            text.tag_add('function',
                         start + "+4c",
                         end)

            start = end + "+1c"

        #CLASS
        start = "1.0"
        while True:
            start = text.search(r"class ",
                                start,
                                stopindex=END,
                                regexp=True)
            
            if not start:
                break
            
            end = text.search(r"(:)|(\()",
                              start + "+6c",
                              stopindex=END,
                              regexp=True)
            if not end:
                end = END
            
            text.tag_add('class',
                         start + "+6c",
                         end)

            start = end + "+1c"

        #STRING
        start = "1.0"
        while True:
            start = text.search(r"(')|(\")",
                                start,
                                stopindex=END,
                                regexp=True)
            if not start:
                break
            
            if text.get(start, start + "+1c") == "'":
                end = text.search(r"'",
                                  start + "+1c",
                                  stopindex=END,
                                  regexp=True)

            else:
                end = text.search(r'"',
                                  start + "+1c",
                                  stopindex=END,
                                  regexp=True)

            if not end:
                end = END
            text.tag_add('string', start, end + "+1c")
        
            start = end + "+1c"
