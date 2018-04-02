import subprocess
import stack
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from ttk import*
import keyword, re
from string import ascii_letters, digits, punctuation, join


type_kw = ['None', 'list', 'dict', 'set','string', 'bool', 'tuple', 'float',
           'frozenset', 'int', 'fn', 'proc', 'of']

other_kw = ['extends']

type_conv = ['tostring', 'tofloat', 'repr', 'toint', 'round', 'tolist',
             'toset', 'tofrozenset']

spec_chars = ['=', '>', '<', ':','*','+', '-', '/']


class Text_editor(Text):

    tags = {'kw' : "#859900",
            'type_kw' : "#d33682",
            'other_kw': "#2aa198",
            'type_conv' : "#dc322f",
            'spec_chars' : "#40E0D0",
            'import_kw' : "#cb4b16",
            'line_comment' : '#A9A9A9',
            "block_comment" : "#20B2AA",
            "declaration_block" : "#859900",
            'string' : "#40E0D0",
            "function" : "#2393E0",
            "class" : "#2393E0"}

    def __init__(self, frame, statusbar):
        Text.__init__(self, frame,width=600, height=400)

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

        self.bind('<KeyRelease>', self.key_release)
        self.bind('<Control-w>', self.key_control_w)
        self.bind('<Control-a>', self.key_control_a)
        self.bind('<Control-f>', self.key_control_f)
        #self.bind('<Control-n>', self.key_control_n)
        self.bind('<Control-o>', self.key_control_o)
        self.bind('<Control-s>', self.key_control_s)
        self.bind('<Shift-Control-s>', self.key_shift_control_s)

    def _callback(self, result, *args):
        self.callback(result, *args)

    def callback(self, result, *args):
        index = self.index("insert")
        self.statusbar.lineCol(*index.split('.'))

        # PAREN MATCH
        self.tag_remove("paren_match", "1.0", END)
        ccline = int(self.index("insert").split('.')[0])
        ccol = int(self.index("insert").split('.')[1])
        char = self.get('%s.%d'%(ccline, ccol))

        if (char == "(" or char == "[" or char == "{"):  
       
            stack_index = stack.stack()
            stack_char = stack.stack()
            start = self.index("insert")
          
            while self.index(start) != self.index(END):
          
                line = int(self.index(start).split('.')[0])
                col = int(self.index(start).split('.')[1])

                if (self.get('%s.%d'%(line, col)) == "(" or 
                    self.get('%s.%d'%(line, col)) == "[" or
                    self.get('%s.%d'%(line, col)) == "{"):
                    
                    stack_index.push(start)
                    stack_char.push(self.get('%s.%d'%(line, col)))
       
                elif (self.get('%s.%d'%(line, col)) == ")" and 
                      stack_char.empty() == False):
              
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
                       
                        
                elif (self.get('%s.%d'%(line, col))  == "}" and 
                      stack_char.empty() == False):
                    
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
                       
                    
                elif (self.get('%s.%d'%(line, col))  == "]" and 
                      stack_char.empty() == False):
                   
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

                if (self.get('%s.%d'%(line, col)) == ")" or 
                    self.get('%s.%d'%(line, col)) == "]" or
                    self.get('%s.%d'%(line, col)) == "}"):
                    
                    stack_index.push(start)
                    stack_char.push(self.get('%s.%d'%(line, col)))
       
                elif (self.get('%s.%d'%(line, col)) == "(" and 
                      stack_char.empty() == False):
              
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
                       
                        
                elif (self.get('%s.%d'%(line, col))  == "{" and 
                      stack_char.empty() == False):
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
                       
                    
                elif (self.get('%s.%d'%(line, col))  == "[" and 
                      stack_char.empty() == False):
                    
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
                            font=("Monospace", 12))
            
        self.tag_config("paren_match", background= "#A9A9A9")
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
        char = self.get('%s.%d'%(cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = self.get('%s.%d'%(cline, lastcol))

        buffer = self.get('%s.%d'%(cline,0),'%s.%d'%(cline,lastcol))
        tokenized = re.split("[^A-Za-z0-9_=><:*+-/]", buffer)
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

    def key_control_s(self, key):
        global filename
        if filename == "Untitled":
            saveas()
        else:    
            current_frame = nb.children[nb.select().split('.')[2]]
            for key, val in current_frame.children.iteritems():
                if isinstance(val, Text):
                    text = val
        
            if text == None:
                print("Something is wrong!")

                t = text.get("0.0", END)
                f = open(filename, 'w')
                f.write(t)
                f.close()

    def key_shift_control_s(self, key):
        f = asksaveasfile(mode='w', defaultextension='.cspy')
        if f == None:
            return
        global filename
        filename = f.name
        current_frame = nb.children[nb.select().split('.')[2]]
        for key, val in current_frame.children.iteritems():
            if isinstance(val, Text):
                text = val
        
        if text == None:
            print("Something is wrong!")

        t = text.get("0.0", END)
        try:
            f.write(t.rstrip())
        except:
            showerror(title="Oops!", message="Unable to save file...")

    def key_control_o(self, key):
        f = askopenfile(parent=root, mode='rb', title="Select a file")
        if file != None:
            t = f.read()
            text_edit.insert("1.0", t)
            cline = 1
            while cline != int(text_edit.index(END).split('.')[0]):
                syn_highlight(text_edit, cline)
                cline += 1
            f.close()

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

    def _callback(self, result, *args):
        self.texteditor.callback(result, *args)

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

#Syntax highlighting
def syn_highlight(text, cline):
        #cline = text.index(INSERT).split('.')[0] 
        lastcol = 0
        char = text.get('%s.%d'%(cline, lastcol))
        while char != '\n':
            lastcol += 1
            char = text.get('%s.%d'%(cline, lastcol))

        buffer = text.get('%s.%d'%(cline,0),'%s.%d'%(cline,lastcol))
        tokenized = re.split("[^A-Za-z0-9_=><:*+-/]", buffer)
        text.remove_tags('%s.%d'%(cline, 0), '%s.%d'%(cline, lastcol))
        start, end = 0, 0
        
        for token in tokenized:
            end = start + len(token)
            if token == "import":
                text.tag_add('import_kw', '%s.%d'%(cline, start), 
                             '%s.%d'%(cline, end))
                
            elif token in keyword.kwlist:
                text.tag_add('kw', '%s.%d'%(cline, start), 
                             '%s.%d'%(cline, end))
            
            elif token in type_kw:
                text.tag_add('type_kw', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))

            elif token in other_kw:
                text.tag_add('other_kw', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))

            elif token in type_conv:
                text.tag_add('type_conv', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))
            
            elif token in spec_chars:
                text.tag_add('spec_chars', '%s.%d'%(cline, start),
                             '%s.%d'%(cline, end))
            
            start += len(token)+1

        # Comment highlighting
        comment_start = buffer.find('#')
        if comment_start != -1:
            text.tag_add('line_comment', '%s.%d'%(cline, comment_start),
                          '%s.%d'%(str(int(cline)+1), 0))
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
                              regexp= True)
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
            
            self.tag_add('class',
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
            

# COPY-CUT-PASTE
def copy(texteditor):
    texteditor.clipboard_clear()
    text = text_editor1.get("sel.first", "sel.last")
    texteditor.clipboard_append(text)
    
def cut(texteditor):
    copy(texteditor)
    texteditor.delete("sel.first", "sel.last")

def paste(texteditor):
    text = texteditor.selection_get(selection='CLIPBOARD')
    texteditor.insert('insert', text)
    cline = 1
    while cline != int(texteditor.index(END).split('.')[0]):
        syn_highlight(text_edit, cline)
        cline += 1

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

#New File

filename = "Untitled"
def newFile():
    global filename
    filename = "untitled"
    # Tab frame
    new_page = Frame(nb)
   
    # Status bar    
    new_status_bar = StatusBar(new_page)
    new_status_bar.pack(side=BOTTOM, fill=X)
   
    # Scrollbar
    new_scrollbar = Scrollbar(new_page)
    new_scrollbar.pack(side=RIGHT, fill=BOTH)
    
    # Text editor Scrollbar
    new_text_edit = Text_editor(new_page, new_status_bar)
    new_text_edit.config(foreground = 'white')
    new_text_edit.pack()
    new_text_edit.focus()   
    new_scrollbar.config(command=new_text_edit.yview)
    new_text_edit.config(yscrollcommand=new_scrollbar.set)

    nb.add(child= new_page, text=filename + "      ")
      

#Save
def saveFile():
    global filename
    if filename == "Untitled":
        saveas()
    else: 
        current_frame = nb.children[nb.select().split('.')[2]]
        for key, val in current_frame.children.iteritems():
            if isinstance(val, Text):
                text = val
        
        if text == None:
            print("Something is wrong!")

        t = text.get("0.0", END)
        f = open(filename, 'w')
        f.write(t)
        f.close()

#Save As
def saveas():
    f = asksaveasfile(mode='w', defaultextension='.cspy')
    if f == None:
        return
    global filename
    filename = f.name
    match = re.match('.*/(?P<name>[^/]+)$', filename)
    str = match.group('name')
    nb.tab(nb.select(), text = str+ "    ") 
    current_frame = nb.children[nb.select().split('.')[2]]
    for key, val in current_frame.children.iteritems():
        if isinstance(val, Text):
            text = val
            
    if text == None:
        print("Something is wrong!")

    t = text.get("0.0", END)
    try:
        f.write(t.rstrip())
        filename = f.name
    except:
        showerror(title="Oops!", message="Unable to save file...")

# Open
def openFile():
    f = askopenfile(parent=root, mode='rb', title="Select a file")
    if file != None:
        global filename
        filename = f.name
        match = re.match('.*/(?P<name>[^/]+)$', filename)
        str = match.group('name')
        # Tab frame
        new_page = Frame(nb)
        
        # Status bar    
        new_status_bar = StatusBar(new_page)
        new_status_bar.pack(side=BOTTOM, fill=X)
   
        # Scrollbar
        new_scrollbar = Scrollbar(new_page)
        new_scrollbar.pack(side=RIGHT, fill=BOTH)
    
        # Text editor Scrollbar
        new_text_edit = Text_editor(new_page, new_status_bar)
        new_text_edit.config(foreground = 'white')
        new_text_edit.pack()
        new_text_edit.focus()   
        new_scrollbar.config(command=new_text_edit.yview)
        new_text_edit.config(yscrollcommand=new_scrollbar.set)

        nb.add(child= new_page, text=str + "      ")
        
        t = f.read()
        new_text_edit.insert("1.0", t)
        cline = 1
        while cline != int(new_text_edit.index(END).split('.')[0]):
            syn_highlight(new_text_edit, cline)
            cline += 1
        f.close()

# Run
def run():
    filename = nb.tab(nb.select(), "text")
    print(filename)
    process = subprocess.Popen(["/home/acampbel/CSPy-shared/ulysses/bin/cspy_terminal.sh", 
                                "/home/acampbel/CSPy-shared/ulysses/iayara-programs/"+filename],
                               stdout = subprocess.PIPE)
    out, err = process.communicate()
    print "Error:", err

    print "Out:", out

class CustomNotebook(Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = Style()
        self.images = (
            PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])



if __name__ == '__main__':
       
    

    root = Tk()
    root.title("CSPy Text Editor")
    root.minsize(width= 635, height= 450)
    root.maxsize(width= 635, height= 450)

    nb = CustomNotebook()

    # Tab frame
    page1 = Frame(nb)

    # Menu bar
    menubar = Menu(root)
    menubar.config(font=("Corbert", 11))    
   
    # Status bar    
    status_bar1 = StatusBar(page1)
    status_bar1.pack(side=BOTTOM, fill=X)
   
    # Scrollbar
    scrollbar1 = Scrollbar(page1)
    scrollbar1.pack(side=RIGHT, fill=BOTH)
    
    # Text editor Scrollbar
    text_edit1 = Text_editor(page1, status_bar1)
    text_edit1.config(foreground = 'white')
    text_edit1.pack()
    text_edit1.focus()   
    scrollbar1.config(command=text_edit1.yview)
    text_edit1.config(yscrollcommand=scrollbar1.set)

    nb.add(child= page1, text=filename + "      ")
    nb.pack()

    # File menu 
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label = "New File...      Ctrl+N",
                         command = newFile)
    filemenu.add_command(label = "Open File...    Ctrl+O",
                         command = openFile)
    filemenu.add_command(label = "Save             Ctrl+S",
                         command = saveFile)
    filemenu.add_command(label = "Save as...",
                         command = saveas)
    filemenu.add_separator()
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
    filemenu.add_separator()
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
    projmenu.add_command(label = "Run Code",
                         command = run)
    projmenu.add_command(label = "Submit Code")
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
