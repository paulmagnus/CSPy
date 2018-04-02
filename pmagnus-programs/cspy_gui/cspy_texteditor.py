import stack
from Tkinter import *
from ttk import*
import keyword
import re
from tkFileDialog import *
from tkMessageBox import *
from tkFont import *
from string import ascii_letters, digits, punctuation, join
from cspy_searchbox import *
from cspy_statusbar import *
from cspy_notebook import *
from cspy_line_numbers import *

type_kw = ['None', 'list', 'dict', 'set', 'string', 'bool', 'tuple', 'float',
           'frozenset', 'int', 'fn', 'proc', 'of']

other_kw = ['extends']

type_conv = ['tostring', 'tofloat', 'repr', 'toint', 'round', 'tolist',
             'toset', 'tofrozenset']

spec_chars = ['=', '>', '<', ':', '*', '+', '-', '/']

filename = "Untitled"


class Text_editor(Text):
    """ This is where you write code """

    tags = {'kw': "#859900",
            'type_kw': "#d33682",
            'other_kw': "#2aa198",
            'type_conv': "#dc322f",
            'spec_chars': "#40E0D0",
            'import_kw': "#cb4b16",
            'line_comment': '#A9A9A9',
            'block_comment': "#20B2AA",
            'declaration_block': "#859900",
            'string': "#40E0D0",
            'function': "#2393E0",
            'class': "#2393E0"}

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

        self.root = root
        self.frame = frame
        self.notebook = notebook
        self.statusbar = statusbar
        self.config(background="#002b36",
                    foreground="white",
                    font=("Monospace", 13),
                    tabs=36,
                    insertbackground="white",
                    bd=0,
                    highlightthickness=0,
                    relief='ridge',
                    lmargin1=10,
                    lmargin2=10)

        #self.tag_config(lmargin1=10,
        #                        lmargin2=10)

        self.background = "#002b36"
        self.config(height=700, width=700, undo=True)
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation

        self.bind('<KeyRelease>', self.key_release)
        self.bind('<Control-q>', self.key_control_q)
        self.bind('<Control-w>', self.key_control_w)
        self.bind('<Control-a>', self.key_control_a)
        self.bind('<Control-l>', self.key_control_l)
        self.bind('<Control-d>', self.key_control_d)
        self.bind('<Control-f>', self.key_control_f)
        self.bind('<Control-n>', self.key_control_n)
        self.bind('<Control-o>', self.key_control_o)
        self.bind('<Control-s>', self.key_control_s)
        self.bind('<Shift-Control-s>', self.key_shift_control_s)

    def change_theme(self):
        """ Switch between Dark/ Light themes """
        if self.background == "#002b36":
            self.config(background="white",
                        foreground="black",
                        font=("Monospace", 13),
                        tabs=36,
                        insertbackground="black")
            self.background = "white"

        else:
            self.config(background="#002b36",
                        foreground="white",
                        font=("Monospace", 13),
                        tabs=36,
                        insertbackground="white")
            self.background = "#002b36"

    def _callback(self, result, *args):
        self.callback(result, *args)

    def callback(self, result, *args):
        """ Updating the position of the cursor """
        index = self.index("insert")
        """ Updating line and column on the status bar """
        self.statusbar.lineCol(*index.split('.'))

        self.frame.linenumbers.redraw()

        """
        As the cursor moves, this part takes care of highligting
        matching parentheses using a stack.
        """
        self.tag_remove("paren_match", "1.0", END)
        ccline = int(self.index("insert").split('.')[0])
        ccol = int(self.index("insert").split('.')[1])
        char = self.get('%s.%d' % (ccline, ccol))

        if (char == "(" or char == "[" or char == "{"):
            stack_index = stack.stack()
            stack_char = stack.stack()
            start = self.index("insert")

            while self.index(start) != self.index(END):

                line = int(self.index(start).split('.')[0])
                col = int(self.index(start).split('.')[1])

                if (self.get('%s.%d' % (line, col)) == "(" or
                   self.get('%s.%d' % (line, col)) == "[" or
                   self.get('%s.%d' % (line, col)) == "{"):

                    stack_index.push(start)
                    stack_char.push(self.get('%s.%d' % (line, col)))

                elif (self.get('%s.%d' % (line, col)) == ")" and
                      stack_char.empty() is False):

                    if stack_char.size == 1 and stack_char.top() == "(":

                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start,
                                     start + "+1c")
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
                                     start,
                                     start + "+1c")
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
                                     start,
                                     start + "+1c")
                        start = END

                    elif stack_char.top() == "[":

                        stack_index.pop()
                        stack_char.pop()

                start = start + "+1c"

        if (char == ")" or char == "]" or char == "}"):
            stack_index = stack.stack()
            stack_char = stack.stack()
            start = self.index("insert")

            while self.index(start) != self.index("1.0"):

                line = int(self.index(start).split('.')[0])
                col = int(self.index(start).split('.')[1])
                if (self.get('%s.%d' % (line, col)) == ")" or
                   self.get('%s.%d' % (line, col)) == "]" or
                   self.get('%s.%d' % (line, col)) == "}"):

                    stack_index.push(start)
                    stack_char.push(self.get('%s.%d' % (line, col)))

                elif (self.get('%s.%d' % (line, col)) == "(" and
                      stack_char.empty() is False):

                    if stack_char.size == 1 and stack_char.top() == ")":
                        self.tag_add('paren_match',
                                     stack_index.top(),
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match',
                                     start,
                                     start + "+1c")
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
                                     start,
                                     start + "+1c")
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
                                     start,
                                     start + "+1c")
                        start = "1.0"
                    
                    elif stack_char.top() == "]":
                        stack_index.pop()
                        stack_char.pop()
                       
                start = start + "-1c"
            
    def config_tags(self):
        for tag, val in self.tags.items():
            self.tag_config(tag, foreground=val,
                            font=("Monospace", 13))
            
        self.tag_config('paren_match', background="#A9A9A9")
        self.tag_lower('declaration_block')
        self.tag_raise('type_kw')
        self.tag_raise('line_comment', 'type_kw')
        self.tag_raise('block_comment', 'line_comment')
            
    def remove_tags(self, start, end):
        for tag in self.tags.keys():
            self.tag_remove(tag, start, end)

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
        
        for token in tokenized:
            end = start + len(token)
            if token == "import":
                self.tag_add('import_kw', '%s.%d' % (cline, start), 
                             '%s.%d' % (cline, end))
                
            elif token in keyword.kwlist:
                self.tag_add('kw', '%s.%d' % (cline, start), 
                             '%s.%d' % (cline, end))
            
            elif token in type_kw:
                self.tag_add('type_kw', '%s.%d' % (cline, start),
                             '%s.%d' % (cline, end))

            elif token[:-1] in type_kw:
                end = end - 1
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
            
            start += len(token) + 1

        # Comment highlighting
        comment_start = buffer.find('#')
        if comment_start != -1:
            self.tag_add('line_comment', '%s.%d' % (cline, comment_start),
                         '%s.%d' % (str(int(cline) + 1), 0))
        self.tag_remove('block_comment', 1.0, END)
        self.tag_remove('declaration_block', 1.0, END)
        self.tag_remove('string', 1.0, END)

        # Docstring highlighting
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
            self.tag_add('block_comment', start, end + "+3c")

            start = end + "+3c"

        # Declaration highlighting
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

        # Function highlighting
        start = "1.0"
        while True:
            start = self.search(r"def",
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

        # Class highlighting
        start = "1.0"
        while True:
            start = self.search(r"class",
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

        # String highlighting
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
            
    def key_control_q(self, event):
        """ Exit the window """
        self.root.destroy()

    def key_control_a(self, event):
        """ Select all """
        self.tag_remove(SEL, "1.0", END)
        self.tag_add(SEL, "1.0", END)
        self.mark_set(INSERT, END)
        self.see(INSERT)
        return 'break'

    def key_control_f(self, event):
        """ Search function """
        SearchBox(self)

    def key_control_s(self, key):
        """ Save """
        global filename
        if filename == "Untitled":
            self.key_shift_control_s(key)
        else:
            current_frame = self.notebook.children[
                self.notebook.select().split('.')[2]]
            for key, val in current_frame.children.iteritems():
                if isinstance(val, Text):
                    text = val
        
            if text is None:
                print("Something is wrong!")

            for key, val in current_frame.children.iteritems():
                if isinstance(val, StatusBar):
                    statusbar = val
            
            if statusbar is None:
                print("Something is wrong!")

            statusbar.set_text()
            self.root.after(3000, statusbar.reset_text)

            t = text.get("0.0", END)
            file = open(filename, 'w')
            file.write(t)
            file.close()

    def key_shift_control_s(self, key):
        """ Save as """
        file = asksaveasfile(mode='w', defaultextension='.cspy')
        if file is None:
            return
        global filename
        filename = file.name

        #match = re.match('(.*/(?P<name>[^/]+)$', filename)
        #str = match.group('name')
        #path = match.group('path')

        self.notebook.tab(self.notebook.select(), text=filename)
        current_frame = self.notebook.children[
            self.notebook.select().split('.')[2]]
        for key, val in current_frame.children.iteritems():
            if isinstance(val, Text):
                text = val
        
        if text is None:
            print("Something is wrong!")

        for key, val in current_frame.children.iteritems():
            if isinstance(val, StatusBar):
                statusbar = val
            
        if statusbar is None:
            print("Something is wrong!")

        statusbar.set_text()
        self.root.after(3000, statusbar.reset_text)

        t = text.get("0.0", END)
        try:
            file.write(t.rstrip())
        except:
            showerror(title="Oops!", message="Unable to save file...")

    def key_control_o(self, key):
        """" Open an existing file """
        file = askopenfile(parent=self.root,
                           mode='rb',
                           title="Select a file")
        if file is not None:
            global filename
            filename = file.name
            
            #match = re.match('(?P<name>[^/]+)$', filename)
            #str = match.group('name')
            #path = match.group('path')

            new_page = CustomFrame(self.root, self.notebook)
            new_page.linenumbers.redraw()

            self.notebook.add(child=new_page, text=filename)
            self.notebook.select(new_page)
            self.root.update()

            t = file.read()
            new_page.get_text_widget().insert("1.0", t)
            cline = 1
            while cline != int(new_page.get_text_widget().
                               index(END).split('.')[0]):
                syn_highlight(new_page.get_text_widget(), cline)
                cline += 1
            file.close()

    def key_control_n(self, key):
        """ Create a new file """
        global filename
        filename = "Untitled"

        new_page = CustomFrame(self.root, self.notebook)
        new_page.linenumbers.redraw()
       
        self.notebook.add(child=new_page, text=filename)
        self.notebook.select(new_page)
        self.root.update()

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

    def key_control_w(self, key):
        """A shortcut for closing the current tab"""
        self.notebook.hide(self.notebook.select())


def syn_highlight(text, cline):
    """ Syntax highlighting for opened files """
    lastcol = 0
    char = text.get('%s.%d' % (cline, lastcol))
    while char != '\n':
        lastcol += 1
        char = text.get('%s.%d' % (cline, lastcol))
        
    buffer = text.get('%s.%d' % (cline, 0), '%s.%d' % (cline, lastcol))
    tokenized = re.split("[^A-Za-z0-9_=><:*+-/]", buffer)
    text.remove_tags('%s.%d' % (cline, 0), '%s.%d' % (cline, lastcol))
    start, end = 0, 0
    for token in tokenized:
        end = start + len(token)
        if token == "import":
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
        start += len(token) + 1

    # Comment highlighting
    comment_start = buffer.find('#')
    if comment_start != -1:
        text.tag_add('line_comment', '%s.%d' % (cline, comment_start),
                     '%s.%d' % (str(int(cline) + 1), 0))
        text.tag_remove('block_comment', 1.0, END)
        text.tag_remove('declaration_block', 1.0, END)
        text.tag_remove('string', 1.0, END)

    # Docstring highlighting
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
        text.tag_add('block_comment', start, end + "+3c")
        start = end + "+3c"

    # Declaration highlighting
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

    # Function highlighting
    start = "1.0"
    while True:
        start = text.search(r"def",
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

    # Class highlighting
    start = "1.0"
    while True:
        start = text.search(r"class",
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

    # String highlighting
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


class CustomFrame(Frame):
    def __init__(self, root, notebook):
        Frame.__init__(self, notebook)
        self.root = root
        self.notebook = notebook
        self.statusbar = StatusBar(self, self.notebook)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        self.text = Text_editor(self.root,
                                self,
                                self.notebook,
                                self.statusbar)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)
        self.linenumbers.pack(side=LEFT, fill=Y)
        self.text.pack(side=RIGHT, fill=BOTH, expand=True)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        
    def get_text_widget(self):
        return self.text
