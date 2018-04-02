import stack
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from ttk import*
import keyword, re
from string import ascii_letters, digits, punctuation, join

from errorFrame import ErrorFrame

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
            'spec_chars' : "#d33682",
            'import_kw' : "#cb4b16",
            'line_comment' : '#A9A9A9',
            "block_comment" : "#20B2AA",
            "declaration_block" : "#859900",
            'string' : "#40E0D0",
            "function" : "#2393E0",
            "class" : "#2393E0"}

    def __init__(self, root, statusbar):
        Text.__init__(self, root, width=600, height=400)

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

#New File
filename = "untitled"
def newFile():
    global filename
    filename = "untitled"
    #text_edit.delete("0.0", END)

#Save
def saveFile():
    global filename
    if filename == "untitled":
        saveas()
    else:    
        t = text_edit.get("0.0", END)
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
    t = text_edit.get("1.0", END)
    try:
        f.write(t.rstrip())
    except:
        showerror(title="Oops!", message="Unable to save file...")

# Open
def openFile():
    f = askopenfile(parent=root, mode='rb', title="Select a file")
    if file != None:
        t = f.read()
        text_edit.insert("1.0", t)
        # add highlighting stuff
        f.close()



class Notebook(Frame):
    """Notebook Widget"""
    def __init__(self, parent, activerelief = RAISED, inactiverelief = RIDGE,
                 xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw ):
       
        self.activefg = activefg                                                           
        self.inactivefg = inactivefg
        #self.font = font
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief                                               
        self.kwargs = kw                                                                   
        self.tabVars = {}                                                                  
        self.tabs = 0                                                                    
        self.noteBookFrame = Frame(parent)                                                 
        self.BFrame = Frame(self.noteBookFrame)                                            
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, padding = 2, **kw)           
        self.noteBook.grid_propagate(0)                                                    
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row =0, sticky = W)
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)

    def change_tab(self, IDNum):
        """Internal Function"""
        
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:                                                  
                if i <> IDNum:                                                             
                    self.tabVars[i][1].grid_remove()                                       
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     
                    self.tabVars[i][0]['foreground'] = self.inactivefg                             
                else:                                                                      
                    self.tabVars[i][1].grid()                                                                    
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   
                    self.tabVars[i][0]['foreground'] = self.activefg                               

    def add_tab(self, width = 2, **kw):
        """Creates a new tab, and returns it's corresponding frame

        """
        
        temp = self.tabs                                                                   
        self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  
        self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) 
        self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                
        self.tabVars[self.tabs][1].grid(row = 0, column = 0)                               
        self.change_tab(0)                                                                 
        self.tabs += 1                                                                     
        return self.tabVars[temp][1]                                                       

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """
        
        self.iteratedTabs = 0                                                              
        for b in self.tabVars.values():                                                    
            if b[1] == tab:                                                                
                b[0].destroy()                                                             
                self.tabs -= 1                                                             
                self.deletedTabs.append(self.iteratedTabs)                                 
                break                                                                      
            self.iteratedTabs += 1                                                         
    
    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """
        
        self.iteratedTabs = 0                                                              
        for b in self.tabVars.values():                                                    
            if b[1] == tab:                                                                
                self.change_tab(self.iteratedTabs)                                         
                break                                                                      
            self.iteratedTabs += 1                                                        

if __name__ == '__main__':
       
    root = Tk()
    root.title("CSPy Text Editor")
    root.minsize(width= 635, height= 450)
    root.maxsize(width= 635, height= 450)

    # nb = Notebook()
    nb = Notebook(root, width=600, height=400, activefg= 'red', inactivefg= 'black')
    nb.grid()
    # nb.grid()
    tab1 = nb.add_tab(text = "Untitled1")
    tab2 = nb.add_tab(text = "Untitled2")

    # Menu bar
    menubar = Menu(root)
    menubar.config(font=("Corbert", 11))    
   
    # Status bar
    
    #status_bar = StatusBar(root)
    #status_bar.pack(side=BOTTOM, fill=X)

    status_bar = StatusBar(tab1)
    status_bar.grid(row=1, column=0, sticky="ew", columnspan=2)

    # Scrollbar
   
    scrollbar = Scrollbar(tab1)
    #scrollbar.pack(side=RIGHT, fill=BOTH)

    #scrollbar = Scrollbar(tab1)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Text editorScrollbar
   
    #text_edit = SyntaxHighlightingText(root, status_bar)
    
    text_edit = SyntaxHighlightingText(tab1, status_bar)
    text_edit.config(foreground = 'white')
    text_edit.grid(row=0, column=0, sticky="nsew")
    text_edit.focus()

    text_edit = SyntaxHighlightingText(tab2, status_bar)
    text_edit.config(foreground = 'white')
    text_edit.grid()
    text_edit.focus()   

    scrollbar.config(command=text_edit.yview)
    text_edit.config(yscrollcommand=scrollbar.set)

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
    projmenu.add_command(label = "Run Code")
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
