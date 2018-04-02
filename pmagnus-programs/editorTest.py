import stack
from Tkinter import *
from ttk import*
import keyword, re
from string import ascii_letters, digits, punctuation, join

type_kw = ['None', 'list', 'dict', 'set','string', 'bool', 'tuple', 'float',
           'frozenset', 'int', 'fn', 'proc', 'of']

other_kw = ['extends']

type_conv = ['tostring', 'tofloat', 'repr', 'toint', 'round', 'tolist',
             'toset', 'tofrozenset']

spec_chars = ['=', '>', '<', ':','*','+', '-', '/']


class SyntaxHighlightingText(Text):

    tags = {'kw' : "#859900",
            'type_kw' : "#d33682",
            'other_kw': "#2aa198",
            'type_conv' : "#dc322f",
            'spec_chars' : "#2393E0",
            'import_kw' : "#cb4b16",
            'line_comment' : '#A9A9A9',
            "block_comment" : "#20B2AA",
            "declaration_block" : "#859900",
            'string' : "#40E0D0",
            "function" : "#2393E0",
            "class" : "#2393E0"}

    def __init__(self, root, statusbar):
        Text.__init__(self, root)

        private_callback = self.register(self._callback)
        self.tk.eval("""
           proc widget_proxy {actual_widget callback args} {
              # this prevents recursion if the widget is called during callback
              set flag ::dont_recurse(actual_widget)

              # call the real tk widget with the real args
              set result [uplevel [linsert $args 0 $actual_widget]]

              # call the callback and ignore errors, but only do so on inserts,
              # deletes, and changes in the mark. Otherwise we'll call the callback
              # way too often.
              if {! [info exists $flag]} {
                 if {([lindex $args 0] in {insert replace delete}) ||
                     ([lrange $args 0 2] == {mark set insert})} {
                    # the flag makes sure that whatever happens in the callback doesn't
                    # cause the callbacks to be called again.
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

        self.statusbar = statusbar
        self.config(background= "#002b36",
                    foreground= "#586e75",
                    font=("Monospace", 12),
                    tabs=36,
                    insertbackground="white")
        self.config(height = 700, width = 700, undo=True)
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation

        #self.bind('<Button-1>', self.button_1)
        self.bind('<KeyRelease>', self.key_release)
        self.bind('<Control-w>', self.key_control_w)
        self.bind('<Control-a>', self.key_control_a)
        self.bind('<Control-f>', self.key_control_f)

    def _callback(self, result, *args):
        self.callback(result, *args)

    def callback(self, result, *args):
        index = self.index("insert")
        self.statusbar.lineCol(*index.split('.'))

        self.tag_remove("paren_match", "1.0", END)
        ccline = int(self.index("insert").split('.')[0])
        ccol = int(self.index("insert").split('.')[1])
        char = self.get('%s.%d'%(ccline, ccol))

        if (char == ")" or char == "]" or char == "}" or 
            char == "(" or char == "[" or char == "{"):
 
            stack_index = stack.stack()
            stack_char = stack.stack()        
            
            start = "1.0"
            while self.index(start) != self.index(END):
                line = int(self.index(start).split('.')[0])
                col = int(self.index(start).split('.')[1])
                
                #print(line, col)
                #print(self.get('%s.%d'%(line, col)))
                #print(stack_char.empty())

                if (self.get('%s.%d'%(line, col)) == "(" or 
                    self.get('%s.%d'%(line, col)) == "[" or
                    self.get('%s.%d'%(line, col)) == "{"):
                    
                    stack_index.push(start)
                    stack_char.push(self.get('%s.%d'%(line, col)))
                    #stack_char.display()
       
                elif (self.get('%s.%d'%(line, col)) == ")" and 
                      stack_char.empty() == False):
                    if stack_char.top() == "(":
                        # print("It matches!")
                        self.tag_add('paren_match', 
                                     stack_index.top(), 
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match', 
                                     start, 
                                     start + "+1c")
                        stack_index.pop()
                        stack_char.pop()
                        
                elif (self.get('%s.%d'%(line, col))  == "}" and 
                      stack_char.empty() == False):
                    if stack_char.top() == "{":
                    #print("It matches!")
                        self.tag_add('paren_match', 
                                     stack_index.top(), 
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match', 
                                     start, 
                                     start + "+1c")
                        stack_index.pop()
                        stack_char.pop()
                    
                elif (self.get('%s.%d'%(line, col))  == "]" and 
                      stack_char.empty() == False):
                    if stack_char.top() == "[":
                        self.tag_add('paren_match', 
                                     stack_index.top(), 
                                     stack_index.top() + "+1c")
                        self.tag_add('paren_match', 
                                     start, 
                                     start+ "+1c")
                        stack_index.pop()
                        stack_char.pop()         
                    
                start = start + "+1c"


       
    def config_tags(self):
        for tag, val in self.tags.items():
            self.tag_config(tag, foreground=val,
                            font=("Monospace", 12))
            
        self.tag_config("paren_match", background= "#A9A9A9")
        self.tag_lower('declaration_block')
        self.tag_raise('type_kw')
        self.tag_raise('line_comment', 'type_kw')
        self.tag_raise('block_comment', 'line_comment')
            
    def remove_tags(self, start, end):
        for tag in self.tags.keys():
            self.tag_remove(tag, start, end)
        
        #self.tag_remove("paren_match", "1.0", END)


    def key_release(self, key):
        cline = self.index(INSERT).split('.')[0] 
        lastcol = 0
        char = self.get('%s.%d'%(cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d'%(cline, lastcol))

        buffer = self.get('%s.%d'%(cline,0),'%s.%d'%(cline,lastcol))
        tokenized = re.split("[^A-Za-z0-9_]", buffer)

        self.remove_tags('%s.%d'%(cline, 0), '%s.%d'%(cline, lastcol))

        start, end = 0, 0
        for token in tokenized:
            end = start + len(token)
            if token == "import":
                self.tag_add('import_kw', '%s.%d'%(cline, start), 
                             '%s.%d'%(cline, end))
            
            elif token in keyword.kwlist:
                self.tag_add('kw', '%s.%d'%(cline, start), 
                             '%s.%d'%(cline, end))
            
            elif token in type_kw:
                self.tag_add('type_kw', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))

            elif token in other_kw:
                self.tag_add('other_kw', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))

            elif token in type_conv:
                self.tag_add('type_conv', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))
            
            elif token in spec_chars:
                self.tag_add('spec_chars', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))
            
            start += len(token)+1

        # Comment highlighting
        comment_start = buffer.find('#')
        if comment_start != -1:
            self.tag_add('line_comment', '%s.%d'%(cline, comment_start),
                          '%s.%d'%(str(int(cline)+1), 0))
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
                              regexp= True)
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
            
    def key_control_w(self, event):
        root.destroy() 

    def key_control_a(self, event):
        self.tag_remove(SEL, "1.0", END)
        self.tag_add(SEL, "1.0", END)
        self.mark_set(INSERT, END)
        self.see(INSERT)
        return 'break'

    def key_control_f(self, event):
        searchbox = SearchBox(self)

    


class SearchBox:
    def __init__(self, texteditor):       
        self.texteditor = texteditor
        self.root = Tk()
        self.root.title("Search box  ")
        self.entry = Text (self.root)
        self.root.geometry("200x30")
        self.entry.focus()
        self.entry.pack()
        self.config_tags()
        self.characters = ascii_letters + digits + punctuation
        self.entry.bind('<KeyRelease>', self.key_release)
        self.entry.bind('<Control-w>', self.key_control_w)
        
        private_callback = self.entry.register(self._callback)
        self.entry.tk.eval("""
           proc widget_proxy {actual_widget callback args} {
              # this prevents recursion if the widget is called during callback
              set flag ::dont_recurse(actual_widget)

              # call the real tk widget with the real args
              set result [uplevel [linsert $args 0 $actual_widget]]

              # call the callback and ignore errors, but only do so on inserts,
              # deletes, and changes in the mark. Otherwise we'll call the callback
              # way too often.
              if {! [info exists $flag]} {
                 if {([lindex $args 0] in {insert replace delete}) ||
                     ([lrange $args 0 2] == {mark set insert})} {
                    # the flag makes sure that whatever happens in the callback doesn't
                    # cause the callbacks to be called again.
                    set $flag 1
                    catch {$callback $result {*}$args } callback_result
                    unset -nocomplain $flag
                 }
              }

              # return the result from the real widget command
              return $result
           }
           """)
        self.entry.tk.eval("""
           rename {widget} _{widget}
           interp alias {{}} ::{widget} {{}} widget_proxy _{widget} {callback}
           """.format(widget=str(self.entry), callback=private_callback))

    def _callback(self, result, *args):
        self.texteditor.callback(result, *args)
    
    def callback(self, result, *args):
        index = self.texteditor.index("insert")     

    def config_tags(self):
        self.texteditor.tag_configure("search", background="#FFFF00")

    def remove_tags(self, start, end):
        self.texteditor.tag_remove("search", 1.0, END)

    def get_text(self):
        cline = self.entry.index(INSERT).split('.')[0] 
        lastcol = 0
        char = self.entry.get('%s.%d'%(cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.entry.get('%s.%d'%(cline, lastcol))      
        buffer = self.entry.get('%s.%d'%(cline,0),'%s.%d'%(cline,lastcol))
        return buffer

    def key_release(self, key):
        self.remove_tags("1.0", END)
        search_text = self.get_text()
        edit_text = self.texteditor.get("1.0", END)        
        start = 1.0
        while True:
            countVar = StringVar()
            pos = self.texteditor.search(search_text, start, 
                                         stopindex=END, count=countVar, regexp = True)
            if not pos:
                break
            else :
                self.texteditor.tag_add("search", pos, "%s+%sc" % (pos, countVar.get()))  
            start = pos + "+1c"

    def key_control_w(self, key):
        self.remove_tags("1.0", END)
        self.root.destroy()


class StatusBar(Frame) :
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.variable = StringVar()
        self.variable.set('    Line:1' + '  Column:1' + '                          ' +
                          'Tab Size:4' + '         '  + 'CSPy')
        
        s = Style()
        s.configure("BW.TLabel", foreground="white", background="#575757", 
                    padding=2, relief="flat")
        self.label = Label(self,
                           textvariable=self.variable,
                           font=("Monospace", 12),
                           style="BW.TLabel") 

        self.label.pack(fill=X)   
        self.pack()

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

    def lineCol(self, line, col):
        self.variable.set('    Line:' + str(line) + '  Column:' + str(col) 
                          + '                          ' + 'Tab Size:4' + 
                          '         '  + 'CSPy')

# COPY-CUT-PASTE
def copy(texteditor):
    texteditor.clipboard_clear()
    text = texteditor.get("sel.first", "sel.last")
    texteditor.clipboard_append(text)
    
def cut(texteditor):
    copy(texteditor)
    texteditor.delete("sel.first", "sel.last")

def paste(texteditor):
    text = texteditor.selection_get(selection='CLIPBOARD')
    texteditor.insert('insert', text)


# UNDO-REDO
def undo(texteditor):
    texteditor.edit_undo()
def redo(texteditor):
    texteditor.edit_redo()

#EXIT
def exit(root):
    root.destroy()

#SELECT ALL
def key_control_a(text):
    text.tag_remove(SEL, "1.0", END)
    text.tag_add(SEL, "1.0", END)
    text.mark_set(INSERT, END)
    text.see(INSERT)
    return 'break'


if __name__ == '__main__':
       
    root = Tk()
    root.title("CSPy Text Editor")
    root.geometry("600x450")

    # Menu bar
    menubar = Menu(root)
    menubar.config(font=("Corbert", 11), relief="groove")
    
   
    # Status bar
    status_bar = StatusBar(root)
    status_bar.pack(side=BOTTOM, fil=X)


    # Scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=BOTH)

    # Text editor
    text_edit = SyntaxHighlightingText(root, status_bar)
    text_edit.config(foreground = 'white')
    text_edit.pack()
    text_edit.focus()

    scrollbar.config(command=text_edit.yview)
    text_edit.config(yscrollcommand=scrollbar.set)

    # File menu 
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label = "New File...      Ctrl+N")
    filemenu.add_command(label = "Open File...    Ctrl+O")
    filemenu.add_command(label = "Save             Ctrl+S")
    filemenu.add_command(label = "Exit               Ctrl+W",
                         command = lambda: exit(root))
    menubar.add_cascade(label = "File ", menu=filemenu)
    filemenu.config(font=("Corbert", 11), bg="#FFFFFF")

    # Edit menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label = "Copy            Ctrl+C",
                         command = lambda: copy(text_edit))
    editmenu.add_command(label = "Cut               Ctrl+X",
                         command = lambda: cut(text_edit))
    editmenu.add_command(label = "Paste            Ctrl+V", 
                         command = lambda: paste(text_edit))
    editmenu.add_command(label = "Undo            Ctrl+Z",
                         command = lambda: undo(text_edit))
    editmenu.add_command(label = "Redo            Ctrl+Y",
                         command = lambda: redo(text_edit))
    menubar.add_cascade(label = "Edit ", menu=editmenu)
    editmenu.config(font=("Corbert", 11), bg="#FFFFFF")

    # Selection menu
    selectmenu = Menu(menubar, tearoff=0)
    selectmenu.add_command(label = "Select All              Ctrl+A",
                           command = lambda: key_control_a(text_edit))
    selectmenu.add_command(label = "Expand selection to line")
    selectmenu.add_command(label = "Expand selection to word")
    menubar.add_cascade(label = "Selection ", menu=selectmenu)
    selectmenu.config(font=("Corbert", 11), bg="#FFFFFF")

    # Find menu
    findmenu = Menu(menubar, tearoff=0)
    findmenu.add_command(label = "Find            Ctrl+F",
                         command = lambda: SearchBox(text_edit))
    findmenu.add_command(label = "Find next")
    findmenu.add_command(label = "Find previous")
    menubar.add_cascade(label = "Find ", menu=findmenu)
    findmenu.config(font=("Corbert", 11), bg="#FFFFFF")
    
    # Project menu
    projmenu = Menu(menubar, tearoff=0)
    projmenu.add_command(label = "Run       ")
    projmenu.add_command(label = "")
    projmenu.add_command(label = "")
    menubar.add_cascade(label = "Project ", menu=projmenu)
    projmenu.config(font=("Corbert", 11), bg="#FFFFFF")

    # Preferences menu
    prefmenu = Menu(menubar, tearoff=0)
    prefmenu.add_command(label = "Font")
    prefmenu.add_command(label = "Color scheme")
    menubar.add_cascade(label = "Preferences ", menu=prefmenu)
    prefmenu.config(font=("Corbert", 11), bg="#FFFFFF")

    # Help menu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label = "Documentation")
    helpmenu.add_command(label = "Ask a TA")
    helpmenu.add_command(label = "About CSPy")
    menubar.add_cascade(label = "Help? ", menu=helpmenu)
    helpmenu.config(font=("Corbert", 11), bg="#FFFFFF")
    
    root.config(menu=menubar)
    root.mainloop()
